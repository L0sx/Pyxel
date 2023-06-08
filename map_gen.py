import pyxel 

from typing import Tuple, List
from dataclasses import dataclass, field

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

HOUSE = 1, 0, 0, 16, 16, 0
CARAMBA = 0, 0, 16, 8, 8, COLKEY

GRASS = 1, 32, 0, 8, 8, COLKEY
TREE = 1, 40, 0, 8, 8, COLKEY

def proximos(entities, x, y, distance=10, type=None) -> int:
    if type:
        entities = [entity for entity in entities if entity.name == type]
    proximos = [entity for entity in entities if abs(entity.x - x) < distance and abs(entity.y - y) < distance]
    return len(proximos)

def map_seed() -> List[Entity]:
    entities = []
    for y in range(pyxel.height):
        for x in range(pyxel.width):
            n = pyxel.noise(x/20, y/20, 0)
            if n > 0.7:
                point_val = 1
                if not proximos(entities, x, y, 15, "tree"):
                    entities.append(Entity("tree", x, y, TREE))
            elif n > 0.4:
                if not proximos(entities, x, y, 15, "grass"):
                    entities.append(Entity("grass", x, y, GRASS))
                    pass
                point_val = 2
            elif n > 0.2:
                point_val = 3
            elif n > 0:
                point_val = 4
            elif n > -0.3:
                point_val = 5
            elif n > -0.7:
                point_val = 6
            else:
                point_val = 0

            pyxel.pset(x, y, point_val)
    return entities
