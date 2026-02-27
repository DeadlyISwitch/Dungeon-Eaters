from game.ecs.systems.collision import circles

def update(run, dt: float):
    pt = run.world.get('transform')[run.player]
    for gid, gem in list(run.gems.items()):
        dx, dy = pt.x-gem['x'], pt.y-gem['y']
        d2 = dx*dx + dy*dy
        if d2 < 140*140:
            gem['x'] += dx * dt * 3
            gem['y'] += dy * dt * 3
        if circles(pt.x, pt.y, 16, gem['x'], gem['y'], 7):
            run.gain_xp(gem['xp'])
            del run.gems[gid]
