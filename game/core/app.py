from __future__ import annotations
import time
import math
import pygame
from dataclasses import dataclass
from game.constants import SCREEN_WIDTH, SCREEN_HEIGHT, TITLE
from game.config import Settings
from game.core.state_base import State
from game.core.timing import FixedStep
from game.core import input as input_mod
from game.data.loader import DataRepo
from game.ecs.world import World
from game.ecs.components import Transform, Health
from game.ecs.systems import movement, ai, spawns, combat, loot, xp_level, status, render, ui
from game.utils.rng import RunRNG
from game.utils.math2d import normalize
from game.save.manager import SaveManager
from game.meta import unlocks, cosmetics
from game.buildlab import ui as buildlab_ui, analyzer, recommender, export_import


@dataclass
class BuildLabModel:
    data: dict
    current: dict
    analysis: dict


class RunSession:
    def __init__(self, app, char_id: str, biome_id: str = "abyss"):
        self.app = app
        self.data = app.data
        self.char_id = char_id
        self.biome_id = biome_id
        self.seed = int(time.time()) % 999999
        self.rng = RunRNG(self.seed)
        self.world = World()
        self.player = self.world.create()
        self.world.add(self.player, 'tag', 'player')
        self.world.add(self.player, 'transform', Transform(0, 0))
        c = self.data.by_id['characters'][char_id]
        hp = c['base_stats']['max_hp']
        self.player_hp = Health(hp, hp)
        self.world.add(self.player, 'health', self.player_hp)
        self.world.add(self.player, 'bag', {'weapons': c['starter_weapons'][:], 'passives': []})
        self.world.add(self.player, 'statuses', {})
        self.player_stats = {'damage': c['base_stats']['damage'], 'attack_speed': c['base_stats']['attack_speed']}
        self.projectiles = {}
        self.gems = {}
        self.statuses = {}
        self.time_alive = 0.0
        self.spawn_timer = 0.0
        self.enemy_cap = 90
        self.attack_cd = 0.4
        self.next_pid = 1
        self.next_gid = 1
        self.level = 1
        self.xp = 0
        self.next_xp = xp_level.xp_needed(self.level)
        self.kills = 0
        self.boss_kills = 0
        self.level_up_choices: list[dict] = []
        self.paused_for_level = False
        self.camera = [-(SCREEN_WIDTH // -2), -(SCREEN_HEIGHT // -2)]
        self.damage_by_weapon = {wid: 0 for wid in self.world.get('bag')[self.player]['weapons']}

    def spawn_enemy_ring(self):
        eid = self.world.create()
        ang = self.rng.random() * math.pi * 2
        dist = self.rng.randint(340, 520)
        px = self.world.get('transform')[self.player].x
        py = self.world.get('transform')[self.player].y
        x, y = px + math.cos(ang) * dist, py + math.sin(ang) * dist
        enemy = self.data.raw['enemies'][self.rng.randint(0, len(self.data.raw['enemies']) - 1)]
        self.world.add(eid, 'tag', 'enemy')
        self.world.add(eid, 'transform', Transform(x, y))
        self.world.add(eid, 'health', Health(enemy['stats']['hp'], enemy['stats']['hp']))
        self.world.add(eid, 'enemy_id', enemy['id'])

    def spawn_projectile(self):
        pt = self.world.get('transform')[self.player]
        target = None
        best = 1e18
        for eid, t in self.world.get('transform').items():
            if self.world.get('tag').get(eid) != 'enemy':
                continue
            d = (t.x - pt.x) ** 2 + (t.y - pt.y) ** 2
            if d < best:
                best = d
                target = t
        dx, dy = (1, 0) if not target else normalize(target.x - pt.x, target.y - pt.y)
        self.projectiles[self.next_pid] = {'x': pt.x, 'y': pt.y, 'vx': dx * 420, 'vy': dy * 420, 'ttl': 1.5}
        self.next_pid += 1

    def kill_enemy(self, eid: int):
        t = self.world.get('transform')[eid]
        self.gems[self.next_gid] = {'x': t.x, 'y': t.y, 'xp': 4}
        self.next_gid += 1
        self.kills += 1
        if self.world.get('enemy_id').get(eid) in ('behemoth', 'archon'):
            self.boss_kills += 1
        self.world.remove(eid)

    def gain_xp(self, amount: int):
        self.xp += amount
        while self.xp >= self.next_xp:
            self.xp -= self.next_xp
            self.level += 1
            self.next_xp = xp_level.xp_needed(self.level)
            self.roll_level_up()

    def roll_level_up(self):
        opts = self.data.raw['passives'] + self.data.raw['weapons']
        count = 4 if self.rng.random() < 0.2 else 3
        self.level_up_choices = self.rng.sample(opts, count)
        self.paused_for_level = True

    def apply_choice(self, idx: int):
        c = self.level_up_choices[idx]
        bag = self.world.get('bag')[self.player]
        if 'pattern_type' in c and c['id'] not in bag['weapons'] and len(bag['weapons']) < 6:
            bag['weapons'].append(c['id'])
        elif 'effects' in c and c['id'] not in bag['passives'] and len(bag['passives']) < 6:
            bag['passives'].append(c['id'])
            for eff in c['effects']:
                if eff['stat'] == 'damage':
                    self.player_stats['damage'] *= 1 + eff['value']
                if eff['stat'] == 'attack_speed':
                    self.player_stats['attack_speed'] *= 1 + eff['value']
        self.paused_for_level = False


class MainMenuState(State):
    options = ["Start Run", "Meta Hub", "Build Lab", "Settings", "Quit"]
    def on_enter(self, app):
        self.sel = 0

    def handle_event(self, app, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_DOWN, pygame.K_s): self.sel = (self.sel + 1) % len(self.options)
            if event.key in (pygame.K_UP, pygame.K_w): self.sel = (self.sel - 1) % len(self.options)
            if event.key == pygame.K_RETURN:
                if self.sel == 0: app.change_state(CharacterSelectState())
                elif self.sel == 1: app.change_state(MetaHubState())
                elif self.sel == 2: app.change_state(BuildLabState())
                elif self.sel == 3: app.change_state(SettingsState())
                else: app.running = False

    def render(self, app, screen):
        screen.fill((8, 10, 18))
        y = 220
        for i, opt in enumerate(self.options):
            c = (120, 240, 255) if i == self.sel else (220, 220, 240)
            screen.blit(app.font_big.render("Dungeon Eaters", True, (180, 120, 255)), (420, 120)) if i == 0 else None
            screen.blit(app.font.render(opt, True, c), (550, y)); y += 48


class CharacterSelectState(State):
    def on_enter(self, app):
        self.ids = app.profile['unlocks']['characters']
        self.sel = 0

    def handle_event(self, app, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RIGHT, pygame.K_d): self.sel = (self.sel + 1) % len(self.ids)
            if event.key in (pygame.K_LEFT, pygame.K_a): self.sel = (self.sel - 1) % len(self.ids)
            if event.key == pygame.K_RETURN:
                app.active_character = self.ids[self.sel]
                app.change_state(RunState())
            if event.key == pygame.K_ESCAPE:
                app.change_state(MainMenuState())

    def render(self, app, screen):
        screen.fill((12, 10, 20))
        screen.blit(app.font_big.render("Select Character", True, (220, 220, 240)), (470, 90))
        x = 200
        for i, cid in enumerate(self.ids):
            ch = app.data.by_id['characters'][cid]
            c = (120, 240, 255) if i == self.sel else (170, 170, 190)
            pygame.draw.rect(screen, (20, 26, 36), pygame.Rect(x, 240, 260, 300), border_radius=12)
            screen.blit(app.font.render(ch['name'], True, c), (x + 20, 260))
            bs = ch['base_stats']
            screen.blit(app.font_small.render(f"HP {bs['max_hp']} DMG {bs['damage']} ASPD {bs['attack_speed']}", True, (220,220,235)), (x + 20, 310))
            x += 320


class RunState(State):
    def on_enter(self, app):
        self.run = RunSession(app, app.active_character)

    def handle_event(self, app, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                app.change_state(RunSummaryState(self.run))
            if event.key == pygame.K_F3:
                app.debug_overlay = not app.debug_overlay
            if self.run.paused_for_level and event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4):
                idx = event.key - pygame.K_1
                if idx < len(self.run.level_up_choices):
                    self.run.apply_choice(idx)

    def update(self, app, dt):
        run = self.run
        if run.paused_for_level:
            return
        keys = pygame.key.get_pressed()
        x, y = input_mod.axis(app.settings, keys)
        nx, ny = normalize(x, y)
        pt = run.world.get('transform')[run.player]
        pt.vx, pt.vy = nx * 220, ny * 220
        run.time_alive += dt
        run.enemy_cap = 60 if app.clock.get_fps() < 50 else 100
        if int(run.time_alive) in (60*10, 60*20):
            run.spawn_enemy_ring()
        ai.update(run.world, dt, run.player)
        movement.update(run.world, dt)
        spawns.update(run, dt)
        status.tick_effects(run, dt)
        combat.update(run, dt)
        loot.update(run, dt)
        for eid, t in list(run.world.get('transform').items()):
            if run.world.get('tag').get(eid) != 'enemy':
                continue
            if (pt.x - t.x) ** 2 + (pt.y - t.y) ** 2 < 26 ** 2:
                run.player_hp.hp -= 10 * dt
        if run.player_hp.hp <= 0:
            app.change_state(RunSummaryState(run))
        run.camera = [pt.x - SCREEN_WIDTH / 2, pt.y - SCREEN_HEIGHT / 2]

    def render(self, app, screen):
        render.render_run(self.run, screen)
        ui.render_hud(self.run, screen, app.font)
        if self.run.paused_for_level:
            pygame.draw.rect(screen, (8, 8, 18), pygame.Rect(260, 160, 760, 380), border_radius=12)
            screen.blit(app.font_big.render("Level Up", True, (120, 240, 255)), (560, 180))
            y = 250
            for i, c in enumerate(self.run.level_up_choices):
                txt = f"{i+1}) {c['name']}"
                screen.blit(app.font.render(txt, True, (230, 230, 240)), (320, y)); y += 70


class RunSummaryState(State):
    def __init__(self, run):
        self.run = run

    def on_enter(self, app):
        s = app.profile['stats']
        s['runs'] += 1
        s['best_time'] = max(s['best_time'], int(self.run.time_alive))
        score = int(self.run.time_alive * 5 + self.run.kills)
        s['best_score'] = max(s['best_score'], score)
        app.profile['meta']['soft'] += int(self.run.time_alive // 5)
        app.profile['meta']['hard'] += self.run.boss_kills
        unlocks.evaluate_unlocks(app.profile, {'time_alive': self.run.time_alive, 'boss_kills': self.run.boss_kills})
        app.save_manager.save(app.profile)

    def handle_event(self, app, event):
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
            app.change_state(MainMenuState())

    def render(self, app, screen):
        screen.fill((10, 8, 16))
        lines=[
            'Run Summary',
            f'Time: {int(self.run.time_alive)}s  Kills: {self.run.kills}  Level: {self.run.level}',
            f'Seed: {self.run.seed}',
            f'Soft earned: {int(self.run.time_alive // 5)} Hard earned: {self.run.boss_kills}',
            'Press Enter to return menu'
        ]
        y=160
        for i,l in enumerate(lines):
            f = app.font_big if i==0 else app.font
            screen.blit(f.render(l, True, (220,220,240)), (350,y)); y+=60


class MetaHubState(State):
    def handle_event(self, app, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                app.save_manager.save(app.profile)
                app.change_state(MainMenuState())
            if event.key == pygame.K_1 and app.profile['meta']['hard'] >= cosmetics.CATALOG[0]['cost']:
                app.profile['meta']['hard'] -= cosmetics.CATALOG[0]['cost']
                app.profile['cosmetics']['owned'].append(cosmetics.CATALOG[0]['id'])
            if event.key == pygame.K_2 and app.profile['meta']['hard'] >= 1:
                app.profile['skill_trees']['meta'].append('meta_power_1')
                app.profile['meta']['hard'] -= 1

    def render(self, app, screen):
        screen.fill((14, 8, 18))
        lines=[
            'Meta Hub (ESC back, auto-save)',
            f"Soft: {app.profile['meta']['soft']} Hard: {app.profile['meta']['hard']}",
            f"Cosmetics owned: {app.profile['cosmetics']['owned']}",
            '1) Buy skin_neon_green (5 hard)',
            '2) Unlock meta_power_1 node (1 hard)',
            f"Meta nodes: {app.profile['skill_trees']['meta']}"
        ]
        y=120
        for i,l in enumerate(lines):
            screen.blit((app.font_big if i==0 else app.font).render(l, True, (220,220,240)), (120,y)); y+=58


class SettingsState(State):
    def handle_event(self, app, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                app.settings.fullscreen = not app.settings.fullscreen
                app.recreate_window()
            if event.key == pygame.K_ESCAPE:
                app.settings.save()
                app.change_state(MainMenuState())

    def render(self, app, screen):
        screen.fill((10, 14, 20))
        screen.blit(app.font_big.render('Settings', True, (220,220,240)), (560,120))
        screen.blit(app.font.render('F11: toggle fullscreen', True, (220,220,240)), (490,240))
        screen.blit(app.font.render('ESC: save and back', True, (220,220,240)), (520,280))


class BuildLabState(State):
    def on_enter(self, app):
        if app.profile['presets']:
            cur = app.profile['presets'][-1]
        else:
            cur = {'name':'starter','character_id':app.active_character,'goal_tag':'survival','weapons':[],'passives':[],'relic':''}
        self.model = BuildLabModel(app.data.by_id, cur, analyzer.analyze(cur, app.data.by_id))

    def handle_event(self, app, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_b:
                app.change_state(MainMenuState())
            if event.key == pygame.K_r:
                self.model.current = recommender.recommend(app.active_character, 'survival', app.data.by_id)[0]
                self.model.analysis = analyzer.analyze(self.model.current, app.data.by_id)
            if event.key == pygame.K_s:
                app.profile['presets'].append(self.model.current)
                app.save_manager.save(app.profile)
            if event.key == pygame.K_e:
                app.clipboard = export_import.export_build(self.model.current)
            if event.key == pygame.K_i and app.clipboard:
                self.model.current = export_import.import_build(app.clipboard)
                self.model.analysis = analyzer.analyze(self.model.current, app.data.by_id)

    def render(self, app, screen):
        screen.fill((6, 8, 14))
        buildlab_ui.render(self.model, screen, app.font)


class GameApp:
    def __init__(self):
        pygame.init()
        self.settings = Settings.load()
        self.clock = pygame.time.Clock()
        self.recreate_window()
        pygame.display.set_caption(TITLE)
        self.font = pygame.font.SysFont('consolas', 24)
        self.font_small = pygame.font.SysFont('consolas', 18)
        self.font_big = pygame.font.SysFont('consolas', 40)
        self.running = True
        self.debug_overlay = False
        self.data = DataRepo()
        self.save_manager = SaveManager()
        self.profile = self.save_manager.load()
        self.active_character = self.profile['unlocks']['characters'][0]
        self.clipboard = ''
        self.state: State = MainMenuState()
        self.state.on_enter(self)
        self.timing = FixedStep(1 / 60)

    def recreate_window(self):
        flags = pygame.FULLSCREEN if self.settings.fullscreen else 0
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags)

    def change_state(self, nxt: State):
        self.state.on_exit(self)
        self.state = nxt
        self.state.on_enter(self)

    def run(self):
        while self.running:
            dt = self.clock.tick(self.settings.fps_cap) / 1000.0
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.running = False
                self.state.handle_event(self, e)
            for _ in range(self.timing.push(min(dt, 0.1))):
                self.state.update(self, self.timing.step)
            self.state.render(self, self.screen)
            if self.debug_overlay:
                fps = self.clock.get_fps()
                self.screen.blit(self.font_small.render(f'FPS {fps:.1f}', True, (255,255,90)), (8, SCREEN_HEIGHT - 28))
            pygame.display.flip()
        self.settings.save()
        self.save_manager.save(self.profile)
        pygame.quit()
