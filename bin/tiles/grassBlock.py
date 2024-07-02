from pygame import Surface, Vector2
from bin.map import Block
from bin.map import Chunk



class grassBlock(Block):
    MAINTEXTURE = "grass.png"
    ID = "grass_block"
    IDInt = "2"
    def __init__(self, image: Surface, cords: Vector2, chunk: Chunk) -> None:
        super().__init__(image, cords, chunk)