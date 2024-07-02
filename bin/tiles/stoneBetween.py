from pygame import Surface, Vector2
from bin.map import Block
from bin.map import Chunk



class stoneBetween(Block):
    MAINTEXTURE = "stone_between.png"
    ID = "stone_between"
    IDInt = "5"
    def __init__(self, image: Surface, cords: Vector2, chunk: Chunk) -> None:
        super().__init__(image, cords, chunk)