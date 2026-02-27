from dataclasses import dataclass, field

@dataclass
class Progression:
    soft: int = 0
    hard: int = 0
    unlocks: set[str] = field(default_factory=set)
    cosmetics: set[str] = field(default_factory=set)
    meta_nodes: set[str] = field(default_factory=set)
    char_nodes: dict[str, set[str]] = field(default_factory=dict)
