from pygame import Surface, Vector2
from bin.map import Block
from bin.map import Chunk
from bin.abstractClasses import Executor



class grass_block(Block):
    MAINTEXTURE = "tiles/grass.png"
    MAINTEXTUREISTRANSPARENT = False
    ID = "grass_block"
    IDInt = 2
    def __init__(self, image: Surface, blockPos: Vector2, chunk: Chunk, executor: Executor | None = None, reason: str | None = None, addToEverything: bool = True) -> None:
        super().__init__(image, blockPos, chunk, executor, reason, addToEverything)