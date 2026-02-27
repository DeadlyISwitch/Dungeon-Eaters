import math

def update(run, dt: float):
    run.spawn_timer += dt
    interval = max(0.2, 1.2 - run.time_alive * 0.01)
    if run.spawn_timer < interval:
        return
    run.spawn_timer = 0
    budget = 1 + int(run.time_alive // 20)
    for _ in range(min(budget, run.enemy_cap)):
        run.spawn_enemy_ring()
