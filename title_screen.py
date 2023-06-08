import pyxel 

from typing import Tuple
from pyxel import *

from dataclasses import dataclass

SPRITEDOWN = 0, 0, 0, 8, 8, 0
SPRITEUP = 0, 8, 0, 8, 8, 0
SPRITELEFT = 0, 0, 8, 8, 8, 0
SPRITERIGHT = 0, 8, 8, 8, 8, 0

ENEMIE_1_DOWN = 0, 24, 0, 8, 8, 0
ENEMIE_1_UP = 0, 0, 0, 8, 8, 0
ENEMIE_1_LEFT = 0, 0, 0, 8, 8, 0
ENEMIE_1_RIGHT = 0, 0, 0, 8, 8, 0

HOUSE = 0, 32, 0, 16, 16, 0


def random_walk(character):
    character.x = (character.x - rndi(-1, 1)) % pyxel.width
    character.y = (character.y - rndi(-1, 1)) % pyxel.height


@dataclass
class Enemie:
    name: str
    x: int
    y: int
    sprite: Tuple[int, int, int, int, int, int]

class Player:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.sprite = SPRITEDOWN

class App:
    def __init__(self):
        self.player = Enemie("Player", 0, 0, SPRITEDOWN)
        self.enemies = []

        self.enemies.append(Enemie("inimigo", 10, 10, ENEMIE_1_DOWN))
        self.enemies.append(Enemie("objeto", 50, 50, HOUSE))

        init(160, 120)
        load("assets/pyxel.pyxres")
        run(self.update, self.draw)

    def update(self):
        if btn(KEY_LEFT):
            self.player.x = (self.player.x - 1) % width
            self.player.sprite = SPRITELEFT
        if btn(KEY_RIGHT):
            self.player.x = (self.player.x + 1) % width
            self.player.sprite = SPRITERIGHT
        if btn(KEY_DOWN):
            self.player.y = (self.player.y + 1) % height
            self.player.sprite = SPRITEDOWN
        if btn(KEY_UP):
            self.player.y = (self.player.y - 1) % height
            self.player.sprite = SPRITEUP

        for enemie in self.enemies:
            if enemie.name == "inimigo":
                random_walk(enemie)

    def draw(self):
        cls(0)
        blt(self.player.x, self.player.y, *self.player.sprite)
        
        for enemie in self.enemies:
            blt(enemie.x, enemie.y, *enemie.sprite)

        text(10, 10, "titulo", 3)
        

App()
