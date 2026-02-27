def analyze(build: dict, data: dict) -> dict:
    synergies = []
    tags=[]
    for wid in build.get('weapons',[]):
        tags += data['weapons'].get(wid,{}).get('tags',[])
    for pid in build.get('passives',[]):
        tags += data['passives'].get(pid,{}).get('tags',[])
    tagset = set(tags)
    for rule in data['synergies'].values():
        needs = set(rule.get('requires',[]))
        if needs and needs.issubset(tagset):
            synergies.append(rule['id'])
    evo=[]
    for wid in build.get('weapons',[]):
        w = data['weapons'].get(wid,{})
        e=w.get('evolution')
        if e:
            ok = e['needs_passive'] in build.get('passives',[])
            evo.append({'weapon':wid,'ready':ok,'missing':None if ok else e['needs_passive']})
    return {'synergies':synergies,'evolutions':evo,'score':len(synergies)*10+sum(1 for x in evo if x['ready'])*15}
