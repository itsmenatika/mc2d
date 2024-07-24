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
    
    def __init__(self, image: Surface, blockPos: Vector2, chunk: Chunk, executor: Executor | None = None, reason: str | None = None, addToEverything: bool = True) -> None:
        super().__init__(image, blockPos, chunk, executor, reason, addToEverything)