import logging
import pyxel
from screen import CreditsScreen, TitleScreen, GameScreen


str_format = '%(asctime)s:%(name)s:%(levelname)s:%(message)s'
formatter = logging.Formatter(str_format)
logging.basicConfig(filename='game.log',
                    encoding='utf-8', level=logging.DEBUG, format=str_format)
log = logging.getLogger(__name__)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)
log.addHandler(ch)


class App:
    def __init__(self):
        log.debug("starting App")
        pyxel.init(160, 120)
        pyxel.load("assets/pyxel.pyxres")
        
        self.select_player = None
        self.screens = {
            TitleScreen: TitleScreen(self),
            GameScreen: None,
            CreditsScreen: None,
        }
        self.current_screen = self.screens[TitleScreen]
        

        pyxel.run(self.update, self.draw)

    def switch_screen(self, screen):
        if screen == GameScreen and self.screens[GameScreen] is None:
            self.screens[GameScreen] = GameScreen(self)
        elif screen == CreditsScreen and self.screens[CreditsScreen] is None:
            self.screens[CreditsScreen] = CreditsScreen(self)
        self.current_screen = self.screens[screen]

    def update(self):
         self.current_screen.update()
 
    def draw(self):
        self.current_screen.draw()


App()
