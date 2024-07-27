import pygame
from pygame.math import Vector2
from typing import Optional
from enum import Enum
from uuid import uuid4, UUID
import asyncio

from bin.abstractClasses import Executor, EventType
# from bin.map import Chunk, Scene # can't import this because i need to import this to map to restore chunks...
from bin.event import Event
from bin.logger import ParentForLogs, Loggable




class entityType(Enum):
    player = "player"
    falling_block = "falling_block"
    
    


# basics of entity, i'm to lazy to continue this now. I need to rewrite how chunk are actived and add some delay and force loading to make able entities going into "unloaded" chunks and i also need to rewrite system to bind entities as "chunk loading entities"
class Entity(pygame.sprite.Sprite, Executor, Loggable):
    basicGravity = Vector2(0, 0.49) # 20 times per second (one tick) (that's 9.8/m2s)
    
    
    async def tick(self):
        # print(self.rect)
        print(self.detectColission())
    
    def getChunk(self) -> 'Chunk':
        return self.__chunk
    
    
    def detectColission(self) -> list:
        sceneSprites: pygame.sprite.Group = self.getScene().sprites()
        
        return pygame.sprite.spritecollide(self, sceneSprites, False)
    
    def isPartOfTheChunk(self, chunk: 'Chunk') -> bool:
        return chunk.isEntityPartOfTheChunk(self)
    
    def getScene(self) -> 'Scene':
        return self.__chunk.getScene()
    
    def getUuid(self) -> UUID:
        return self.__uuid
    
    def getCords(self) -> Vector2:
        return self.rect.topleft
    
    def moveBy(self, howMuch: Vector2) -> Vector2:
        pass
    
    def __init__(self, image: pygame.surface.Surface, chunk: 'Chunk', cords: Vector2, oftype: entityType, forcedUUID: Optional[int] = None, nbtData: Optional[dict] = None):
        super().__init__()
        self.__game = chunk.getGame()
        self.image = image
        self.__chunk = chunk
        self.__cords, self.__velocity, self.__accelaration = cords, Vector2(0,0), Vector2(0,0)
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.__cords
        
        if forcedUUID == None:
            self.__uuid: UUID = uuid4()
        else: self.__uuid = forcedUUID
        
        if nbtData == None:
            self.__nbtData: dict = {}
        else: self.__nbtData = nbtData
        
        
        self.__type = oftype
        self.setLogParent(parentForLogs=ParentForLogs(name=f"entity_{self.__uuid}", parent=self.__game.getLogParent()))
        
    