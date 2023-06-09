import logging
from typing import Callable, Sequence
import pyxel

from dataclasses import dataclass, field

from sprites import SPRITE_TYPE, Sides
from sprites import Efeitos


log = logging.getLogger(__name__)

def ciclone(self):
        return_list = []
        directions = Sides
        damage = self.player.atk

        for i, direction in enumerate(directions):
            dx, dy = direction.value
            distance = 8
            index = i

            new_speedx = dx * distance
            new_speedy = dy * distance

            new_x = self.player.x + new_speedx
            new_y = self.player.y + new_speedy

            attack = Projectile(
                new_x, new_y, Efeitos.CYCLONE[index], duration=1.1 ,damage=damage)
            print(attack)
            return_list.append(attack)
        return return_list

def arrow(self):
        return_list = []
        speedx, speedy = self.player.direct.value

        multi = 8
        new_speedx = speedx * multi
        new_speedy = speedy * multi

        new_x = self.player.x + new_speedx
        new_y = self.player.y + new_speedy

        damage = self.player.atk
        if self.player.direct == Sides.LEFT:
            attack = Projectile(
                new_x, new_y, Efeitos.ARROW[0], speedx=speedx, speedy=speedy, damage=damage)
        elif self.player.direct == Sides.RIGHT:
            attack = Projectile(
                new_x, new_y, Efeitos.ARROW[1], speedx=speedx, speedy=speedy, damage=damage)
        elif self.player.direct == Sides.UP:
            attack = Projectile(
                new_x, new_y, Efeitos.ARROW[3], speedx=speedx, speedy=speedy, damage=damage)
        elif self.player.direct == Sides.DOWN:
            attack = Projectile(
                new_x, new_y, Efeitos.ARROW[2], speedx=speedx, speedy=speedy, damage=damage)
        return_list.append(attack)
        return return_list

def a_button(self):
    return_list = []
    speedx, speedy = self.player.direct.value

    multi = 8
    new_speedx = speedx * multi
    new_speedy = speedy * multi

    new_x = self.player.x + new_speedx
    new_y = self.player.y + new_speedy

    damage = self.player.atk

    if self.player.direct == Sides.LEFT:
        attack = Projectile(
            new_x, new_y, Efeitos.FIREBALL[0], speedx=speedx, speedy=speedy, damage=damage)
    elif self.player.direct == Sides.RIGHT:
        attack = Projectile(
            new_x, new_y, Efeitos.FIREBALL[1], speedx=speedx, speedy=speedy, damage=damage)
    elif self.player.direct == Sides.UP:
        attack = Projectile(
            new_x, new_y, Efeitos.FIREBALL[3], speedx=speedx, speedy=speedy, damage=damage)
    elif self.player.direct == Sides.DOWN:
        attack = Projectile(
            new_x, new_y, Efeitos.FIREBALL[2], speedx=speedx, speedy=speedy, damage=damage)
    print("attack: ", attack)
    return_list.append(attack)
    return return_list


def space_button(self):
    return_list = []
    for side in Sides:
        speedx, speedy = side.value

        multi = 8
        new_speedx = speedx * multi
        new_speedy = speedy * multi

        new_x = self.player.x + new_speedx
        new_y = self.player.y + new_speedy

        damage = self.player.atk

        attack = Projectile(
            new_x, new_y, Efeitos.ATTACK[0], Efeitos.ATTACK, speedx, speedy, damage=damage)
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


def levelUp(character):
    if character.exp_atual == character.exp_para_upar or character.exp_atual > character.exp_para_upar:
        character.level += 1
        character.exp_atual = 0
        character.exp_para_upar = int(
            character.exp_progresso * character.exp_para_upar)
        log.info(f"personagem upou {character}")


def exp_walk(self, orb):
    player_x = self.player.x
    player_y = self.player.y
    object_x = orb.x
    object_y = orb.y

    distance = pyxel.sqrt((player_x - object_x) ** 2 +
                          (player_y - object_y) ** 2)

    if distance > 0:
        direction_x = (player_x - object_x) / distance
        direction_y = (player_y - object_y) / distance
        orb.x += round(direction_x)
        orb.y += round(direction_y)


def addItem(character, item):
    character.inventory.append(item)


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
    spritelist: Sequence[SPRITE_TYPE] | None = None
    speed: int = 1
    atk: int = 1
    strength: int = 0
    dexterity: int = 0
    intelligence: int = 0
    direct: Sides = Sides.DOWN
    is_alive: bool = True
    vida: int = 10
    inventory: list = field(default_factory=list)
    level: int = 1
    exp_atual: int = 0
    exp_para_upar: int = 10
    exp_rate: int = 1
    exp_progresso: float = 3.14
    skill_1: Callable = None


@dataclass
class Enemy:
    x: int
    y: int
    sprite: SPRITE_TYPE
    sprite_list: Sequence[SPRITE_TYPE] | None = None
    speedx: float = 0
    speedy: float = 0
    exp: int = 1
    vida: int = 10

    def walk(self):
        self.speedx = pyxel.sin(pyxel.frame_count % 360)
        self.speedy = pyxel.cos(pyxel.frame_count % 360)
        self.x %= pyxel.width
        self.y %= pyxel.height


@dataclass
class Projectile:
    x: int
    y: int
    sprite: SPRITE_TYPE | None = None
    sprite_list: Sequence[SPRITE_TYPE] | None = None
    speedx: int = 0
    speedy: int = 0
    duration: int = 30
    angle: int = 0
    damage: int = 0


@dataclass
class Item:
    x: int
    y: int
    sprite: SPRITE_TYPE
    sprite_list: Sequence[SPRITE_TYPE] | None = None
    exp: int = 0


@dataclass
class Portal:
    x: int
    y: int
    sprite: SPRITE_TYPE
    sprite_list: Sequence[SPRITE_TYPE] | None = None
