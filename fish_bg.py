from dataclasses import dataclass
from math import atan2, cos, degrees, radians, sin, sqrt
from typing import Dict, Optional, Sequence
from sprites import ARCHER, DOWN, FIREBALL, MAGE, RIGHT, WARRIOR, Sides

from engine import esper
import pyxel


def rndxy():
    return pyxel.rndi(0, pyxel.width), pyxel.rndi(0, pyxel.height)


@dataclass
class Sprite:
    sprite: Sequence[tuple] = ((0, 0, 0, 8, 8, 0), )
    states: Optional[Dict] = None
    current_state: Optional[type] = None
    w: int = sprite[0][3]
    h: int = sprite[0][4]


@dataclass
class Pos:
    x: float = 0
    y: float = 0


@dataclass
class Combat:
    hp: int = 1
    max_hp: int = hp
    damage: int = 0


class Enemy:
    pass


class Projectile:
    pass


class EnemyProjectile:
    pass


@dataclass
class Movement:
    speed: float = 0
    angle: float = 0


@dataclass
class Timer:
    time: int


@dataclass
class Text:
    text: str = "PLACEHOLDER"
    colkey: int = 9


class TextSystem(esper.Processor):
    def process(self):
        text_comps = Text, Pos
        for _, (text, pos) in self.world.get_components(*text_comps):
            pyxel.text(pos.x, pos.y, text.text, text.colkey)


class TimerSystem(esper.Processor):
    def process(self):
        for id, timer in self.world.get_components(Timer):
            timer = timer[0]
            timer.time -= 1
            if timer.time <= 0:
                self.world.delete_entity(id)


class HUD(esper.Processor):
    def process(self):
        _, (pos, sprite, combat, _) = self.world.get_components(
            Pos, Sprite, Combat, PlayerComponent)[0]

        exp = 5
        exp_atual = exp if exp else 1
        exp_total = 10
        percenteExp = (exp_atual / exp_total)
        tamanhoBarra = pyxel.width - 20

        xlife = pos.x
        ylife = pos.y - 4
        tamanhoLife = sprite.w
        percenteLife = (combat.hp / combat.max_hp)

        pyxel.circ(10, 10, sprite.w, 7)
        pyxel.circb(10, 10, sprite.w, 10)

        pyxel.rect(10, 10, tamanhoBarra * percenteExp, 4, 3)
        pyxel.rectb(10, 10, tamanhoBarra, 4, 7)

        pyxel.rect(xlife, ylife, tamanhoLife * percenteLife, 1, 8)


class EnemySpawner(esper.Processor):
    def process(self):
        comps = self.world.get_components(Enemy)
        if len(comps) <= 5:
            x, y = rndxy()
            self.world.create_entity(
                Sprite(
                    states=WARRIOR,
                    current_state=DOWN
                ),
                Pos(
                    x=x,
                    y=y,
                ),
                Movement(speed=1),
                Enemy(),
                Combat(),
            )


class CollissionSystem(esper.Processor):
    def process(self):
        pid, (playerpos, playersprite, _) = self.world.get_components(
            Pos, Sprite, PlayerComponent)[0]

        for eid, (pos, sprite) in self.world.get_components(Pos, Sprite):
            if pid == eid:
                continue
            pass

        projcetile_components = Pos, Sprite, Combat, Projectile
        for pid, (ppos, psprite, pcombat, _) in self.world.get_components(*projcetile_components):
            enemy_components = Pos, Sprite, Combat, Enemy
            for eid, (epos, esprite, ecombat, _) in self.world.get_components(*enemy_components):
                if self.collide_with(ppos, psprite, epos, esprite):
                    self.world.create_entity(
                        Text(str(pcombat.damage)),
                        Pos(epos.x, epos.y),
                        Movement(speed=1, angle=-90),
                        Timer(25),
                    )
                    self.attack(pcombat, ecombat, eid)

    def attack(self, combat1: Combat, combat2: Combat, combat2_id):
        print(combat1, combat2, combat2_id)
        combat2.hp -= combat1.damage
        if combat2.hp <= 0:
            self.world.delete_entity(combat2_id)

    @staticmethod
    def collide_with(render1, sprite1, render2, sprite2):
        if render1.x > render2.x + sprite2.w or render2.x > render1.x + sprite1.w:
            return False
        if render1.y > render2.y + sprite2.w or render2.y > render1.y + sprite1.w:
            return False
        return True


class MovementSystem(esper.Processor):
    def process(self):
        _, (player, _) = self.world.get_components(
            Pos, PlayerComponent)[0]
        for _id, (pos, moviment) in self.world.get_components(Pos, Movement):
            self.move(pos, moviment)
        for _id, (pos, moviment, _) in self.world.get_components(Pos, Movement, Enemy):
            self.move_keep_distance(pos, moviment, target=player)

    @staticmethod
    def move(pos, moviment):
        angle_rad = radians(moviment.angle)
        pos.x += cos(angle_rad) * moviment.speed
        pos.y += sin(angle_rad) * moviment.speed

    def move_to_target(self, pos, moviment, target=None):
        if target is None:
            self.move(pos, moviment)
            return

        dx = pos.x - target.x
        dy = pos.y - target.y
        angle = - degrees(atan2(dx, dy)) - 90
        moviment.angle = angle
        self.move(pos, moviment)

    def move_away_from(self, pos, moviment, target=None):
        if target is None:
            self.move(moviment, pos)
            return

        dx = pos.x - target.x
        dy = pos.y - target.y
        angle = degrees(pyxel.atan2(dx, dy)) - 90
        moviment.angle = angle
        self.move(pos, moviment)

    def move_keep_distance(self, pos, moviment, target=None):
        if target is None:
            self.move(pos, moviment)
        else:
            n1 = (pos.x - target.x)**2
            n2 = (pos.y - target.y)**2
            distance = sqrt(n1 + n2)
            if distance > 75:
                self.move_to_target(pos, moviment, target)
            elif distance < 50:
                self.move_away_from(pos, moviment, target)


class PlayerComponent:
    pass


class SpriteSystem(esper.Processor):
    def __init__(self) -> None:
        super().__init__()

    def draw_sprite(self, sprite: Sprite, pos: Pos):
        nframes = 5
        i = pyxel.frame_count % (nframes * len(sprite.sprite)) // nframes
        pyxel.blt(pos.x, pos.y, *sprite.sprite[i])

    def process(self):
        for _, (sprite, pos) in self.world.get_components(Sprite, Pos):
            if sprite.states is None:
                self.draw_sprite(sprite, pos)
            else:
                self.draw_state_sprite(sprite, pos)

    @staticmethod
    def draw_state_sprite(sprite, pos):
        if sprite.states and sprite.current_state:
            image = sprite.states[sprite.current_state]
        else:
            image = sprite.image
        nframes = 5
        i = pyxel.frame_count % (nframes * len(image)) // nframes
        pyxel.blt(pos.x, pos.y, *image[i])


class KeyboardInputProcessor(esper.Processor):
    def __init__(self) -> None:
        super().__init__()

    def send_player_pos(self, client, render):
        client.send(str(render.__dict__))

    def process(self):
        for ent, (pos, player) in self.world.get_components(Pos, PlayerComponent):
            if pyxel.btn(pyxel.KEY_LEFT):
                pos.x -= 1
            if pyxel.btn(pyxel.KEY_RIGHT):
                pos.x += 1
            if pyxel.btn(pyxel.KEY_UP):
                pos.y -= 1
            if pyxel.btn(pyxel.KEY_DOWN):
                pos.y += 1
            if pyxel.btnp(pyxel.KEY_SPACE):
                for side in Sides:
                    self.world.create_entity(
                        Projectile(),
                        Pos(x=pos.x, y=pos.y),
                        Sprite(FIREBALL[RIGHT]),
                        Movement(speed=3, angle=side.value),
                        Timer(25),
                        Combat(damage=1),
                    )
            if pyxel.btnp(pyxel.KEY_Q):
                self.world.create_entity(
                    Projectile(),
                    Pos(x=pos.x, y=pos.y),
                    Sprite(FIREBALL[RIGHT]),
                    Movement(speed=3, angle=0),
                    Timer(25),
                    Combat(damage=1),
                )


class App:
    def __init__(self) -> None:
        pyxel.init(180, 140)
        pyxel.load("assets/pyxel.pyxres")
        pyxel.playm(0, loop=True)

        self.world = esper.World()
        self.world.add_processor(SpriteSystem())
        self.world.add_processor(MovementSystem())
        self.world.add_processor(EnemySpawner())
        self.world.add_processor(HUD())
        self.world.add_processor(TimerSystem())
        self.world.add_processor(KeyboardInputProcessor())
        self.world.add_processor(CollissionSystem())
        self.world.add_processor(TextSystem())

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
            Combat(hp=5)
        )
        self.world.create_entity(
            Sprite(
                states=ARCHER,
                current_state=DOWN
            ),
            Pos(
                x=pyxel.width//3,
                y=pyxel.height//3,
            ),
            Movement(speed=1)
        )

        pyxel.run(self.update, self.draw)

    def update(self):
        return

    def draw(self):
        pyxel.cls(1)
        self.world.process()


App()
