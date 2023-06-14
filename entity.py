import logging
from typing import Tuple
import pyxel

from dataclasses import dataclass, field

from sprites import SPRITE_TYPE, Sides, PLAYER, LEFT, RIGHT, UP, DOWN, ATTACK


log = logging.getLogger(__name__)


def player_controller(self):
    if pyxel.btn(pyxel.KEY_LEFT):
        self.player.x = (self.player.x - 1) % pyxel.width
        self.player.sprite = PLAYER[LEFT]
        self.direction = LEFT
    if pyxel.btn(pyxel.KEY_RIGHT):
        self.player.x = (self.player.x + 1) % pyxel.width
        self.player.sprite = PLAYER[RIGHT]
        self.direction = RIGHT
    if pyxel.btn(pyxel.KEY_DOWN):
        self.player.y = (self.player.y + 1) % pyxel.height
        self.player.sprite = PLAYER[DOWN]
        self.direction = DOWN
    if pyxel.btn(pyxel.KEY_UP):
        self.player.y = (self.player.y - 1) % pyxel.height
        self.player.sprite = PLAYER[UP]
        self.direction = UP
    if pyxel.btnp(pyxel.KEY_A):
        self.attack()
    if pyxel.btnp(pyxel.KEY_SPACE):
        self.entities += boom(self.player.x, self.player.y)


def boom(x, y):
    return_list = []
    for side in Sides:
        speedx, speedy = side.value

        multi = 8
        new_speedx = speedx * multi
        new_speedy = speedy * multi

        new_x = x + new_speedx
        new_y = y + new_speedy

        attack = Projectile(new_x, new_y, ATTACK[0], ATTACK, speedx, speedy)
        return_list.append(attack)
    return return_list


def verifyCollision(objeto1, objeto2):
    if (objeto1.x < objeto2.x + objeto2.sprite[3] and
            objeto1.x + objeto1.sprite[3] > objeto2.x and
            objeto1.y < objeto2.y + objeto2.sprite[4] and
            objeto1.y + objeto1.sprite[4] > objeto2.y):
        log.debug(f"{type(objeto1)} - {type(objeto2)} colidiram um com o outro")
        return True
    else:
        return False


def addItem(character, item):
    character.inventory.append(item)
    print("itens:", character.inventory)


def is_in_inventory(character, item):
    return item in character.inventory


@dataclass
class Object:
    x: int
    y: int
    sprite: SPRITE_TYPE
    name: str


@dataclass
class Player:
    x: int
    y: int
    sprite: SPRITE_TYPE
    speed: int = 0
    atk: int = 0
    strength: int = 0
    dexterity: int = 0
    intelligence: int = 0
    direct: Sides = Sides.DOWN
    is_alive: bool = True
    vida: int = 10
    inventory: list = field(default_factory=list)


@dataclass
class Enemy:
    x: int
    y: int
    sprite: SPRITE_TYPE
    speedx: int = 0
    speedy: int = 0

    def walk(self):
        self.speedx = pyxel.rndi(-1, 1)
        self.speedy = pyxel.rndi(-1, 1)
        self.x %= pyxel.width
        self.y %= pyxel.height


@dataclass
class Projectile:
    x: int
    y: int
    sprite: SPRITE_TYPE | None = None
    sprite_list: Tuple[SPRITE_TYPE] | None = None
    speedx: int = 0
    speedy: int = 0
    duration: int = 30
    angle: int = 0


@dataclass
class Item:
    x: int
    y: int
    sprite: SPRITE_TYPE


@dataclass
class Portal:
    x: int
    y: int
    sprite: SPRITE_TYPE
    sprite_list: Tuple[SPRITE_TYPE] | None = None
