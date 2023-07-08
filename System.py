from math import atan2, cos, degrees, pi, radians, sin, sqrt
from sprites import ARCHER, DOWN, FIREBALL, MAGE, RIGHT, WARRIOR, Sides, UPATTACK, UPLIFE, UPCD, UPSPEED, UPPROJECTILE
from components import *
from functions import *

import esper
import pyxel

class RenderSystem(esper.Processor):
    def process(self):
        circle_comps = Circle, Pos
        for _, (circle, pos) in self.world.get_components(*circle_comps):
            colkey = circle.colkey if circle.colkey <= 15 else rainbow()
            pyxel.circb(pos.x, pos.y, circle.r, colkey)
            circle.r += circle.r_inc
        square_comps = Square, Pos
        for _, (square, pos) in self.world.get_components(*square_comps):
            colkey = square.colkey if square.colkey <= 15 else rainbow()
            pyxel.rect(pos.x, pos.y, square.w, square.h, colkey)
        text_comps = Text, Pos
        for _, (text, pos) in self.world.get_components(*text_comps):
            colkey = text.colkey if text.colkey <= 15 else rainbow()
            pyxel.text(pos.x, pos.y, text.text, colkey)
        



class TimerSystem(esper.Processor):
    def process(self):
        pid, (_, player) = self.world.get_components(
            Pos, PlayerComponent)[0]
        if player.selectupgrade:
            return
        for id, timer in self.world.get_components(Timer):
            timer = timer[0]
            timer.time -= 1
            if timer.time <= 0:
                self.world.delete_entity(id)

class CollissionSystem(esper.Processor):
    def show_upgrade(self):
        sprites = UPATTACK, UPLIFE, UPCD, UPSPEED, UPPROJECTILE
        

        for i, sprite in enumerate(sprites):
            self.world.create_entity(
                Square(16, 16),
                Upgrade(),
                Pos(
                    x= 60 + i*20,
                    y=pyxel.height//2,
                ),
                Sprite(sprite),
            )
            self.world.create_entity(
                Square(6, 6, 3),
                Text(text=str(i)),
                Pos(
                    x= 60 + i*20,
                    y=pyxel.height//2 + 20,
                ),
                Upgrade()

            )

    def process(self):
        pid, (playerpos, playersprite, playercombat, player) = self.world.get_components(
            Pos, Sprite, Combat, PlayerComponent)[0]
        if player.selectupgrade:
            return
        for eid, (pos, sprite) in self.world.get_components(Pos, Sprite):
            if pid == eid:
                continue
            pass

        projcetile_components = Pos, Sprite, Combat, Projectile
        for pid, (ppos, psprite, pcombat, _) in self.world.get_components(*projcetile_components):
            enemy_components = Pos, Sprite, Combat, Enemy
            for eid, (epos, esprite, ecombat, enemy) in self.world.get_components(*enemy_components):
                if self.collide_with(ppos, psprite, epos, esprite):
                    self.world.delete_entity(pid)
                    if self.attack(pcombat, ecombat, eid):
                        self.world.create_entity(
                            Text(str(pcombat.damage)),
                            Pos(epos.x, epos.y),
                            Movement(speed=1, angle=-90),
                            Timer(25),
                        )
                        player.exp += enemy.exp

                    if player.exp >= player.exp_total:
                        player.exp = player.exp_total - player.exp
                        player.exp_total = int(player.exp_total*pi)
                        player.level += 1
                        player.selectupgrade = True
                        self.show_upgrade()
                        self.world.create_entity(
                            Circle(r_inc=1),
                            Pos(playerpos.x, playerpos.y),
                            Timer(25),
                        )
                        self.world.create_entity(
                            Circle(r_inc=2),
                            Pos(playerpos.x, playerpos.y),
                            Timer(25),
                        )
                        self.world.create_entity(
                            Circle(r_inc=3),
                            Pos(playerpos.x, playerpos.y),
                            Timer(25),
                        )

        enemy_components = Pos, Sprite, Combat, Enemy
        for eid, (epos, esprite, ecombat, enemy) in self.world.get_components(*enemy_components):
            if self.collide_with(epos, esprite, playerpos, playersprite):
                if self.attack(ecombat, playercombat):
                    self.world.create_entity(
                        Text(str(ecombat.damage), 7),
                        Pos(epos.x, epos.y),
                        Movement(speed=1, angle=-90),
                        Timer(25),
                    )

    def attack(self, combat1: Combat, combat2: Combat, combat2_id=None):
        combat2.hp -= combat1.damage
        if combat2.hp <= 0 and combat2_id:
            self.world.delete_entity(combat2_id)
            pyxel.play(0, 0)
            return True

    @staticmethod
    def collide_with(render1, sprite1, render2, sprite2):
        if render1.x > render2.x + sprite2.w or render2.x > render1.x + sprite1.w:
            return False
        if render1.y > render2.y + sprite2.w or render2.y > render1.y + sprite1.w:
            return False
        return True


class MovementSystem(esper.Processor):
    def process(self):
        _, (player, playercomponent) = self.world.get_components(
            Pos, PlayerComponent)[0]
        if playercomponent.selectupgrade:
            return
        for _id, (pos, moviment) in self.world.get_components(Pos, Movement):
            self.move(pos, moviment)

        for _id, (pos, moviment) in self.world.get_components(Pos, CircularMovement):
            self.move_circular(pos, moviment)

        for _id, (pos, moviment, _) in self.world.get_components(Pos, Movement, Enemy):
            self.move_to_target(pos, moviment, target=player)

    @staticmethod
    def move_circular(pos, moviment):
        angle_rad = radians(moviment.angle + pyxel.frame_count * 10)
        pos.x += cos(angle_rad) * moviment.speed
        pos.y += sin(angle_rad) * moviment.speed

    @staticmethod
    def move(pos, moviment):
        angle_rad = radians(moviment.angle)
        pos.x += cos(angle_rad) * moviment.speed
        pos.y += sin(angle_rad) * moviment.speed

    def move_to_target(self, pos, moviment, target):
        dx = pos.x - target.x
        dy = pos.y - target.y
        angle = - degrees(atan2(dx, dy)) - 90
        moviment.angle = angle

    def move_away_from(self, pos, moviment, target):
        dx = pos.x - target.x
        dy = pos.y - target.y
        angle = degrees(pyxel.atan2(dx, dy)) - 90
        moviment.angle = angle

    def move_keep_distance(self, pos, moviment, target):
        n1 = (pos.x - target.x)**2
        n2 = (pos.y - target.y)**2
        distance = sqrt(n1 + n2)
        if distance > 75:
            self.move_to_target(pos, moviment, target)
        elif distance < 50:
            self.move_away_from(pos, moviment, target)

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
        self.delay_q = 0
        self.delay_w = 0

    def remove_update(self):
        for ent, (upgrade) in self.world.get_components(Upgrade):
            self.world.delete_entity(ent)

    def process(self):
        for ent, (pos, combat, player) in self.world.get_components(Pos, Combat, PlayerComponent):
            if player.selectupgrade:
                if pyxel.btn(pyxel.KEY_1):
                    combat.damage += 1
                    self.world.create_entity(
                            Text("Damage UP"),
                            Pos(pos.x, pos.y),
                            Movement(speed=1, angle=-90),
                            Timer(25),
                        )
                    player.selectupgrade = False
                    self.remove_update()
                if pyxel.btn(pyxel.KEY_2):
                    player.speed += 1
                    self.world.create_entity(
                            Text("Speed UP"),
                            Pos(pos.x, pos.y),
                            Movement(speed=1, angle=-90),
                            Timer(25),
                        )
                    player.selectupgrade = False
                    self.remove_update()
                if pyxel.btn(pyxel.KEY_3):
                    player.projectiles += 1
                    self.world.create_entity(
                            Text("Projectile UP"),
                            Pos(pos.x, pos.y),
                            Movement(speed=1, angle=-90),
                            Timer(25),
                        )
                    player.selectupgrade = False
                    self.remove_update()
                return
            if pyxel.btn(pyxel.KEY_LEFT):
                pos.x -= player.speed
            if pyxel.btn(pyxel.KEY_RIGHT):
                pos.x += player.speed
            if pyxel.btn(pyxel.KEY_UP):
                pos.y -= player.speed
            if pyxel.btn(pyxel.KEY_DOWN):
                pos.y += player.speed
            if pyxel.btn(pyxel.KEY_Q) and self.delay_q <= pyxel.frame_count:
                self.delay_q = int(pyxel.frame_count) + 30
                #print(f"{self.delay_q=} {pyxel.frame_count=}")
                for side in Sides:
                    self.world.create_entity(
                        Projectile(),
                        Pos(x=pos.x, y=pos.y),
                        Sprite(FIREBALL[RIGHT]),
                        CircularMovement(speed=6, angle=side.value),
                        Timer(50),
                        Combat(damage=combat.damage),
                    )
            if pyxel.btn(pyxel.KEY_W) and self.delay_w <= pyxel.frame_count:
                self.delay_w = int(pyxel.frame_count) + 30
                _, (epos, esprite, ecombat, _) = self.world.get_components(
                    Pos, Sprite, Combat, Enemy)[0]

                dx = pos.x - epos.x
                dy = pos.y - epos.y
                angle = - degrees(atan2(dx, dy)) - 90

                start = -25
                stop = 25
                step = (abs(start) + abs(stop)) // player.projectiles
                if player.projectiles > 1:
                    for ang_dif in range(start, stop + step, step):
                        self.world.create_entity(
                            Projectile(),
                            Pos(x=pos.x, y=pos.y),
                            Sprite(FIREBALL[RIGHT]),
                            Movement(speed=3, angle=angle+ang_dif),
                            Timer(25),
                            Combat(damage=combat.damage),
                        )
                else:
                    self.world.create_entity(
                        Projectile(),
                        Pos(x=pos.x, y=pos.y),
                        Sprite(FIREBALL[RIGHT]),
                        Movement(speed=3, angle=angle),
                        Timer(25),
                        Combat(damage=combat.damage),
                    )

class HUD(esper.Processor):
    def process(self):
        _, (epos, esprite, ecombat, _) = self.world.get_components(
            Pos, Sprite, Combat, Enemy)[0]

        pyxel.circb(epos.x+esprite.w//2, epos.y +
                    esprite.h//2, esprite.w, rainbow())

        _, (pos, sprite, combat, player) = self.world.get_components(
            Pos, Sprite, Combat, PlayerComponent)[0]

        pyxel.line(epos.x, epos.y, pos.x, pos.y, rainbow())

        exp = player.exp
        exp_atual = exp if exp else 1
        exp_total = player.exp_total
        tamanhoBarra = pyxel.width - 20
        percenteExp = (exp_atual / exp_total)

        xlife = pos.x
        ylife = pos.y - 4
        hp = combat.hp if combat.hp > 0 else 1
        percenteLife = (hp / combat.max_hp)
        healthbar_size = sprite.w * percenteLife if combat.hp > 0 else 0

        pyxel.circ(10, 10, sprite.w, 7)
        pyxel.circb(10, 10, sprite.w, 10)

        pyxel.rect(10, 10, tamanhoBarra * percenteExp, 4, 3)
        pyxel.rectb(10, 10, tamanhoBarra, 4, 7)

        pyxel.rect(xlife, ylife, healthbar_size, 1, 8)


class EnemySpawner(esper.Processor):
    def process(self):
        pid, (playerpos, playersprite, pcombat, player) = self.world.get_components(
            Pos, Sprite, Combat, PlayerComponent)[0]

        coisa = pyxel.frame_count % 360
        c = cos(coisa)
        s = sin(coisa)

        xhalf = pyxel.width // 2
        yhalf = pyxel.height // 2

        speed = 120
        x = cos(coisa) * speed
        y = sin(coisa) * speed
        x += xhalf
        y += yhalf

        comps = self.world.get_components(Enemy)
        if len(comps) <= 10:
            # x, y = rndxy()
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
                Combat(hp=player.level//2+1, damage=player.level//2+1),
            )