import pyxel 

from typing import Tuple, List
from dataclasses import dataclass, field

SPRITEDOWN = 0, 0, 0, 8, 8, 0
SPRITEUP = 0, 8, 0, 8, 8, 0
SPRITELEFT = 0, 0, 8, 8, 8, 0
SPRITERIGHT = 0, 8, 8, 8, 8, 0

ENEMIE_1_DOWN = 0, 24, 0, 8, 8, 0
ENEMIE_1_UP = 0, 0, 0, 8, 8, 0
ENEMIE_1_LEFT = 0, 0, 0, 8, 8, 0
ENEMIE_1_RIGHT = 0, 0, 0, 8, 8, 0

HOUSE = 0, 32, 0, 16, 16, 0
CARAMBA = 0, 0, 16, 8, 8, 0

GRASS = 1, 32, 0, 8, 8, 1
TREE = 1, 40, 0, 8, 8, 1


@dataclass
class Entity:
    name: str
    x: int
    y: int
    sprite: Tuple[int, int, int, int, int, int]
    attrs: dict = field(default_factory=dict)

def casa(x, y):
    return Entity("casa", x, y, HOUSE)

def proximos(entities, x, y, distance=10, type=None) -> int:
    if type:
        entities = [entity for entity in entities if entity.name == type]
    proximos = [entity for entity in entities if abs(entity.x - x) < distance and abs(entity.y - y) < distance]
    return len(proximos)

def map_seed(width, height) -> List[Entity]:
    map_list = [[ 0 for _ in range(width)] for _ in range(height)]
    entities = []
    for y in range(pyxel.height):
        for x in range(pyxel.width):
            n = pyxel.noise(x/20, y/20, 0)
            if n > 0.7:
                map_list[y][x] = 8
                if not proximos(entities, x, y, 15, "casa"):
                    entities.append(casa(x,y))
            elif n > 0.4:
                if not proximos(entities, x, y, 15, "tree"):
                    entities.append(Entity("tree", x, y, TREE))
                map_list[y][x] = 2
            elif n > 0.2:
                map_list[y][x] = 3
            elif n > 0:
                map_list[y][x] = 4
            elif n > -0.3:
                map_list[y][x] = 5
            elif n > -0.7:
                map_list[y][x] = 6
            else:
                map_list[y][x] = 0


            # pyxel.pset(x, y, map_list[y][x])
    return entities




def random_walk(character):
    character.x = (character.x - pyxel.rndi(-1, 1)) % pyxel.width
    character.y = (character.y - pyxel.rndi(-1, 1)) % pyxel.height



class Player:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.sprite = SPRITEDOWN

class App:
    def __init__(self):
        self.player = Entity("Player", 0, 0, SPRITEDOWN)
        self.entities = []

        self.entities.append(Entity("inimigo", 10, 10, ENEMIE_1_DOWN))

        pyxel.init(160, 120)
        pyxel.load("assets/pyxel.pyxres")
        more_entities = map_seed(pyxel.width, pyxel.height)
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
        map_seed(pyxel.width, pyxel.height)
        pyxel.blt(self.player.x, self.player.y, *self.player.sprite)
        
        for entity in self.entities:
            pyxel.blt(entity.x, entity.y, *entity.sprite)

        pyxel.text(10, 10, "map_gen", 3)
        

App()
