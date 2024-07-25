from pygame import Surface, Vector2
from bin.map import Block
from bin.map import Chunk
from bin.abstractClasses import Executor


class Unknown(Block):
    MAINTEXTURE = "tiles/default.png"
    MAINTEXTUREISTRANSPARENT = False
    ID = "?"
    IDInt = 19
