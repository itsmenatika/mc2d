from pygame.math import Vector2
from bin.map import Block, Chunk

def getBlockPosAbsFromCords(cords: Vector2) -> tuple[int,int]:
    return (cords.x // Block.SIZE.x, cords.y // Block.SIZE.y)

def getChunkPosFromCords(cords: Vector2) -> int:
    return cords.x // Chunk.SIZE.x