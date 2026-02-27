REQUIRED = {
    'characters': ['id','name','base_stats'],
    'weapons': ['id','name','tags','base_stats','pattern_type'],
    'passives': ['id','name','tags','effects'],
    'enemies': ['id','name','stats','tags'],
}

def validate(kind: str, items: list[dict]):
    req = REQUIRED.get(kind, [])
    for i, row in enumerate(items):
        for key in req:
            if key not in row:
                raise ValueError(f'{kind}[{i}] missing {key}')
