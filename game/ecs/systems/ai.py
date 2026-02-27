from game.utils.math2d import normalize

def update(world, dt: float, player_eid: int):
    pt = world.get('transform').get(player_eid)
    if not pt:
        return
    for eid, tag in list(world.get('tag').items()):
        if tag != 'enemy':
            continue
        t = world.get('transform')[eid]
        nx, ny = normalize(pt.x - t.x, pt.y - t.y)
        t.vx, t.vy = nx * 90, ny * 90
