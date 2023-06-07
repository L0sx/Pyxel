import pyxel

from dataclasses import dataclass

SPRITEDOWN = 0, 0, 0, 8, 8, 0
SPRITEUP = 0, 8, 0, 8, 8, 0
SPRITELEFT = 0, 0, 8, 8, 8, 0
SPRITERIGHT = 0, 8, 8, 8, 8, 0


def random_walk(character):
    character.x = (character.x - pyxel.rndi(-1, 1)) % pyxel.width
    character.y = (character.y - pyxel.rndi(-1, 1)) % pyxel.width


@dataclass
class Enemie:
    name: str
    x: int
    y: int
    sprite: int

class Player:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.sprite = SPRITEDOWN

class App:
    def __init__(self):
        self.player = Enemie("Player", 0, 0, SPRITEDOWN)
        self.enemies = []

        self.enemies.append(Enemie("inimigo", 10, 10, SPRITELEFT))

        pyxel.init(160, 120)
        pyxel.load("assets/pyxel.pyxres")
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btn(pyxel.KEY_LEFT):
            self.player.x = (self.player.x - 1) % pyxel.width
            self.player.sprite = SPRITELEFT
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.player.x = (self.player.x + 1) % pyxel.width
            self.player.sprite = SPRITERIGHT
        if pyxel.btn(pyxel.KEY_DOWN):
            self.player.y = (self.player.y + 1) % pyxel.height
            self.player.sprite = SPRITEDOWN
        if pyxel.btn(pyxel.KEY_UP):
            self.player.y = (self.player.y - 1) % pyxel.height
            self.player.sprite = SPRITEUP

        for enemie in self.enemies:
            random_walk(enemie)

    def draw(self):
        pyxel.cls(0)
        pyxel.blt(self.player.x, self.player.y, *self.player.sprite)
        
        for enemie in self.enemies:
            pyxel.blt(enemie.x, enemie.y, *enemie.sprite)
        

App()
