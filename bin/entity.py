import pygame
from pygame.math import Vector2
from typing import Optional
from uuid import uuid4, UUID

from bin.abstractClasses import Executor, Loggable, EventType
# from bin.map import Chunk, Scene # can't import this because i need to import this to map to restore chunks...
from bin.event import Event


# basics of entity, i'm to lazy to continue this now. I need to rewrite how chunk are actived and add some delay and force loading to make able entities going into "unloaded" chunks and i also need to rewrite system to bind entities as "chunk loading entities"
class Entity(pygame.sprite.Sprite, Executor, Loggable):
    def getChunk(self) -> 'Chunk':
        return self.__chunk
    def getScene(self) -> 'Scene':
        return self.__chunk.getScene()
    
    def getUuid(self) -> UUID:
        return self.__uuid
    
    def getCords(self) -> Vector2:
        return self.__cords
    
    def moveBy(self, howMuch: Vector2) -> Vector2:
        pass
    
    def __init__(self, chunk: 'Chunk', cords: Vector2, forcedUUID = Optional[int] = None):
        super().__init__()
        
        self.__chunk = chunk
        self.__cords = cords
        self.__uuid: UUID = uuid4()
        
    