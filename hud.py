import pyxel
from sprites import Hud
from entity import Object

class PlayerHUD:
    def __init__(self) -> None:
        self.listExp = []
        
    def criar_primeira_barra(self):
        self.listExp.append(Object(0, 118, Hud.exp_start, "exp_start"))
        
    def criar_barra_exp(self, x):
        zx = x + 2
        self.listExp.append(Object(zx, 118, Hud.exp_middle, "exp_middle"))
        
    def excluir_todas_barras(self):
        self.listExp.clear()

        
        
    def displayHud(self, player):
        
        exp_atual = player.exp_atual
        expToDisplay = int(player.exp_para_upar / 60)
        
        if exp_atual == 0:
            return
        else:
            print(expToDisplay % exp_atual)
        
        
    def update(self, player):
        self.displayHud(player)

    def drawn(self):
        for barra in self.listExp:
            pyxel.blt(barra.x, barra.y, *barra.sprite)
