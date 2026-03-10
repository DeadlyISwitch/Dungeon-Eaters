from __future__ import annotations
import random

class RunRNG:
    def __init__(self, seed: int):
        self.seed = seed
        self._rng = random.Random(seed)

    def randint(self, a: int, b: int) -> int:
        return self._rng.randint(a, b)

    def random(self) -> float:
        return self._rng.random()

    def choice(self, arr):
        return self._rng.choice(arr)

    def sample(self, arr, n: int):
        n = min(n, len(arr))
        return self._rng.sample(arr, n)
