from pygame import Surface, Vector2
from bin.map import Block
from bin.map import Chunk
from bin.abstractClasses import Executor



class oakWood(Block):
    MAINTEXTURE = "oak_wood.png"
    ID = "oak_wood"
    IDInt = "8"
    def __init__(self, image: Surface, cordsRelative: Vector2, chunk: Chunk, executor: Executor | None = None, reason: str | None = None) -> None:
        super().__init__(image, cordsRelative, chunk, executor, reason)