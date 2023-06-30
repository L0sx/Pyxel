import pyxel
from math import radians, degrees, atan2
from dataclasses import dataclass
from typing import Optional
from engine.components import StateRender, Movement, Combat
from sprites import DOWN, FIREBALL, Sides


@dataclass
class Player(StateRender, Movement):
    hp: int = 10
    max_hp: int = 10
    dmg_interval: int = 5

    def skill_1(self, world):
        world.add(
            Projectile(x=self.x, y=self.y, angle=self.current_state.value,
                       speed=3, origin=type(self),
                       sprite=FIREBALL[self.current_state], damage=1,
                       duration=25)
        )

    def skill_2(self, world):
        x = self.x - self.w // 2
        y = self.y - self.h // 2
        projs = [
            Projectile(x=x, y=y, origin=type(self),
                       sprite=FIREBALL[self.current_state], damage=1, duration=25, angle=s.value, speed=2)
            for s in Sides
        ]
        world.add(*projs)


@dataclass
class Enemy(StateRender, Movement, Combat):
    hp: int = 3

    def update(self, game):
        player = game.entities[Player][0]
        self.move_to_target(player)
        if self.hp <= 0 and game:
            game.remove(self)

        if pyxel.frame_count % 30 == 0:

            dx = self.x - player.x
            dy = self.y - player.y

            angle = atan2(dx, dy)
            angle = degrees(angle)
            game.add(
                Projectile(x=self.x, y=self.y, angle=-angle,
                           speed=3, origin=type(self),
                           sprite=FIREBALL[DOWN], damage=1,
                           duration=25)
            )


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
