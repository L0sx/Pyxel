import pyxel


def rainbow():
    return pyxel.frame_count % 15


def frame_cd(n) -> bool:
    return not pyxel.frame_count % n


def rndxy():
    return pyxel.rndi(0, pyxel.width), pyxel.rndi(0, pyxel.height)


def get_tile(tile_x, tile_y):
    return pyxel.tilemap(0).pget(tile_x, tile_y)
