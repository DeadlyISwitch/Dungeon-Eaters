from dataclasses import dataclass, field

@dataclass
class BuildPreset:
    name: str
    character_id: str
    goal_tag: str
    weapons: list[str] = field(default_factory=list)
    passives: list[str] = field(default_factory=list)
    relic: str = ''
    notes: str = ''
    last_used: float = 0.0
