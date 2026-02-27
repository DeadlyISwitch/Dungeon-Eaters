from game.ecs.systems.collision import circles

def update(run, dt: float):
    run.attack_cd -= dt
    if run.attack_cd <= 0:
        run.attack_cd = max(0.15, 0.8 / max(0.5, run.player_stats['attack_speed']))
        run.spawn_projectile()
    for pid, p in list(run.projectiles.items()):
        p['x'] += p['vx'] * dt
        p['y'] += p['vy'] * dt
        p['ttl'] -= dt
        if p['ttl'] <= 0:
            del run.projectiles[pid]
            continue
        for eid, t in list(run.world.get('transform').items()):
            if run.world.get('tag').get(eid) != 'enemy':
                continue
            if circles(p['x'], p['y'], 6, t.x, t.y, 14):
                hp = run.world.get('health')[eid]
                hp.hp -= run.player_stats['damage']
                if hp.hp <= 0:
                    run.kill_enemy(eid)
                del run.projectiles[pid]
                break
