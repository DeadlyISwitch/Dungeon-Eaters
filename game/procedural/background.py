import pygame

def draw_background(screen, biome_id: str, t: float):
    base = (8,10,16) if biome_id == 'abyss' else (12,8,18)
    screen.fill(base)
    w,h = screen.get_size()
    c = (30,40,60) if biome_id == 'abyss' else (45,30,65)
    for i in range(0, w, 80):
        y = int((i*0.3 + t*8) % h)
        pygame.draw.circle(screen, c, (i,y), 2)
