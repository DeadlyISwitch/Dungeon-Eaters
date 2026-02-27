import pygame
from game.procedural.shapes import draw_round_rect

def render(buildlab, screen, font):
    draw_round_rect(screen, pygame.Rect(40,40,1200,640), (16,20,30,220), 12)
    y=60
    lines=[
        'Build Lab (B para volver)',
        f"Preset: {buildlab.current.get('name','new')}",
        f"Weapons: {', '.join(buildlab.current.get('weapons',[]))}",
        f"Passives: {', '.join(buildlab.current.get('passives',[]))}",
        f"Synergies: {', '.join(buildlab.analysis.get('synergies',[]))}",
        f"Evolutions: {buildlab.analysis.get('evolutions',[])}",
        'R: auto-fill | E: export | I: import from clipboard',
    ]
    for ln in lines:
        screen.blit(font.render(ln, True, (220,220,240)), (60,y)); y+=34
