from dataclasses import dataclass

@dataclass
class FixedStep:
    step: float = 1/60
    acc: float = 0.0

    def push(self, dt: float) -> int:
        self.acc += dt
        c = 0
        while self.acc >= self.step:
            self.acc -= self.step
            c += 1
        return c
