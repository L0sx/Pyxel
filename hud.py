import pyxel


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
