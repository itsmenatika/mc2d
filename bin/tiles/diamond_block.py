from pygame import Surface, Vector2
from bin.map import Block
from bin.map import Chunk
from bin.abstractClasses import Executor


class diamond_block(Block):
    MAINTEXTURE = "tiles/diamond_block.png"
    MAINTEXTUREISTRANSPARENT = False
    ID = "diamond_block"
    IDInt = 12
