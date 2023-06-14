import logging

from typing import Callable, Generator, Tuple

import pyxel

from map_gen import map_seed
from entity import (Enemy, Player, Projectile, verifyCollision,
                    Item, player_controller, addItem)
from sprites import ATTACK, ENEMIE1, PLAYER, DOWN, Items
from hud import PlayerHUD


str_format = '%(asctime)s:%(name)s:%(levelname)s:%(message)s'
formatter = logging.Formatter(str_format)
logging.basicConfig(filename='game.log',
                    encoding='utf-8', level=logging.DEBUG, format=str_format)
log = logging.getLogger(__name__)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)
log.addHandler(ch)


class App:
    def __init__(self):
        log.debug("starting App")
        pyxel.init(160, 120)
        pyxel.load("assets/pyxel.pyxres")
        self.reset()
        pyxel.run(self.update, self.draw)

    def reset(self):
        self.entities = []
        self._trash = set()
        self.player_hud = PlayerHUD()

        self.player = Player(80, 60, PLAYER[DOWN])
        self.direction = DOWN
        self.last_spawn = 0

        map_entities = map_seed()
        self.entities += map_entities

    def spawn_enemy(self):
        log.debug("spawning enemie")
        enemy_count = len([enemy for enemy in self.filter_entities(Enemy)])
        if self.last_spawn + 10 < pyxel.frame_count and enemy_count < 10:
            self.last_spawn = pyxel.frame_count
            x = pyxel.rndi(0, pyxel.width)
            y = pyxel.rndi(0, pyxel.height)
            new_enemy = Enemy(x, y, ENEMIE1[DOWN])
            self.entities.append(new_enemy)

    def filter_entities(self, _type) -> Generator[Tuple[int, Callable], None, None]:
        return ((i, entity) for i, entity in enumerate(self.entities) if isinstance(entity, _type))

    def kill(self, entity_id) -> None:
        self._trash.add(entity_id)
        log.debug(f"entidade: {entity_id} foi movida para a lixeira")

    def entities_collision(self):
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
            for project_id, projectile in self.filter_entities(Projectile):
                if verifyCollision(enemy, projectile):
                    self.kill(entity_id)
                    item = Item(enemy.x, enemy.y, Items.blade)
                    self.entities.append(item)

        for entity_id, item in self.filter_entities(Item):
            if verifyCollision(item, self.player):
                self.kill(entity_id)
                self.player.inventory.append(item)
                log.info(f"player pegou o item: {entity_id}")

    def update(self):
        player_controller(self)
        self.entities_collision()
        self.spawn_enemy()

        trash = reversed(sorted(self._trash))
        for entity_id in trash:
            del self.entities[entity_id]
            self._trash.remove(entity_id)
            log.debug(f"entidade: {entity_id} foi deletado")

    def draw(self):
        pyxel.cls(1)
        pyxel.blt(self.player.x, self.player.y, *self.player.sprite)

        for entity in self.entities:
            if hasattr(entity, 'sprite_list'):
                frames_per_sprite = 3
                sprite_frame = pyxel.frame_count % len(
                    entity.sprite_list) * frames_per_sprite
                sprite_i = sprite_frame // frames_per_sprite
                entity.sprite = entity.sprite_list[sprite_i]
            pyxel.blt(entity.x, entity.y, *entity.sprite)

        vida_texto = "Vida: {}".format(self.player.vida)
        pyxel.text(10, 10, vida_texto, 7)

        self.player_hud.drawn(self.player)

    def attack(self):
        speedx, speedy = self.direction.value

        multi = 8
        new_speedx = speedx * multi
        new_speedy = speedy * multi

        new_x = self.player.x + new_speedx
        new_y = self.player.y + new_speedy

        attack = Projectile(new_x, new_y, ATTACK[0], ATTACK, speedx, speedy)
        self.entities.append(attack)


App()
