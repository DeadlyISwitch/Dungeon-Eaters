from __future__ import annotations
from collections import defaultdict

class World:
    def __init__(self):
        self.next_id = 1
        self.components = defaultdict(dict)

    def create(self) -> int:
        eid = self.next_id
        self.next_id += 1
        return eid

    def add(self, eid: int, comp: str, value):
        self.components[comp][eid] = value

    def get(self, comp: str):
        return self.components[comp]

    def remove(self, eid: int):
        for c in self.components.values():
            c.pop(eid, None)
