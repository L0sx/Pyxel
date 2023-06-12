import pyxel

from dataclasses import dataclass

from sprites import SPRITE_TYPE, Sides


def verifyCollision(objeto1, objeto2):
        if (objeto1.x < objeto2.x + objeto2.sprite[3] and
                objeto1.x + objeto1.sprite[3] > objeto2.x and
                objeto1.y < objeto2.y + objeto2.sprite[4] and
                objeto1.y + objeto1.sprite[4] > objeto2.y):
            return True
        else:
            return False

def changeSprite(character):
     if character.name == "Attack":
          if character.sprite != "SPRITEATTACK4":
               print(character.sprite)

def random_walk(character):
    character.x = (character.x - pyxel.rndi(-1, 1)) % pyxel.width
    character.y = (character.y - pyxel.rndi(-1, 1)) % pyxel.width


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


@dataclass
class Projectile:
    x: int
    y: int
    sprite: SPRITE_TYPE
    speedx: int = 0
    speedy: int = 0
    duration: int = 30
    angle: int = 0

