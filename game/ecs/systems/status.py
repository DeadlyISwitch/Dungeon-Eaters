def tick_effects(run, dt: float):
    for eid, sts in list(run.statuses.items()):
        hp = run.world.get('health').get(eid)
        if not hp:
            continue
        for key in list(sts.keys()):
            st = sts[key]
            st['time'] -= dt
            if key in ('burn', 'poison'):
                st['tick'] -= dt
                if st['tick'] <= 0:
                    hp.hp -= st['dps']
                    st['tick'] = 0.5
            if st['time'] <= 0:
                del sts[key]
