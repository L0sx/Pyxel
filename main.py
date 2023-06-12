import pyxel
import math

from map_gen import map_seed
from entity import Entity



COLKEY = 1

SPRITEATTACK1 = 2, 0, 0, 8, 8, 0
SPRITEATTACK2 = 2, 8, 0, 8, 8, 0
SPRITEATTACK3 = 2, 0, 8, 8, 8, 0
SPRITEATTACK4 = 2, 8, 8, 8, 8, 0

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

def attack_walk(character):
        for i in range(character.repeat):
            if character.direct == "left":
                character.x = character.x - 1
            if i == 3:
                return True
        

def verifyCollision(objeto1, objeto2):
        if (objeto1.x < objeto2.x + objeto2.sprite[3] and
                objeto1.x + objeto1.sprite[3] > objeto2.x and
                objeto1.y < objeto2.y + objeto2.sprite[4] and
                objeto1.y + objeto1.sprite[4] > objeto2.y):
            return True
        else:
            return False



class App:
    def __init__(self):
        self.player = Entity("Player", 80, 60, SPRITEDOWN)
        self.entities = []
        self.vida = 10
        self.entities.append(Entity("inimigo", 10, 10, ENEMIE_1_DOWN))
        self.last_key_pressed = None

        pyxel.init(160, 120)
        pyxel.load("assets/pyxel.pyxres")
        more_entities = map_seed()
        self.entities += more_entities
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btn(pyxel.KEY_LEFT):
            self.player.x = (self.player.x - 1) % pyxel.width
            self.player.sprite = SPRITELEFT
            self.last_key_pressed = "left"
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.player.x = (self.player.x + 1) % pyxel.width
            self.player.sprite = SPRITERIGHT
            self.last_key_pressed = "right"
        if pyxel.btn(pyxel.KEY_DOWN):
            self.player.y = (self.player.y + 1) % pyxel.height
            self.player.sprite = SPRITEDOWN
            self.last_key_pressed = "down"
        if pyxel.btn(pyxel.KEY_UP):
            self.player.y = (self.player.y - 1) % pyxel.height
            self.player.sprite = SPRITEUP
            self.last_key_pressed = "up"
        if pyxel.btnp(pyxel.KEY_A):
            self.attack()

        for entity in self.entities:
            if entity.name == "inimigo":
                random_walk(entity)
            if entity.name == "attack" and entity.is_alive:
                    if entity.repeat > 0:
                        entity.repeat -= 1
                        if entity.direct == "left":
                            entity.x -= 1
                        elif entity.direct == "right":
                            entity.x += 1
                        elif entity.direct == "up":
                            entity.y -= 1
                        elif entity.direct == "down":
                            entity.y += 1
                    else: Entity.die(entity)
                    

        
        for entity in self.entities:
            if entity.name == "inimigo" and verifyCollision(self.player, entity):
                if self.player.x < entity.x:
                    self.vida -= 1
                    self.player.x -= 5
                    entity.x += 5
                else:
                    self.vida -= 1
                    self.player.x += 5
                    entity.x -= 5
                    

    def draw(self):
        pyxel.cls(1)
        pyxel.blt(self.player.x, self.player.y, *self.player.sprite)
        
        for entity in self.entities:
            pyxel.blt(entity.x, entity.y, *entity.sprite)

        vida_texto = "Vida: {}".format(self.vida)
        pyxel.text(10, 10, vida_texto, 7)

    def attack(self):
        self.entities.append(Entity("attack", self.player.x, self.player.y, SPRITEATTACK1, repeat= 10, direct=self.last_key_pressed))

App()
