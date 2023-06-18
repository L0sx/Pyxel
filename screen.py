import logging
import pyxel
from typing import Callable, Generator, Tuple
from map_gen import map_seed
from entity import (Enemy, Player, Portal, Projectile, verifyCollision,
                    Item, player_controller, levelUp, exp_walk)
from sprites import DOWN
from sprites import Inimigos, Personagens, Objetos, Efeitos
from hud import PlayerHUD

log = logging.getLogger(__name__)


COLKEY = 1

SPRITEDOWN = 0, 0, 0, 8, 8, COLKEY
SPRITEUP = 0, 8, 0, 8, 8, COLKEY
SPRITELEFT = 0, 0, 8, 8, 8, COLKEY
SPRITERIGHT = 0, 8, 8, 8, 8, COLKEY

ENEMIE_1_DOWN = 0, 24, 0, 8, 8, COLKEY
ENEMIE_1_UP = 0, 0, 0, 8, 8, COLKEY
ENEMIE_1_LEFT = 0, 0, 0, 8, 8, COLKEY
ENEMIE_1_RIGHT = 0, 0, 0, 8, 8, COLKEY

HOUSE = 0, 32, 0, 16, 16, COLKEY
CARAMBA = 0, 0, 16, 8, 8, COLKEY

GRASS = 1, 32, 0, 8, 8, COLKEY
TREE = 1, 40, 0, 8, 8, COLKEY


def center_x_text(y, text, colkey=9, bg=None):
    x = pyxel.width / 2 - len(text) * 2

    if bg:
        pyxel.rect(x-1, y-1, len(text) * 4 + 2, 5 + 2, bg)

    pyxel.text(x, y, text, colkey)


def title_controller(self):
    if pyxel.btnp(pyxel.KEY_LEFT):
        pass
    if pyxel.btnp(pyxel.KEY_RIGHT):
        pass
    if pyxel.btnp(pyxel.KEY_DOWN):
        self.current_option = (self.current_option +
                               1) % len(self.menu_options)
    if pyxel.btnp(pyxel.KEY_UP):
        self.current_option = (self.current_option -
                               1) % len(self.menu_options)
    if pyxel.btnp(pyxel.KEY_RETURN):
        if self.current_option == 0:
            self.app.switch_screen(self.app.game_screen)


class TitleScreen:
    def __init__(self, app):
        self.app = app
        self.menu_options = [
            "start",
            "configs",
            "credits"
        ]
        self.current_option = 0

    def center_x_text(self, y, text, colkey=9, bg=None):
        x = pyxel.width / 2 - len(text) * 2

        if bg:
            pyxel.rect(x-1, y-1, len(text) * 4 + 2, 5 + 2, bg)

        pyxel.text(x, y, text, colkey)

    def update(self):
        title_controller(self)

    def draw(self):
        pyxel.cls(1)
        for y in range(pyxel.height):
            for x in range(pyxel.width):
                n = pyxel.noise(x/20, y/20, pyxel.frame_count / 40)
                if n > 0.7:
                    point_val = 1
                elif n > 0.4:
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
        first30 = pyxel.height * 0.3
        self.center_x_text(first30 / 2, "TITULO DO JOGO", 9, 13)

        for i, option in enumerate(self.menu_options):
            color = pyxel.frame_count % 15 if i == self.current_option else 9
            self.center_x_text(first30 + i*8, option, color, 12)


class GameScreen:
    def __init__(self, app):
        self.app = app
        self.start()

    def start(self, player=None, level=1):
        log.info(f"iniciando level {level}")
        if not player:
            player = Player(80, 60, Personagens.PLAYER[DOWN])

        self.player = player
        self.entities = []
        self._trash = set()
        self.player_hud = PlayerHUD()
        self.bg_color = pyxel.rndi(0, 15)

        self.direction = DOWN
        self.points = 0
        self.level = level
        self.last_spawn = 0
        self.portal = False

        map_entities = map_seed()
        self.entities += map_entities

    def spawn(self):
        enemy_count = len([enemy for enemy in self.filter_entities(Enemy)])
        if self.last_spawn + 10 < pyxel.frame_count and enemy_count < 10:
            log.debug("spawning enemie")
            self.last_spawn = pyxel.frame_count
            x = pyxel.rndi(0, pyxel.width)
            y = pyxel.rndi(0, pyxel.height)
            new_enemy = Enemy(
                x, y, Inimigos.TURRET[0], Inimigos.TURRET, vida=self.level)
            self.entities.append(new_enemy)

        if self.points >= 10 and not self.portal:
            log.info(f"points {self.points}")
            portal = Portal(pyxel.width // 2, pyxel.height // 2,
                            Objetos.PORTAL[0], Objetos.PORTAL)
            self.entities.append(portal)
            self.portal = True

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
                pyxel.play(0, 1)
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
                    self.kill(project_id)
                    enemy.vida -= projectile.damage
                    pyxel.play(0, 0)
                    if enemy.vida <= 0:
                        self.kill(entity_id)
                        self.points += 1
                        item = Item(enemy.x, enemy.y,
                                    Efeitos.EXP_ORB[0], Efeitos.EXP_ORB, enemy.exp)
                        self.entities.append(item)

        for entity_id, item in self.filter_entities(Item):
            exp_walk(self, item)
            if verifyCollision(item, self.player):
                if item.exp > 0:
                    self.player.exp_atual += item.exp
                    levelUp(self.player)
                    self.kill(entity_id)
                    log.debug(f"player ganhou {item.exp} de exp")
                else:
                    self.kill(entity_id)
                    self.player.inventory.append(item)
                    log.debug(f"player pegou o item: {entity_id}")

        for entity_id, portal in self.filter_entities(Portal):
            if verifyCollision(portal, self.player):
                self.start(self.player, self.level+1)

    def update(self):
        player_controller(self)
        self.entities_collision()
        self.spawn()

        if self.player.vida <= 0:
            self.start()
            self.app.switch_screen(self.app.title_screen)

        trash = reversed(sorted(self._trash))
        for entity_id in trash:
            del self.entities[entity_id]
            self._trash.remove(entity_id)
            log.debug(f"entidade: {entity_id} foi deletado")

    def draw(self):
        pyxel.cls(self.bg_color)
        pyxel.blt(self.player.x, self.player.y, *self.player.sprite)

        for entity in self.entities:
            if hasattr(entity, 'sprite_list'):
                frames_per_sprite = 3
                sprite_frame = pyxel.frame_count % len(
                    entity.sprite_list) * frames_per_sprite
                sprite_i = sprite_frame // frames_per_sprite
                entity.sprite = entity.sprite_list[sprite_i]
            pyxel.blt(entity.x, entity.y, *entity.sprite)

        vida_texto = "points: {}".format(self.points)
        pyxel.text(10, 10, vida_texto, 7)

        self.player_hud.drawn(self.player)
