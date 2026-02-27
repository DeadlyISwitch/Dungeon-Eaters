def migrate(payload: dict) -> dict:
    v = payload.get('save_version', 1)
    if v == 1:
        payload.setdefault('cosmetics', {'owned':[], 'equipped':{}})
        payload['save_version'] = 2
        v = 2
    return payload
