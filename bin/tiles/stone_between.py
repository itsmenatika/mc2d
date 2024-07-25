from pygame import Surface, Vector2
from bin.map import Block
from bin.map import Chunk
from bin.abstractClasses import Executor



class stone_between(Block):
    MAINTEXTURE = "tiles/stone_between.png"
    MAINTEXTUREISTRANSPARENT = False
    ID = "stone_between"
    IDInt = 5