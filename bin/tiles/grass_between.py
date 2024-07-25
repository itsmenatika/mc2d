from pygame import Surface, Vector2
from bin.map import Block
from bin.map import Chunk
from bin.abstractClasses import Executor



class grass_between(Block):
    MAINTEXTURE = "tiles/grass_between.png"
    MAINTEXTUREISTRANSPARENT = False
    ID = "grass_between"
    IDInt = 4
