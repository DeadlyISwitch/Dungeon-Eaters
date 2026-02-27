import pygame
from functools import lru_cache

@lru_cache(maxsize=256)
def make_icon(icon_type: str, size: int = 32):
    s = pygame.Surface((size,size), pygame.SRCALPHA)
    pygame.draw.rect(s, (28,30,40), s.get_rect(), border_radius=7)
    if icon_type == 'sword':
        pygame.draw.line(s, (230,230,240), (10,22), (22,10), 4)
    elif icon_type == 'orb':
        pygame.draw.circle(s, (90,220,255), (16,16), 8)
    else:
        pygame.draw.polygon(s, (180,130,255), [(16,6),(24,24),(8,24)])
    return s
