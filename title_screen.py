import pyxel



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


class App:
    def __init__(self):
        self.menu_options = [
                "start",
                "configs",
                "credits"
                ]
        self.current_option = 0
        pyxel.init(160, 120)
        pyxel.load("assets/pyxel.pyxres")
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_LEFT):
            pass
        if pyxel.btnp(pyxel.KEY_RIGHT):
            pass
        if pyxel.btnp(pyxel.KEY_DOWN):
            self.current_option = (self.current_option + 1) % len(self.menu_options)
        if pyxel.btnp(pyxel.KEY_UP):
            self.current_option = (self.current_option - 1) % len(self.menu_options)
        if pyxel.btnp(pyxel.KEY_A):
            pass


    def draw(self):
        pyxel.cls(1)
        for y in range(pyxel.height):
            for x in range(pyxel.width):
                n = pyxel.noise(x/20, y/20, pyxel.frame_count/ 40)
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

        for i, option in enumerate(self.menu_options):
            color = pyxel.frame_count % 15 if i == self.current_option else 9
            center_x_text(first30 + i*8, option, color, 12)


if __name__ == "__main__":
    App()
