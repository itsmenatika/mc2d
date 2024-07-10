from pygame import Surface, Vector2
from bin.map import Block
from bin.map import Chunk
from bin.abstractClasses import Executor



class stone(Block):
    MAINTEXTURE = "stone.png"
    MAINTEXTUREISTRANSPARENT = False
    ID = "stone"
    IDInt = 3
    def __init__(self, image: Surface, blockPos: Vector2, chunk: Chunk, executor: Executor | None = None, reason: str | None = None) -> None:
        super().__init__(image, blockPos, chunk, executor, reason)