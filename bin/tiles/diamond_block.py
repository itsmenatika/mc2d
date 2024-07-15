from pygame import Surface, Vector2
from bin.map import Block
from bin.map import Chunk
from bin.abstractClasses import Executor


class diamond_block(Block):
    MAINTEXTURE = "tiles/diamond_block.png"
    MAINTEXTUREISTRANSPARENT = False
    ID = "diamond_block"
    IDInt = 12
    def __init__(self, image: Surface, blockPos: Vector2, chunk: Chunk, executor: Executor | None = None, reason: str | None = None, addToEverything: bool = True) -> None:
        super().__init__(image, blockPos, chunk, executor, reason, addToEverything)