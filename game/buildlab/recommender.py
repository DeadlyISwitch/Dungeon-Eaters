def recommend(character_id: str, goal: str, data: dict) -> list[dict]:
    weapons=list(data['weapons'].keys())[:8]
    passives=list(data['passives'].keys())[:10]
    base={'character_id':character_id,'goal_tag':goal,'relic':next(iter(data['relics'].keys()),'')}
    outs=[]
    for name,woff,poff in [('standard',0,0),('offense',2,1),('safe',1,3)]:
        b=dict(base)
        b['name']=name
        b['weapons']=weapons[woff:woff+6]
        b['passives']=passives[poff:poff+6]
        outs.append(b)
    return outs
