from dataclasses import dataclass, field

@dataclass
class Transform:
    x: float
    y: float
    vx: float = 0
    vy: float = 0

@dataclass
class Health:
    hp: float
    max_hp: float

@dataclass
class CombatStats:
    dmg: float
    speed: float
    area: float = 1.0
    cooldown: float = 1.0

@dataclass
class Bag:
    weapons: list[str] = field(default_factory=list)
    passives: list[str] = field(default_factory=list)
