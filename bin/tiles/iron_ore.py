from pygame import Surface, Vector2
from bin.map import Block
from bin.map import Chunk
from bin.abstractClasses import Executor


class iron_ore(Block):
    MAINTEXTURE = "tiles/iron_ore.png"
    MAINTEXTUREISTRANSPARENT = False
    ID = "iron_ore"
    IDInt = 10