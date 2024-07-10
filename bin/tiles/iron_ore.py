from pygame import Surface, Vector2
from bin.map import Block
from bin.map import Chunk
from bin.abstractClasses import Executor


class iron_ore(Block):
    MAINTEXTURE = "iron_ore.png"
    MAINTEXTUREISTRANSPARENT = False
    ID = "iron_ore"
    IDInt = "10"
    def __init__(self, image: Surface, blockPos: Vector2, chunk: Chunk, executor: Executor | None = None, reason: str | None = None) -> None:
        super().__init__(image, blockPos, chunk, executor, reason)