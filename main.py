from dataclasses import dataclass
from math import atan2, cos, degrees, pi, radians, sin, sqrt
from typing import Any, Dict, Optional, Sequence
from sprites import ARCHER, DOWN, FIREBALL, MAGE, RIGHT, WARRIOR, UPATTACK, Sides
from System import *

import esper
import pyxel


class App:
    def __init__(self) -> None:
        pyxel.init(220, 180)
        pyxel.load("assets/pyxel.pyxres")
        # pyxel.playm(0, loop=True)

        self.world = esper.World()
        self.world.add_processor(MovementSystem())
        self.world.add_processor(EnemySpawner())
        self.world.add_processor(HUD())
        self.world.add_processor(TimerSystem())
        self.world.add_processor(KeyboardInputProcessor())
        self.world.add_processor(CollissionSystem())
        self.world.add_processor(RenderSystem())
        self.world.add_processor(SpriteSystem())

        self.world.create_entity(
            Sprite(
                states=MAGE,
                current_state=DOWN
            ),
            Pos(
                x=pyxel.width//2,
                y=pyxel.height//2,
            ),
            PlayerComponent(),
            Combat(hp=5, max_hp=5, damage=1)
        )


        pyxel.run(self.update, self.draw)

    def update(self):
        return

    def draw(self):
        pyxel.cls(1)
        self.world.process()


App()
