from pygame import Surface, Vector2
from bin.map import Block
from bin.map import Chunk



class coalOre(Block):
    MAINTEXTURE = "coal.png"
    ID = "coal_ore"
    IDInt = "6"
    def __init__(self, image: Surface, cords: Vector2, chunk: Chunk) -> None:
        super().__init__(image, cords, chunk)