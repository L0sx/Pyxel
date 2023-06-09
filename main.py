import pyxel
import math

from map_gen import map_seed
from entity import Entity



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


def random_walk(character):
    character.x = (character.x - pyxel.rndi(-1, 1)) % pyxel.width
    character.y = (character.y - pyxel.rndi(-1, 1)) % pyxel.width

def verifyCollision(objeto1, objeto2):
        if (objeto1.x < objeto2.x + objeto2.sprite[3] and
                objeto1.x + objeto1.sprite[3] > objeto2.x and
                objeto1.y < objeto2.y + objeto2.sprite[4] and
                objeto1.y + objeto1.sprite[4] > objeto2.y):
            return True
        else:
            return False



class App:
    def __init__(self):
        self.player = Entity("Player", 80, 60, SPRITEDOWN)
        self.entities = []
        self.vida = 10
        self.entities.append(Entity("inimigo", 10, 10, ENEMIE_1_DOWN))
        self.last_key_pressed = None

        pyxel.init(160, 120)
        pyxel.load("assets/pyxel.pyxres")
        more_entities = map_seed()
        self.entities += more_entities
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btn(pyxel.KEY_LEFT):
            self.player.x = (self.player.x - 1) % pyxel.width
            self.player.sprite = SPRITELEFT
            self.last_key_pressed = pyxel.KEY_LEFT
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.player.x = (self.player.x + 1) % pyxel.width
            self.player.sprite = SPRITERIGHT
            self.last_key_pressed = pyxel.KEY_RIGHT
        if pyxel.btn(pyxel.KEY_DOWN):
            self.player.y = (self.player.y + 1) % pyxel.height
            self.player.sprite = SPRITEDOWN
            self.last_key_pressed = pyxel.KEY_DOWN
        if pyxel.btn(pyxel.KEY_UP):
            self.player.y = (self.player.y - 1) % pyxel.height
            self.player.sprite = SPRITEUP
            self.last_key_pressed = pyxel.KEY_UP
        if pyxel.btn(pyxel.KEY_A):
            self.draw_player_attack()

        for entity in self.entities:
            if entity.name == "inimigo":
                random_walk(entity)
        for entity in self.entities:
            if entity.name == "inimigo" and verifyCollision(self.player, entity):
                if self.player.x < entity.x:
                    self.vida -= 1
                    self.player.x -= 5
                    entity.x += 5
                else:
                    self.vida -= 1
                    self.player.x += 5
                    entity.x -= 5
                    

    def draw(self):
        pyxel.cls(1)
        pyxel.blt(self.player.x, self.player.y, *self.player.sprite)
        
        for entity in self.entities:
            pyxel.blt(entity.x, entity.y, *entity.sprite)

        vida_texto = "Vida: {}".format(self.vida)
        pyxel.text(10, 10, vida_texto, 7)

    def draw_player_attack(self):
        pyxel.cls(2)
        angle = 0

        if self.last_key_pressed == pyxel.KEY_UP:
            angle = 270
        elif self.last_key_pressed == pyxel.KEY_DOWN:
            angle = 90
        elif self.last_key_pressed == pyxel.KEY_LEFT:
            angle = 180
        elif self.last_key_pressed == pyxel.KEY_RIGHT:
            angle = 0

        # Converter o ângulo para radianos
        angle_rad = math.radians(angle)

        # Calcular as coordenadas finais do raio de ataque
        attack_length = 40
        attack_end_x = self.player.x + attack_length * math.cos(angle_rad)
        attack_end_y = self.player.y + attack_length * math.sin(angle_rad)

        rect_width = abs(attack_end_x - self.player.x)
        rect_height = abs(attack_end_y - self.player.y)
        rect_x = min(attack_end_x, self.player.x)
        rect_y = min(attack_end_y, self.player.y)
        

        # Desenhar o raio de ataque
        pyxel.rect(rect_x, rect_y, rect_width, rect_height, 9)

        # Verificar colisão com inimigos
        for entity in self.entities:
            if self.check_collision(entity, attack_end_x, attack_end_y):
                print("Inimigo atingido!")

    def check_collision(self, entity, x, y):
        enemy_size = 16
        if (x > entity.x and x < entity.x + enemy_size and
            y > entity.y and y < entity.y + enemy_size):
            return True
        return False
        

App()
