from dataclasses import dataclass
from typing import Optional
from engine.components import StateRender, Movement, Combat
from sprites import FIREBALL, Sides


@dataclass
class Player(StateRender, Movement):
    hp: int = 3

    def skill_1(self, world):
        world.add(
            Projectile(x=self.x, y=self.y, angle=self.current_state.value,
                       speed=3, origin=type(self),
                       sprite=FIREBALL[self.current_state], damage=1,
                       duration=15)
        )

    def skill_2(self, world):
        projs = [
            Projectile(x=self.x-8, y=self.y-8, origin=type(self),
                       sprite=FIREBALL[self.current_state], damage=1, duration=15, angle=s.value, speed=2)
            for s in Sides
        ]
        world.add(*projs)


@dataclass
class Enemy(StateRender, Movement, Combat):
    hp: int = 3

    def update(self, world):
        self.move()
        if self.hp <= 0 and world:
            world.remove(self)


@dataclass
class Projectile(StateRender, Movement, Combat):
    origin: Optional[type] = None
    duration: Optional[int] = None

    def update(self, world=None):
        self.move()
        if self.duration is not None:
            self.duration -= 1
        if self.duration and self.duration <= 0:
            if world:
                world.remove(self)

    def collide_with_target(self, other):
        coisa = self.collide_with(other) and self.origin != type(other)
        if coisa:
            return True
        return False
