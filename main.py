import pyxel

from map_gen import map_seed
from entity import Entity



COLKEY = 1

SPRITEDOWN = 0, 0, 0, 8, 8, COLKEY
SPRITEUP = 0, 8, 0, 8, 8, COLKEY
SPRITELEFT = 0, 0, 8, 8, 8, COLKEY
SPRITERIGHT = 0, 8, 8, 8, 8, COLKEY

ENEMIE_1_DOWN = 0, 24, 0, 8, 8, COLKEY
ENEMIE_1_UP = 0, 0, 0, 8, 8, COLKEY
ENEMIE_1_LEFT = 0, 0, 0, 8, 8, COLKEY
ENEMIE_1_RIGHT = 0, 0, 0, 8, 8, COLKEY

HOUSE = 0, 32, 0, 16, 16, COLKEY
CARAMBA = 0, 0, 16, 8, 8, COLKEY

GRASS = 1, 32, 0, 8, 8, COLKEY
TREE = 1, 40, 0, 8, 8, COLKEY


def random_walk(character):
    character.x = (character.x - pyxel.rndi(-1, 1)) % pyxel.width
    character.y = (character.y - pyxel.rndi(-1, 1)) % pyxel.width




class App:
    def __init__(self):
        self.player = Entity("Player", 0, 0, SPRITEDOWN)
        self.entities = []

        self.entities.append(Entity("inimigo", 10, 10, ENEMIE_1_DOWN))

        pyxel.init(160, 120)
        pyxel.load("assets/pyxel.pyxres")
        more_entities = map_seed()
        self.entities += more_entities
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

        for entity in self.entities:
            if entity.name == "inimigo":
                random_walk(entity)

    def draw(self):
        pyxel.cls(1)
        pyxel.blt(self.player.x, self.player.y, *self.player.sprite)
        
        for entity in self.entities:
            pyxel.blt(entity.x, entity.y, *entity.sprite)

        pyxel.text(10, 10, "map_gen", 3)
        

App()
