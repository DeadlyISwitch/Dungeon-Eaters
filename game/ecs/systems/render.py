import pygame
from game.procedural.sprites import sprite_character, sprite_enemy
from game.procedural.background import draw_background

def render_run(run, screen):
    draw_background(screen, run.biome_id, run.time_alive)
    camx, camy = run.camera
    for gid, g in run.gems.items():
        pygame.draw.circle(screen, (60,240,255), (int(g['x']-camx), int(g['y']-camy)), 6)
    for _, p in run.projectiles.items():
        pygame.draw.circle(screen, (255, 220, 80), (int(p['x']-camx), int(p['y']-camy)), 4)
    for eid, t in run.world.get('transform').items():
        tag = run.world.get('tag').get(eid)
        pos = (int(t.x-camx), int(t.y-camy))
        if tag == 'player':
            screen.blit(sprite_character(run.char_id, 28), (pos[0]-28, pos[1]-28))
        elif tag == 'enemy':
            screen.blit(sprite_enemy(eid%5, 20), (pos[0]-20, pos[1]-20))
