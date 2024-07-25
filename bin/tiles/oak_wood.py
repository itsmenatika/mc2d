from pygame import Surface, Vector2
from bin.map import Block
from bin.map import Chunk
from bin.abstractClasses import Executor



class oak_wood(Block):
    MAINTEXTURE = "tiles/oak_wood.png"
    MAINTEXTUREISTRANSPARENT = False
    ID = "oak_wood"
    IDInt = 7