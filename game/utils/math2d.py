from __future__ import annotations
import math

def length(x: float, y: float) -> float:
    return math.hypot(x, y)

def normalize(x: float, y: float) -> tuple[float, float]:
    l = length(x, y)
    if l <= 1e-6:
        return 0.0, 0.0
    return x / l, y / l
