from pygame import Surface, Vector2
from bin.map import Block
from bin.map import Chunk
from bin.abstractClasses import Executor



class stone_between(Block):
    MAINTEXTURE = "stone_between.png"
    ID = "stone_between"
    IDInt = 5
    def __init__(self, image: Surface, cordsRelative: Vector2, chunk: Chunk, executor: Executor | None = None, reason: str | None = None) -> None:
        super().__init__(image, cordsRelative, chunk, executor, reason)