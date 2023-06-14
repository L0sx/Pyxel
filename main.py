from typing import Callable, Generator, Tuple
import pyxel

from map_gen import map_seed
from entity import (Enemy, Player, Projectile, verifyCollision,
                    Item, player_controller, addItem)
from sprites import ATTACK, ENEMIE1, PLAYER, DOWN, Items


class PlayerHUD:
    def __init__(self) -> None:
        self.height = 10

    def drawn(self, player):
        start_h = pyxel.height - self.height
        half_height = self.height/2

        pyxel.tri(0, start_h-10, 0, pyxel.height,
                  self.height+10, pyxel.height, 13)
        pyxel.circ(0+half_height, start_h + half_height, half_height, 8)
        pyxel.rect(0, start_h, self.height+1, (10-player.vida) % 10, 13)

        pyxel.text(self.height, start_h, f"{player.vida}", 7)

        pyxel.circ(pyxel.width-half_height, start_h +
                   half_height + 3, half_height, 6)

        for i, item in enumerate(player.inventory):
            x = 20 + i * 11
            y = start_h
            pyxel.rect(x-1, y-1, 10, 10, 13)
            pyxel.blt(x, y, *item.sprite)


class App:
    def __init__(self):
        pyxel.init(160, 120)
        pyxel.load("assets/pyxel.pyxres")
        self. restart()
        pyxel.run(self.update, self.draw)

    def restart(self):
        self.entities = []
        self._trash = set()
        self.player_hud = PlayerHUD()

        self.player = Player(80, 60, PLAYER[DOWN])
        self.direction = DOWN
        self.last_spawn = 0

        map_entities = map_seed()
        self.entities += map_entities

    def spawn_enemy(self):
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

    def update(self):
        player_controller(self)
        self.entities_collision()

        self.spawn_enemy()

        trash = reversed(sorted(self._trash))
        for entity_id in trash:
            del self.entities[entity_id]
            self._trash.remove(entity_id)

            for item_id, item in self.filter_entities(Item):
                if verifyCollision(item, self.player):
                    self.kill(item_id)
                    addItem(self.player, item)

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
