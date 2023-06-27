import logging
import pyxel
from typing import Callable, Generator, Tuple
from map_gen import map_seed
from entity import (Enemy, Player, Portal, Projectile, verifyCollision,
                    Item, levelUp, exp_walk, space_button, a_button, ciclone, arrow)
from sprites import LEFT, RIGHT, UP, DOWN
from sprites import Inimigos, Personagens, Objetos, Efeitos, Colors
from hud import PlayerHUD

log = logging.getLogger(__name__)


def center_x_text(y, text, colkey=9, bg=None):
    x = pyxel.width / 2 - len(text) * 2
    if bg:
        pyxel.rect(x-1, y-1, len(text) * 4 + 2, 5 + 2, bg)
    pyxel.text(x, y, text, colkey)


class TitleScreen:
    def __init__(self, app):
        self.app = app
        self.current_option = 0
        self.deadzone = 2000
        self.characters = [Player(0, 0, Personagens.WARRIOR[DOWN], Personagens.WARRIOR, skill_1=ciclone), 
                            Player(0, 0, Personagens.ARCHER[DOWN], Personagens.ARCHER, skill_1=arrow),
                            Player(0, 0, Personagens.MAGE[DOWN], Personagens.MAGE, skill_1=a_button),
                            CreditsScreen]
        self.current_player = 0

    def controller(self):
        if pyxel.btnp(pyxel.KEY_LEFT):
            self.current_player = (self.current_player - 1) % 3
        if pyxel.btnp(pyxel.KEY_RIGHT):
            self.current_player = (self.current_player + 1) % 3
        if pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnv(pyxel.GAMEPAD1_AXIS_LEFTY) > self.deadzone:
            self.current_player = 3
        if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnv(pyxel.GAMEPAD1_AXIS_LEFTY) < -self.deadzone:
            self.current_player = 0
        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_START):
            match self.current_player:
                case 0:
                    self.app.select_player = self.characters[self.current_player]
                    self.app.switch_screen(GameScreen)
                case 1:
                    self.app.select_player = self.characters[self.current_player]
                    self.app.switch_screen(GameScreen)
                case 2:
                    self.app.select_player = self.characters[self.current_player]
                    self.app.switch_screen(GameScreen)
                case 3:
                    self.app.switch_screen(CreditsScreen)
            # self.app.switch_screen(self.menu_options[self.current_option])

    def update(self):
        self.controller()

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
        center_x_text(first30 / 2, "TITULO DO JOGO", 9, 13)

        
        color = pyxel.frame_count % 15
        option = self.characters[3].name
        center_x_text(first30 + 30, option, color if self.current_player == 3 else 0, 12)
        char1 = self.characters[0]
        char2 = self.characters[1]
        char3 = self.characters[2]
        x = 76
        y = 50
        pyxel.circ(x + 3, y + char2.sprite[3] // 2, char2.sprite[3], Colors.BLACK)
        pyxel.circb(x + 3, y + char2.sprite[3] // 2, char2.sprite[3], pyxel.frame_count % 15 if self.current_player == 0 else 11)
        pyxel.circ(x + 23, y + char3.sprite[3] // 2, char3.sprite[3], Colors.BLACK)
        pyxel.circb(x + 23, y + char3.sprite[3] // 2, char3.sprite[3], pyxel.frame_count % 15 if self.current_player == 1 else 11)
        pyxel.circ(x - 17, y + char1.sprite[3] // 2, char1.sprite[3], Colors.BLACK)
        pyxel.circb(x - 17, y + char1.sprite[3] // 2, char1.sprite[3], pyxel.frame_count % 15 if self.current_player == 2 else 11)
        pyxel.blt(x, y, *char1.sprite)
        pyxel.blt(x + 20, y, *char2.sprite)
        pyxel.blt(x - 20, y, *char3.sprite)

class CreditsScreen:
    name = "Creditos"

    def __init__(self, app):
        self.app = app

    def controller(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            self.app.switch_screen(GameScreen)
        if pyxel.btnp(pyxel.KEY_RIGHT):
            pass
        if pyxel.btnp(pyxel.KEY_DOWN):
            pass
        if pyxel.btnp(pyxel.KEY_UP):
            pass
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.app.switch_screen(TitleScreen)

    def update(self):
        self.controller()

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

        xpadd = pyxel.width // 10
        ypadd = pyxel.height // 10
        w = pyxel.width - xpadd * 2
        h = pyxel.height - ypadd * 2
        pyxel.rect(xpadd, ypadd, w, h, 5)

        center_x_text(first30 / 2, "CREDITOS", 9, 13)
        center_x_text(30, "FEITOR POR:", 9, 13)
        center_x_text(40, "bhunao", 9, 13)
        center_x_text(50, "los", 9, 13)


class GameScreen:
    name = "game"

    def __init__(self, app):
        self.app = app
        self.player = self.app.select_player
        self.start()
        self.t = 0
        

    def start(self, level=1):
        log.info(f"iniciando level {level}")
        self.player = self.player
        self.player.x = pyxel.width // 2
        self.player.y = pyxel.height // 2

        self.entities = []
        self._trash = set()
        self.player_hud = PlayerHUD()
        self.bg_color = pyxel.rndi(0, 15)

        self.direction = DOWN
        self.points = 0
        self.level = level
        self.last_spawn = 0
        self.portal = False
        self.deadzone = 2000

        map_entities = map_seed()
        self.entities += map_entities
        boss = Enemy(0, 0, Inimigos.BOSS[0], Inimigos.BOSS, vida=level*10)
        self.entities.append(boss)

        self.camera = [0, 0]

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
                self.start(self.level+1)

    def updateCamera (self):
        self.camera[0] = self.player.x - pyxel.width // 2
        self.camera[1] = self.player.y - pyxel.height // 2

    def controller(self):
        for at in dir(pyxel):
            if "GAMEPAD" in at:
                attr = getattr(pyxel, at)
                bo = pyxel.btn(attr)
                if bo:
                    print(attr, at, bo)

        #print(pyxel.GAMEPAD1_BUTTON_A, pyxel.GAMEPAD1_BUTTON_DPAD_LEFT)
        #print(pyxel.btnv(pyxel.GAMEPAD2_AXIS_LEFTX),
        #      pyxel.btnv(pyxel.GAMEPAD1_AXIS_LEFTY))
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
            self.player.x = (self.player.x - 1)
            self.player.sprite = self.player.spritelist[LEFT]
            self.player.direct = LEFT
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
            self.player.x = (self.player.x + 1)
            self.player.sprite = self.player.spritelist[RIGHT]
            self.player.direct = RIGHT
        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
            self.player.y = (self.player.y + 1)
            self.player.sprite = self.player.spritelist[DOWN]
            self.player.direct = DOWN
        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
            self.player.y = (self.player.y - 1)
            self.player.sprite = self.player.spritelist[UP]
            self.player.direct = UP
        if pyxel.btnp(pyxel.KEY_A) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
            self.entities += self.player.skill_1(self)
        if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_X):
            self.entities += space_button(self)

    def update(self):
        self.updateCamera()
        self.t += 1
        self.controller()
        self.entities_collision()
        self.spawn()
        self.player_hud.update(self.player)

        if self.player.vida <= 0:
            self.start()
            self.app.switch_screen(TitleScreen)

        trash = reversed(sorted(self._trash))
        for entity_id in trash:
            del self.entities[entity_id]
            self._trash.remove(entity_id)
            log.debug(f"entidade: {entity_id} foi deletado")

    def draw(self):
        pyxel.camera(*self.camera)
        pyxel.cls(self.bg_color)
        pyxel.blt(self.player.x, self.player.y, *self.player.sprite)

        for entity in self.entities:
            if hasattr(entity, 'sprite_list') and entity.sprite_list != None:
                frames_per_sprite = 3
                sprite_frame = pyxel.frame_count % len(
                    entity.sprite_list) * frames_per_sprite
                sprite_i = sprite_frame // frames_per_sprite
                entity.sprite = entity.sprite_list[sprite_i]
            pyxel.blt(entity.x, entity.y, *entity.sprite)

        vida_texto = "points: {}".format(self.points)
        pyxel.text(10, 10, vida_texto, 7)

        self.player_hud.drawn()
