from dataclasses import dataclass
import pyxel
from typing import Dict
from entities import Optional, Player, Enemy, Projectile
from engine.components import FloatingText
from sprites import MAGE, LEFT, RIGHT, UP, DOWN, WARRIOR


@dataclass
class HUD:
    player: Player

    def draw(self):
        xlife = self.player.x
        ylife = self.player.y - 4
        tamanhoLife = self.player.w
        exp = 99
        exp_atual = exp if exp else 1
        exp_total = 100
        percenteExp = (exp_atual / exp_total)
        percenteLife = (self.player.hp / self.player.max_hp)
        tamanhoBarra = pyxel.width - 20

        pyxel.circ(10, 10, self.player.w, 7)
        pyxel.circb(10, 10, self.player.w, 10)

        pyxel.rect(10, 10, tamanhoBarra * percenteExp, 4, 3)
        pyxel.rectb(10, 10, tamanhoBarra, 4, 7)

        pyxel.rect(xlife, ylife, tamanhoLife * percenteLife, 1, 8)


class Game:
    def __init__(self):
        pyxel.init(180, 140)
        pyxel.load('assets/pyxel.pyxres')
        self.start()
        pyxel.run(self.update, self.draw)

    def start(self):
        self.entities: Dict[type, list] = {}
        player = Player(x=50, y=50, states=MAGE, current_state=DOWN)
        self.add(
            player,
            HUD(player),
            Enemy(speed=1, angle=45, states=WARRIOR, current_state=DOWN),
            FloatingText(text="55", x=50, y=50)
        )

    def get(self, entity_type):
        entity_list = self.entities.get(entity_type, []).copy()
        return entity_list

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
        player: Player = self.get(Player)[0]
        if pyxel.btn(pyxel.KEY_LEFT):
            player.current_state = LEFT
            player.x -= 1
        if pyxel.btn(pyxel.KEY_RIGHT):
            player.current_state = RIGHT
            player.x += 1
        if pyxel.btn(pyxel.KEY_DOWN):
            player.current_state = DOWN
            player.y += 1
        if pyxel.btn(pyxel.KEY_UP):
            player.current_state = UP
            player.y -= 1
        if pyxel.btnp(pyxel.KEY_SPACE):
            player.skill_1(self)
        if pyxel.btnp(pyxel.KEY_A):
            player.skill_2(self)

    def update(self):
        self.controller()

        if len(self.entities[Enemy]) <= 10:
            self.add(
                Enemy(
                    states=WARRIOR,
                    current_state=DOWN,
                    x=pyxel.rndi(0, pyxel.width),
                    y=pyxel.rndi(0, pyxel.width),
                    angle=45, speed=1
                )
            )

        for entity_type in set(self.entities.keys()):
            for entity in self.get(entity_type):
                if hasattr(entity, "update"):
                    entity.update(self)

                match entity:
                    case Projectile():
                        for enemy in self.get(Enemy):
                            if entity.collide_with_target(enemy):
                                self.remove(entity)
                                entity.attack(enemy, game=self)
                        for player in self.get(Player):
                            if entity.collide_with_target(player):
                                self.remove(entity)
                                entity.attack(player, game=self)
                    case Enemy():
                        entity.angle += 5

    def draw(self):
        pyxel.cls(0)
        for entity_type in set(self.entities.keys()):
            for entity in self.get(entity_type):
                entity.draw()


Game()
