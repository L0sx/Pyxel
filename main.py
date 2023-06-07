import pyxel

SPRITEDOWN = 0, 0, 0, 8, 8, 0
SPRITEUP = 0, 8, 0, 8, 8, 0
SPRITELEFT = 0, 0, 8, 8, 8, 0
SPRITERIGHT = 0, 8, 8, 8, 8, 0

class Player:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.sprite = SPRITEDOWN

class App:
    def __init__(self):
        self.player = Player()
        pyxel.init(160, 120)
        pyxel.load("assets/pyxel.pyxres")
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btn(pyxel.KEY_LEFT):
            self.player.x = (self.player.x - 1) % pyxel.width
            self.player.sprite = SPRITELEFT
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.player.x = (self.player.x + 1) % pyxel.width
            self.player.sprite = SPRITERIGHT
        if pyxel.btn(pyxel.KEY_DOWN):
            self.player.y = (self.player.y + 1) % pyxel.height
            self.player.sprite = SPRITEDOWN
        if pyxel.btn(pyxel.KEY_UP):
            self.player.y = (self.player.y - 1) % pyxel.height
            self.player.sprite = SPRITEUP

    def draw(self):
        pyxel.cls(0)
        pyxel.blt(self.player.x, self.player.y, *self.player.sprite)
        

App()
