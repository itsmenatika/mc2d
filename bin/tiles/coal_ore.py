from pygame import Surface, Vector2
from bin.map import Block
from bin.map import Chunk
from bin.abstractClasses import Executor


class coal_ore(Block):
    MAINTEXTURE = "coal.png"
    ID = "coal_ore"
    IDInt = 6
    def __init__(self, image: Surface, cordsRelative: Vector2, chunk: Chunk, executor: Executor | None = None, reason: str | None = None) -> None:
        super().__init__(image, cordsRelative, chunk, executor, reason)