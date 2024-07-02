from pygame import Surface, Vector2
from bin.map import Block
from bin.map import Chunk



class dirt(Block):
    MAINTEXTURE = "dirt.png"
    ID = "dirt"
    IDInt = "1"
    def __init__(self, image: Surface, cords: Vector2, chunk: Chunk) -> None:
        super().__init__(image, cords, chunk)