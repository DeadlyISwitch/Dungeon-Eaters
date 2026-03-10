from __future__ import annotations
import json
from pathlib import Path
from game.constants import DATA_DIR
from game.data.schema import validate

class DataRepo:
    def __init__(self):
        self.raw = {}
        for name in [
            'characters','weapons','passives','relics','biomes','enemies',
            'synergies','skilltrees_meta','skilltrees_characters','sets']:
            p = Path(DATA_DIR) / f'{name}.json'
            data = json.loads(p.read_text(encoding='utf-8'))
            validate(name if name in ('characters','weapons','passives','enemies') else '', data)
            self.raw[name] = data
        self.by_id = {k: {x['id']:x for x in v if isinstance(x, dict) and 'id' in x} for k,v in self.raw.items()}
