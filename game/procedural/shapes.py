import pygame

def draw_round_rect(surface, rect, color, radius=8):
    pygame.draw.rect(surface, color, rect, border_radius=radius)

def capsule(surface, a, b, r, color):
    pygame.draw.line(surface, color, a, b, r*2)
    pygame.draw.circle(surface, color, a, r)
    pygame.draw.circle(surface, color, b, r)

def starburst(surface, pos, r, color):
    x,y = pos
    pygame.draw.line(surface, color, (x-r,y), (x+r,y),2)
    pygame.draw.line(surface, color, (x,y-r), (x,y+r),2)

def ring(surface, pos, r, color, w=2):
    pygame.draw.circle(surface, color, pos, r, w)

def arc(surface, rect, color, a0, a1, w=2):
    pygame.draw.arc(surface, color, rect, a0, a1, w)

def glow(surface, pos, r, color):
    for i in range(3,0,-1):
        pygame.draw.circle(surface, (*color[:3], 30*i), pos, r*i)
