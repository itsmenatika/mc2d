from pygame import Surface, Vector2
from bin.map import Block
from bin.map import Chunk
from bin.abstractClasses import Executor



class stone(Block):
    MAINTEXTURE = "tiles/stone.png"
    MAINTEXTUREISTRANSPARENT = False
    ID = "stone"
    IDInt = 3
