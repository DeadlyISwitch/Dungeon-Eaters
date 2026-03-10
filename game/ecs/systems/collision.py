def circles(ax, ay, ar, bx, by, br):
    dx, dy = ax-bx, ay-by
    return dx*dx + dy*dy <= (ar+br)*(ar+br)
