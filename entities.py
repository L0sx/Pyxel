import pyxel
from math import degrees, atan2, pi
from dataclasses import dataclass
from typing import Any, Optional
from engine.components import FloatingText, MovementMinDistance, StateRender, Movement, Combat
from sprites import DOWN, FIREBALL, Sides


@dataclass
class Player(StateRender, Movement, Combat):
    hp: int = 10
    max_hp: int = 10
    dmg_interval: int = 5

    exp: int = 0
    next_level_exp: int = 10
    level: int = 1

    def update(self, game):
        if self.exp >= self.next_level_exp:
            self.exp = self.next_level_exp - self.exp
            self.next_level_exp *= pi
            self.damage += 1
            self.max_hp += 1
            self.hp = self.max_hp
            self.level += 1

            dur = 45
            game.add(
                Effect(x=self.x, y=self.y, duration=dur, r=5),
                FloatingText(x=self.x, y=self.y, text="LVL UP", duration=dur)
            )

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
    exp: int = 1

    def update(self, game):
        player = game.entities[Player][0]
        self.move_to_target(player)
        if self.hp <= 0 and game:
            game.remove(self)


@dataclass
class Enemy2(StateRender, MovementMinDistance, Combat):
    hp: int = 3
    exp: int = 1

    def update(self, game):
        player = game.entities[Player][0]
        self.move_keep_distance(player)
        if self.hp <= 0 and game:
            game.remove(self)

        if pyxel.frame_count % 30 == 0:
            dx = self.x - player.x
            dy = self.y - player.y
            angle = - degrees(atan2(dx, dy)) - 90
            game.add(
                Projectile(x=self.x, y=self.y, angle=-angle,
                           speed=3, origin=Enemy,
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


@dataclass
class HUD:
    player: Player

    def draw(self):
        exp = self.player.exp
        exp_atual = exp if exp else 1
        exp_total = self.player.next_level_exp
        percenteExp = (exp_atual / exp_total)
        tamanhoBarra = pyxel.width - 20

        xlife = self.player.x
        ylife = self.player.y - 4
        tamanhoLife = self.player.w
        percenteLife = (self.player.hp / self.player.max_hp)

        pyxel.circ(10, 10, self.player.w, 7)
        pyxel.circb(10, 10, self.player.w, 10)

        pyxel.rect(10, 10, tamanhoBarra * percenteExp, 4, 3)
        pyxel.rectb(10, 10, tamanhoBarra, 4, 7)

        pyxel.rect(xlife, ylife, tamanhoLife * percenteLife, 1, 8)


@dataclass
class Effect:
    _type: str = 'circ'
    x: float = 15
    y: float = 15
    r: int = 5
    colkey: int = 16
    size_inc: int = 1
    duration: Optional[int] = None

    def draw(self):
        if self.colkey >= 16:
            color = pyxel.frame_count % 15
        else:
            color = self.colkey
        pyxel.circb(self.x, self.y, self.r, color)

    def update(self, game):
        self.r += self.size_inc

        if self.duration is not None:
            self.duration -= 1
            if self.duration <= 0:
                game.remove(self)
