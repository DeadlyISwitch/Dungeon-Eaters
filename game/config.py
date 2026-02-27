from __future__ import annotations
from dataclasses import dataclass, asdict
import json
from pathlib import Path
from game.constants import SETTINGS_FILE

@dataclass
class Settings:
    up: str = "w"
    down: str = "s"
    left: str = "a"
    right: str = "d"
    fps_cap: int = 120
    fullscreen: bool = False
    scale: float = 1.0

    @classmethod
    def load(cls) -> "Settings":
        p = Path(SETTINGS_FILE)
        if not p.exists():
            return cls()
        try:
            return cls(**json.loads(p.read_text(encoding='utf-8')))
        except Exception:
            return cls()

    def save(self) -> None:
        p = Path(SETTINGS_FILE)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(asdict(self), indent=2), encoding='utf-8')
