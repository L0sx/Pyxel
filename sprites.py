from enum import Enum
from typing import Tuple


SPRITE_TYPE = Tuple[int, int, int, int, int, int]


class Sides(Enum):
    LEFT = -1, 0
    RIGHT = 1, 0
    UP = 0, -1
    DOWN = 0, 1
    UP_LEFT = -1, -1
    UP_RIGHT = 1, -1
    DOWN_LEFT = -1, 1
    DOWN_RIGHT = 1, 1


LEFT = Sides.LEFT
RIGHT = Sides.RIGHT
UP = Sides.UP
DOWN = Sides.DOWN


COLKEY = 7

ATTACK = (
    (2, 0, 0, 8, 8, 0),
    (2, 8, 0, 8, 8, 0),
    (2, 0, 8, 8, 8, 0),
    (2, 8, 8, 8, 8, 0),
)

PLAYER = {
    LEFT: (0, 0, 8, 8, 8, COLKEY),
    RIGHT: (0, 8, 8, 8, 8, COLKEY),
    UP: (0, 8, 0, 8, 8, COLKEY),
    DOWN: (0, 0, 0, 8, 8, COLKEY),
}

ENEMIE1 = {
    LEFT: (0, 0, 0, 8, 8, COLKEY),
    RIGHT: (0, 0, 0, 8, 8, COLKEY),
    UP: (0, 0, 0, 8, 8, COLKEY),
    DOWN: (0, 24, 0, 8, 8, 1),
}


class Items:
    blade = 2, 40, 0, 8, 8, 15

EXP_ORB = (
        (2, 16, 16, 8, 8, 15),
        (2, 24, 16, 8, 8, 15),
        (2, 16, 24, 8, 8, 15),
        (2, 24, 24, 8, 8, 15)
)


HOUSE = 0, 32, 0, 16, 16, COLKEY
CARAMBA = 0, 0, 16, 8, 8, COLKEY

GRASS = 1, 32, 0, 8, 8, COLKEY
TREE = 1, 40, 0, 8, 8, COLKEY

PORTAL = (
    (1, 32, 8, 8, 8, COLKEY),
    (1, 40, 8, 8, 8, COLKEY),
)

TURRET = (
    (0, 0, 48, 8, 8, COLKEY),
    (0, 8, 48, 8, 8, COLKEY),
    (0, 0, 56, 8, 8, COLKEY),
    (0, 8, 56, 8, 8, COLKEY),
)
