import pyxel

from typing import List

from entity import Object
from sprites import Objetos


def proximos(entities, x, y, distance=10, name=None) -> int:
    if name:
        entities = [entity for entity in entities if name == entity.name]
    proximos = [entity for entity in entities if abs(
        entity.x - x) < distance and abs(entity.y - y) < distance]
    return len(proximos)


def map_seed() -> List[Object]:
    entities = []
    for y in range(pyxel.height):
        for x in range(pyxel.width):
            n = pyxel.noise(x/20, y/20, pyxel.frame_count)
            if n > 0.7:
                point_val = 1
                if not proximos(entities, x, y, 15, "tree"):
                    tree = Object(x, y, Objetos.TREE, "tree")
                    entities.append(tree)
            elif n > 0.4:
                if not proximos(entities, x, y, 15, "grass"):
                    grass = Object(x, y, Objetos.GRASS, "grass")
                    entities.append(grass)
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
