from pygame import Surface, Vector2
from bin.map import Block
from bin.map import Chunk



class grassBetween(Block):
    MAINTEXTURE = "grass_between.png"
    ID = "grass_between"
    IDInt = "4"
    def __init__(self, image: Surface, cords: Vector2, chunk: Chunk) -> None:
        super().__init__(image, cords, chunk)