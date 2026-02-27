import pygame
from functools import lru_cache

@lru_cache(maxsize=128)
def sprite_character(char_seed: str, size: int):
    surf = pygame.Surface((size*2,size*2), pygame.SRCALPHA)
    c = (90,220,255) if 'arcanist' in str(char_seed) else (220,120,255) if 'runner' in str(char_seed) else (170,255,120)
    pygame.draw.circle(surf, (20,20,28), (size,size), size)
    pygame.draw.circle(surf, c, (size,size), size-4)
    pygame.draw.circle(surf, (255,255,255), (size-6,size-6), 4)
    return surf

@lru_cache(maxsize=128)
def sprite_enemy(kind: int, size: int):
    surf = pygame.Surface((size*2,size*2), pygame.SRCALPHA)
    colors=[(255,80,100),(255,140,80),(220,80,255),(80,255,160),(255,220,80)]
    c = colors[kind%len(colors)]
    pygame.draw.circle(surf, (30,10,10), (size,size), size)
    pygame.draw.circle(surf, c, (size,size), size-3)
    return surf
