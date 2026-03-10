from __future__ import annotations
import hashlib, json
from pathlib import Path
from copy import deepcopy
from game.constants import SAVE_FILE, SAVE_BAK
from game.save.defaults import DEFAULT_PROFILE
from game.save.migrations import migrate

class SaveManager:
    def __init__(self):
        self.path = Path(SAVE_FILE)
        self.bak = Path(SAVE_BAK)

    def _digest(self, payload: dict) -> str:
        raw = json.dumps(payload, sort_keys=True, separators=(",",":")).encode()
        return hashlib.sha256(raw).hexdigest()

    def load(self) -> dict:
        data = self._read(self.path) or self._read(self.bak)
        if not data:
            return deepcopy(DEFAULT_PROFILE)
        return migrate(data)

    def _read(self, path: Path):
        if not path.exists():
            return None
        try:
            obj = json.loads(path.read_text(encoding='utf-8'))
            payload, sig = obj['payload'], obj['hash']
            if self._digest(payload) != sig:
                return None
            return payload
        except Exception:
            return None

    def save(self, payload: dict) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        wrapped = {'payload': payload, 'hash': self._digest(payload)}
        txt = json.dumps(wrapped, indent=2)
        if self.path.exists():
            self.bak.write_text(self.path.read_text(encoding='utf-8'), encoding='utf-8')
        self.path.write_text(txt, encoding='utf-8')
