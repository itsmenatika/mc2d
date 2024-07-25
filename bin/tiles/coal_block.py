from pygame import Surface, Vector2
from bin.map import Block
from bin.map import Chunk
from bin.abstractClasses import Executor


class coal_block(Block):
    MAINTEXTURE = "tiles/coal_block.png"
    MAINTEXTUREISTRANSPARENT = False
    ID = "coal_block"
