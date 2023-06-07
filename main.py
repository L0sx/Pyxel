import pyxel

class App:
    def __init__(self):
        pyxel.init(160, 120)
        pyxel.load("assets/pyxel.pyxres")
        self.x = 0
        pyxel.run(self.update, self.draw)

    def update(self):
        self.x = (self.x + 1) % pyxel.width

    def draw(self):
        pyxel.cls(0)
        pyxel.bltm(self.x, 0, 0, 0, 0, 8, 8, 0)
App()
