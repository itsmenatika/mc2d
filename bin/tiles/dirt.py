from pygame import Surface, Vector2
from bin.map import Block
from bin.map import Chunk
from bin.abstractClasses import Executor


class dirt(Block):
    MAINTEXTURE = "tiles/dirt.png"
    MAINTEXTUREISTRANSPARENT = False
    ID = "dirt"
    IDInt = 1