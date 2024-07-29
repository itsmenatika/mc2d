import pygame
from pygame.math import Vector2


from bin.entity import Entity, entityType


class _example(Entity):
    ID = "id"
    
    def __init__(self, image: pygame.Surface, chunk: 'Chunk', cords: Vector2, oftype: entityType, forcedUUID: int | None = None, nbtData: dict | None = None):
        super().__init__(image, chunk, cords, oftype, forcedUUID, nbtData)