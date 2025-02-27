from pygame import Surface, Vector2
from bin.map import Block
from bin.map import Chunk
from bin.abstractClasses import Executor


class stone_background(Block):
    MAINTEXTURE = "tiles/stone_background.png"
    MAINTEXTUREISTRANSPARENT = False
    ID = "stone_background"
    IDInt = 22
    
    lightingAbsorption = 0 # tells lighting engine how that should be treated (if that should absorb the light)