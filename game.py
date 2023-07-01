import pyxel
from typing import Dict
from entities import Enemy2, Player, Enemy, Projectile, HUD
from sprites import ARCHER, ENEMY2, MAGE, LEFT, RIGHT, UP, DOWN, WARRIOR


class Game:
    def __init__(self):
        pyxel.init(180, 140)
        pyxel.load('assets/pyxel.pyxres')
        self.over = False
        self.start()
        pyxel.run(self.update, self.draw)

    def start(self):
        self.entities: Dict[type, list] = {}
        player = Player(x=50, y=50, states=MAGE, current_state=DOWN)
        self.add(
            player,
            HUD(player),
            Enemy(speed=1, angle=45, states=WARRIOR, current_state=DOWN),
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
        if pyxel.btnp(pyxel.KEY_A):
            player.skill_1(self)
        if pyxel.btnp(pyxel.KEY_SPACE):
            player.skill_2(self)
        if pyxel.btnp(pyxel.KEY_Q):
            player.hp = player.max_hp
            self.over = False

    def update(self):
        self.controller()
        player = self.get(Player)[0]

        if player.hp <= 0:
            self.over = True
            return

        n_enemies = len(self.get(Enemy)) + len(self.get(Enemy2))
        if n_enemies <= 10:
            if not pyxel.frame_count % 15:
                self.add(
                    Enemy(
                        states=ENEMY2,
                        current_state=DOWN,
                        x=pyxel.rndi(0, pyxel.width),
                        y=pyxel.rndi(0, pyxel.width),
                        angle=45, speed=1
                    )
                )

            if not pyxel.frame_count % 3:
                self.add(
                    Enemy2(
                        states=ARCHER,
                        current_state=DOWN,
                        x=pyxel.rndi(0, pyxel.width),
                        y=pyxel.rndi(0, pyxel.width),
                        angle=45, speed=1
                    )
                )

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
                                player.exp += enemy.exp
                        for player in self.get(Player):
                            if entity.collide_with_target(player):
                                self.remove(entity)
                                entity.attack(player)
                    case Enemy():
                        pass

    def draw(self):
        pyxel.cls(0)
        for entity_type in set(self.entities.keys()):
            for entity in self.get(entity_type):
                entity.draw()

        if self.over:
            pyxel.text(pyxel.width//2, pyxel.height//2,
                       "GAME OVER!", pyxel.frame_count % 15)


Game()
