from pygame import Surface, Vector2
from bin.map import Block
from bin.map import Chunk



class bedrock(Block):
    MAINTEXTURE = "bedrock.png"
    ID = "bedrock"
    IDInt = 8
    def __init__(self, image: Surface, cords: Vector2, chunk: Chunk) -> None:
        super().__init__(image, cords, chunk)