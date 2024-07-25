from pygame import Surface, Vector2
from bin.map import Block
from bin.map import Chunk
from bin.abstractClasses import Executor


class oak_leaves(Block):
    MAINTEXTURE = "tiles/oak_leaves.png"
    MAINTEXTUREISTRANSPARENT = True
    ID = "oak_leaves"
    IDInt = 11
    
    lightingAbsorption = 1 # tells lighting engine how that should be treated (if that should absorb the light)