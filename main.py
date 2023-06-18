import logging
import pyxel
from screen import TitleScreen, GameScreen


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
        self.screens = {
            TitleScreen: TitleScreen(self),
            GameScreen: GameScreen(self),

        }
        self.current_screen = self.screens[TitleScreen]
        self.game_screen = GameScreen(self)

        pyxel.run(self.update, self.draw)

    def switch_screen(self, screen):
        print(screen, self.screens.keys())
        self.current_screen = self.screens[screen]

    def update(self):
        self.current_screen.update()

    def draw(self):
        self.current_screen.draw()


App()
