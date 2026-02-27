def update(world, dt: float):
    for eid, t in list(world.get('transform').items()):
        t.x += t.vx * dt
        t.y += t.vy * dt
