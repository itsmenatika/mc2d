from pygame import Surface, Vector2
from bin.map import Block
from bin.map import Chunk
from bin.abstractClasses import Executor



class grass_block(Block):
    MAINTEXTURE = "tiles/grass.png"
    MAINTEXTUREISTRANSPARENT = False
    ID = "grass_block"
    IDInt = 2