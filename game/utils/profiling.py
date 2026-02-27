from dataclasses import dataclass, field
import time

@dataclass
class Profiler:
    values: dict[str, float] = field(default_factory=dict)
    _start: dict[str, float] = field(default_factory=dict)

    def begin(self, key: str) -> None:
        self._start[key] = time.perf_counter()

    def end(self, key: str) -> None:
        s = self._start.get(key)
        if s:
            self.values[key] = (time.perf_counter() - s) * 1000
