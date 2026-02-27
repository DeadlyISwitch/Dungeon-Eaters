import pygame
from game.procedural.shapes import draw_round_rect

def draw_text(screen, font, txt, x, y, c=(230,230,240)):
    screen.blit(font.render(txt, True, c), (x,y))

def render_hud(run, screen, font):
    draw_round_rect(screen, pygame.Rect(10,10,320,108), (20,25,35,220), 10)
    draw_text(screen, font, f"HP: {int(run.player_hp.hp)}/{int(run.player_hp.max_hp)}", 20, 20)
    draw_text(screen, font, f"LVL: {run.level} XP: {run.xp}/{run.next_xp}", 20, 44)
    draw_text(screen, font, f"Kills: {run.kills} Time: {int(run.time_alive)}s", 20, 68)
    draw_text(screen, font, f"Seed: {run.seed}", 20, 92)
