from typing import Callable, Generator, Tuple
import pyxel

from map_gen import map_seed
from entity import Enemy, Player, Projectile, verifyCollision
from sprites import ATTACK, ENEMIE1, PLAYER, LEFT, RIGHT, UP, DOWN




class App:
    def __init__(self):
        self.player = Player(80, 60, PLAYER[DOWN])
        self.entities = []
        self._trash = set()

        self.direction = DOWN

        test_enemy = Enemy(10, 10, ENEMIE1[DOWN])
        self.entities.append(test_enemy)

        pyxel.init(160, 120)
        pyxel.load("assets/pyxel.pyxres")
        map_entities = map_seed()
        self.entities += map_entities

        pyxel.run(self.update, self.draw)

    def filter_entities(self, _type) -> Generator[Tuple[int, Callable], None, None]:
        return ((i ,entity) for i, entity in enumerate(self.entities) if isinstance(entity, _type))

    def kill(self, entity_id) -> None:
        self._trash.add(entity_id)

    def update(self):
        if pyxel.btn(pyxel.KEY_LEFT):
            self.player.x = (self.player.x - 1) % pyxel.width
            self.player.sprite = PLAYER[LEFT]
            self.direction = LEFT
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.player.x = (self.player.x + 1) % pyxel.width
            self.player.sprite = PLAYER[RIGHT]
            self.direction = RIGHT
        if pyxel.btn(pyxel.KEY_DOWN):
            self.player.y = (self.player.y + 1) % pyxel.height
            self.player.sprite = PLAYER[DOWN]
            self.direction = DOWN
        if pyxel.btn(pyxel.KEY_UP):
            self.player.y = (self.player.y - 1) % pyxel.height
            self.player.sprite = PLAYER[UP]
            self.direction = UP
        if pyxel.btnp(pyxel.KEY_A):
            self.attack()

        for entity_id, projectile in self.filter_entities(Projectile):
            projectile.duration -= 1
            projectile.x += projectile.speedx
            projectile.y += projectile.speedy
            if projectile.duration <= 0:
                self.kill(entity_id)

        for entity_id, enemy in self.filter_entities(Enemy):
            enemy.x += enemy.speedx
            enemy.y += enemy.speedy
            enemy.walk()
            if verifyCollision(self.player, enemy):
                if self.player.x < enemy.x:
                    self.player.vida -= 1
                    self.player.x -= 5
                    enemy.x += 5
                else:
                    self.player.vida -= 1
                    self.player.x += 5
                    enemy.x -= 5

        trash = reversed(sorted(self._trash))
        for entity_id in trash:
            del self.entities[entity_id]
            self._trash.remove(entity_id)

    def draw(self):
        pyxel.cls(1)
        pyxel.blt(self.player.x, self.player.y, *self.player.sprite)
        
        for entity in self.entities:
            pyxel.blt(entity.x, entity.y, *entity.sprite)

        vida_texto = "Vida: {}".format(self.player.vida)
        pyxel.text(10, 10, vida_texto, 7)

    def attack(self):
        speedx, speedy = self.direction.value

        attack = Projectile(self.player.x, self.player.y, ATTACK[0], speedx, speedy) 
        self.entities.append(attack)

App()
