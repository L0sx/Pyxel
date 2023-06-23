import pyxel
import logging

from typing import List

from entity import Object
from sprites import Objetos, Ground, Colors


log = logging.getLogger(__name__)


GRASSES = [
    Ground.GRASS1,
    Ground.GRASS2,
    Ground.GRASS3,
    Ground.GRASS4,
]
WATERS = [
    Ground.WATER1,
    Ground.WATER2,
    Ground.WATER3,
    Ground.WATER4,
]


def proximos(entities, x, y, distance=10, name=None) -> int:
    if name:
        entities = [entity for entity in entities if name == entity.name]
    proximos = [entity for entity in entities if abs(
        entity.x - x) < distance and abs(entity.y - y) < distance]
    return len(proximos)


def map_seed() -> List[Object]:
    entities = []
    for y in range(pyxel.height * 3):
        for x in range(pyxel.width * 3):
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


class MapGenScreen:
    name = "Test Screen"

    def __init__(self):
        pyxel.init(160, 120)
        pyxel.load("assets/pyxel.pyxres")
        self.start()
        pyxel.run(self.draw, self.update)

    def start(self):
        self.entities = []
        self._trash = set()
        self.bg_color = 1
        self.portal = False
        self.entities += map_seed()
        self.camera = [0, 0]
        self.xdiv = 5
        self.ydiv = 5
        self.zdiv = 1

    def controller(self):
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
            self.xdiv = max(1, self.xdiv - 1)
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
            self.xdiv = max(1, self.xdiv + 1)
        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
            self.ydiv = max(1, self.ydiv + 1)
        if pyxel.btn(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
            self.ydiv = max(1, self.ydiv - 1)
        if pyxel.btn(pyxel.KEY_SPACE):
            self.zdiv += 1

    def update(self):
        self.controller()

    def draw(self):
        pyxel.camera(*self.camera)
        pyxel.cls(1)
        tilesize = 8
        for y in range(pyxel.height//tilesize):
            for x in range(pyxel.width//tilesize):
                n = pyxel.noise(x/self.xdiv, y/self.ydiv, self.zdiv/40)
                if n > 0.5:
                    tile = WATERS[(x+y) % len(WATERS)]
                    point_val = Colors.BLUE1
                elif n > 0.2:
                    point_val = Colors.BLUE2
                    tile = GRASSES[(x+y) % len(GRASSES)]
                elif n > -0.5:
                    point_val = Colors.BLUE3
                    tile = GRASSES[(x+y) % len(GRASSES)]
                else:
                    point_val = Colors.BLUE4
                    tile = GRASSES[(x+y) % len(GRASSES)]

                pyxel.blt(x*tilesize, y*tilesize, *tile)
                pyxel.pset(x*tilesize, y*tilesize, point_val)

        tcolor = Colors.WHITE
        pyxel.rect(10, 10, 100, 15, Colors.BLACK)
        pyxel.text(10, 10, f"{self.xdiv=}", tcolor)
        pyxel.text(10, 15, f"{self.ydiv=}", tcolor)
        pyxel.text(10, 20, f"{self.zdiv=}", tcolor)


if __name__ == "__main__":
    screen = MapGenScreen()
