from dataclasses import dataclass
from typing import Any, Dict, Optional, Sequence


@dataclass
class Sprite:
    sprite: Sequence[tuple] = ((0, 0, 0, 8, 8, 0), )
    states: Optional[Dict] = None
    current_state: Optional[Any] = None
    w: int = sprite[0][3]
    h: int = sprite[0][4]


@dataclass
class Circle:
    r: int = 10
    colkey: int = 16
    r_inc: int = 0


@dataclass
class Square:
    w: int = 10
    h: int = 10
    colkey: int = 16


@dataclass
class Pos:
    x: float = 0
    y: float = 0


@dataclass
class Combat:
    hp: int = 1
    max_hp: int = hp
    damage: int = 0


class Enemy:
    exp: int = 1
    atk_cd: int = 0


class Projectile:
    pass


class EnemyProjectile:
    pass


@dataclass
class CircularMovement:
    speed: float = 0
    angle: float = 0


@dataclass
class Movement:
    speed: float = 0
    angle: float = 0


@dataclass
class Timer:
    time: int


@dataclass
class Text:
    text: str = "PLACEHOLDER"
    colkey: int = 16


class PlayerComponent:
    exp: int = 0
    exp_total: int = 10
    level: int = 1
    projectiles: int = 1
    selectupgrade: bool = False
    speed: int = 1
    atk_speed: int = 30


class Upgrade:
    pass


@dataclass
class Level:
    level: int = 1
    spawned: bool = False
    boss: bool = False
    portal: bool = False

    def __get__(self):
        return self.level


class Portal:
    pass
