from pygame import Surface, Vector2
from bin.map import Block
from bin.map import Chunk
from bin.abstractClasses import Executor


class iron_block(Block):
    MAINTEXTURE = "tiles/iron_block.png"
    MAINTEXTUREISTRANSPARENT = False
    ID = "iron_block"
    IDInt = 13
    def __init__(self, image: Surface, blockPos: Vector2, chunk: Chunk, executor: Executor | None = None, reason: str | None = None, addToEverything: bool = True) -> None:
        super().__init__(image, blockPos, chunk, executor, reason, addToEverything)