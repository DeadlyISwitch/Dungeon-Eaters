import pygame

KEYMAP = {
    'w': pygame.K_w, 'a': pygame.K_a, 's': pygame.K_s, 'd': pygame.K_d
}

def axis(settings, keys):
    x = float(keys[KEYMAP.get(settings.right, pygame.K_d)]) - float(keys[KEYMAP.get(settings.left, pygame.K_a)])
    y = float(keys[KEYMAP.get(settings.down, pygame.K_s)]) - float(keys[KEYMAP.get(settings.up, pygame.K_w)])
    return x, y
