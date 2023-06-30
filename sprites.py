from enum import Enum


class Colors:
    BLACK = 0
    BLUE1 = 1
    PURPLE = 2
    PISCINA = 3
    MARROM = 4
    BLUE2 = 5
    BLUE3 = 6
    WHITE = 7
    PINK = 8
    ORANGE = 9
    YELLOW = 10
    GREEN = 11
    BLUE4 = 12
    GRAY = 13
    SALMON = 14
    BEGE = 15


GRASS1 = [(1, 32, 64, 8, 8, Colors.WHITE),]
GRASS2 = [(1, 40, 64, 8, 8, Colors.WHITE),]
GRASS3 = [(1, 32, 72, 8, 8, Colors.WHITE),]
GRASS4 = [(1, 40, 72, 8, 8, Colors.WHITE),]
WATER1 = [(1, 32, 32, 8, 8, Colors.WHITE),]
WATER2 = [(1, 40, 32, 8, 8, Colors.WHITE),]
WATER3 = [(1, 32, 40, 8, 8, Colors.WHITE),]
WATER4 = [(1, 40, 40, 8, 8, Colors.WHITE),]


class Sides(Enum):
    RIGHT = 0
    RIGHT_UP = 45
    DOWN = 90
    LEFT_DOWN = 135
    LEFT = 180
    LEFT_UP = 225
    UP = 270


LEFT = Sides.LEFT
RIGHT = Sides.RIGHT
UP = Sides.UP
DOWN = Sides.DOWN


ENEMY1 = [
    (0, 0, 48, 8, 8, Colors.WHITE),
    (0, 8, 48, 8, 8, Colors.WHITE),
    (0, 0, 56, 8, 8, Colors.WHITE),
    (0, 8, 56, 8, 8, Colors.WHITE),
]
ENEMY2 = [
    (0, 32, 0, 16, 16, 1),
    (0, 32, 16, 16, 16, 1),
    (0, 48, 16, 16, 16, 1),
    (0, 48, 16, 16, 16, 1),
]


ATTACK = [
    (2, 0, 0, 8, 8, 0),
    (2, 8, 0, 8, 8, 0),
    (2, 0, 8, 8, 8, 0),
    (2, 8, 8, 8, 8, 0),
]
CYCLONE = [
    (2, 0, 40, 8, 8, Colors.BLACK),
    (2, 0, 48, 8, 8, Colors.BLACK),
    (2, 8, 32, 8, -8, Colors.BLACK),
    (2, 0, 48, -8, 8, Colors.BLACK),
    (2, 0, 40, -8, 8, Colors.BLACK),
    (2, 0, 32, -8, 8, Colors.BLACK),
    (2, 8, 32, 8, 8, Colors.BLACK),
    (2, 0, 32, 8, 8, Colors.BLACK),
]
ARROW = [
    (2, 0, 24, 8, 5, Colors.WHITE),
    (2, 0, 24, -8, 5, Colors.WHITE),
    (2, 0, 16, 5, -8, Colors.WHITE),
    (2, 0, 16, 5, 8, Colors.WHITE),
]
FIREBALL = {
    LEFT: ((2, 8, 24, 8, 5, 7),),
    RIGHT: ((2, 8, 24, -8, 5, 7),),
    DOWN: ((2, 8, 16, 5, -8, 7),),
    UP: ((2, 8, 16, 5, 8, 7),),
}
EXP_ORB = [
    (2, 16, 16, 8, 8, 15),
    (2, 24, 16, 8, 8, 15),
    (2, 16, 24, 8, 8, 15),
    (2, 24, 24, 8, 8, 15)
]


MAGE = {
    LEFT: ((0, 16, 0, -8, 8, 7),),
    RIGHT: ((0, 16, 0, 8, 8, 7),),
    UP: ((0, 16, 0, 8, 8, 7),),
    DOWN: ((0, 16, 0, 8, 8, 7),),
}

WARRIOR = {
    LEFT: ((0, 16, 8, -8, 8, 7),),
    RIGHT: ((0, 16, 8, 8, 8, 7),),
    UP: ((0, 16, 8, 8, 8, 7),),
    DOWN: ((0, 16, 8, 8, 8, 7),),
}

ARCHER = {
    LEFT: ((0, 16, 16, -8, 8, 7),),
    RIGHT: ((0, 16, 16, 8, 8, 7),),
    UP: ((0, 16, 16, 8, 8, 7),),
    DOWN: ((0, 16, 16, 8, 8, 7),),
}

PLAYER = {
    LEFT: ((0, 0, 8, 8, 8, Colors.WHITE),),
    RIGHT: ((0, 8, 8, 8, 8, Colors.WHITE),),
    UP: ((0, 8, 0, 8, 8, Colors.WHITE),),
    DOWN: ((0, 0, 0, 8, 8, Colors.WHITE),),
}
ENEMIE1 = {
    LEFT: ((0, 0, 0, 8, 8, Colors.WHITE),),
    RIGHT: ((0, 0, 0, 8, 8, Colors.WHITE),),
    UP: ((0, 0, 0, 8, 8, Colors.WHITE),),
    DOWN: ((0, 24, 0, 8, 8, 1),),
}
GRASS = [(1, 32, 0, 8, 8, Colors.WHITE)]
TREE = [(1, 40, 0, 8, 8, Colors.WHITE)]
PORTAL = [
    (1, 32, 8, 8, 8, Colors.WHITE),
    (1, 40, 8, 8, 8, Colors.WHITE),
]
