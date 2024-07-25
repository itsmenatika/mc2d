from pygame import Surface, Vector2
from bin.map import Block
from bin.map import Chunk
from bin.abstractClasses import Executor


class coal_ore(Block):
    MAINTEXTURE = "tiles/coal.png"
    MAINTEXTUREISTRANSPARENT = False
    ID = "coal_ore"
    IDInt = 6
