from enum import Enum
import pyxel
from typing import Dict
from engine.entities import Player, Enemy, Projectile


class Sides(Enum):
    LEFT = -1, 0
    DOWN_LEFT = -1, 1
    DOWN = 0, 1
    DOWN_RIGHT = 1, 1
    RIGHT = 1, 0
    UP_RIGHT = 1, -1
    UP = 0, -1
    UP_LEFT = -1, -1


LEFT = Sides.LEFT
RIGHT = Sides.RIGHT
UP = Sides.UP
DOWN = Sides.DOWN

FIREBALL = (
    (2, 8, 16, 5, 8, 7),
)
MAGE = {
    LEFT: ((0, 16, 0, -8, 8, 7), ),
    RIGHT: ((0, 16, 0, 8, 8, 7), ),
    UP: ((0, 16, 0, 8, 8, 7), ),
    DOWN: ((0, 16, 0, 8, 8, 7), ),
}
ENEMIE1 = {
    LEFT: ((0, 0, 0, 8, 8, 7),),
    RIGHT: ((0, 0, 0, 8, 8, 7),),
    UP: ((0, 0, 0, 8, 8, 7),),
    DOWN: ((0, 24, 0, 8, 8, 7),),
}


class Game:
    def __init__(self):
        pyxel.init(180, 140)
        pyxel.load('assets/pyxel.pyxres')
        self.start()
        pyxel.run(self.update, self.draw)

    def start(self):
        self.entities: Dict[type, list] = {}
        self.add(
            Player(x=50, y=50, states=MAGE, current_state=DOWN),
            Enemy(speed=1, angle=45, states=ENEMIE1, current_state=DOWN)
        )

    def add(self, *entities):
        for entity in entities:
            if not self.entities.get(type(entity)):
                self.entities[type(entity)] = []
            self.entities[type(entity)].append(entity)

    def remove(self, *entities):
        for entity in entities:
            if entity in self.entities[type(entity)]:
                self.entities[type(entity)].remove(entity)

    def controller(self):
        player: Player = self.entities[Player][0]
        if pyxel.btn(pyxel.KEY_LEFT):
            player.current_state = LEFT
            player.x -= 1
        if pyxel.btn(pyxel.KEY_RIGHT):
            player.current_state = RIGHT
            player.x += 1
        if pyxel.btn(pyxel.KEY_DOWN):
            player.y += 1
        if pyxel.btn(pyxel.KEY_UP):
            player.y -= 1
        if pyxel.btnp(pyxel.KEY_SPACE):
            player.skill_1(self.add)
        if pyxel.btnp(pyxel.KEY_A):
            player.skill_2(self.add)

    def update(self):
        self.controller()

        if len(self.entities[Enemy]) <= 10:
            self.add(
                Enemy(
                    states=ENEMIE1,
                    current_state=DOWN,
                    x=pyxel.rndi(0, pyxel.width),
                    y=pyxel.rndi(0, pyxel.width),
                    angle=45, speed=1
                )
            )

        for entity_list in self.entities.values():
            for entity in entity_list:
                entity.move()

                match entity:
                    case Projectile():
                        for enemy in self.entities[Enemy]:
                            if entity.collide_with_target(enemy):
                                self.remove(entity)
                                entity.attack(
                                    enemy, kill_func=self.remove)
                                self.remove(entity)
                        for player in self.entities[Player]:
                            if entity.collide_with_target(player):
                                entity.attack(player)
                                self.remove(entity)
                    case Enemy():
                        entity.angle += 5

    def draw(self):
        pyxel.cls(0)
        for entity_list in self.entities.values():
            for entity in entity_list:
                entity.render()


Game()
