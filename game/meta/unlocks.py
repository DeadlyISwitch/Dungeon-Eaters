def evaluate_unlocks(profile: dict, run_stats: dict) -> list[str]:
    unlocked=[]
    if run_stats.get('time_alive',0) >= 300:
        if 'runner' not in profile['unlocks']['characters']:
            profile['unlocks']['characters'].append('runner'); unlocked.append('runner')
    if run_stats.get('boss_kills',0) >= 1 and 'arcanist' not in profile['unlocks']['characters']:
        profile['unlocks']['characters'].append('arcanist'); unlocked.append('arcanist')
    return unlocked
