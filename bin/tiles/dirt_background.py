from pygame import Surface, Vector2
from bin.map import Block
from bin.map import Chunk
from bin.abstractClasses import Executor


class dirt_background(Block):
    MAINTEXTURE = "tiles/dirt_background.png"
    MAINTEXTUREISTRANSPARENT = False
    ID = "dirt_background"
    IDInt = 20
    
    lightingAbsorption = 0 # tells lighting engine how that should be treated (if that should absorb the light)