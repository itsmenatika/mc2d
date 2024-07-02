from pygame import Surface, Vector2
from bin.map import Block
from bin.map import Chunk



class oakWood(Block):
    MAINTEXTURE = "oak_wood.png"
    ID = "oak_wood"
    IDInt = "8"
    def __init__(self, image: Surface, cords: Vector2, chunk: Chunk) -> None:
        super().__init__(image, cords, chunk)