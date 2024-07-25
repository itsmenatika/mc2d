from pygame import Surface, Vector2
from bin.map import Block
from bin.map import Chunk
from bin.abstractClasses import Executor


class diamond_ore(Block):
    MAINTEXTURE = "tiles/diamond.png"
    MAINTEXTUREISTRANSPARENT = False
    ID = "diamond_ore"
    IDInt = 9