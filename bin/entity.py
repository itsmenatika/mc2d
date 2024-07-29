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
    maxSpeed = Vector2(5, 5)
    dividingFactor = 2 # the smaller factor the more accurate physics but also the slower
    
    
    async def tick(self):
        # basic adding
        
        # check if entity has any velocity
        if abs(self.__velocity.x) > 0 or abs(self.__velocity.y) > 0:
            # copy velocity to divide it into smaller parts in the future (temp will function as remaining part to add)
            temp: Vector2 = self.__velocity.copy()
            
            # execute till there's at least one part to divide
            while abs(temp.x) > 0 or abs(temp.y)  > 0:
                # get parts
                divingFactorX: int = min(self.dividingFactor, temp.x) if temp.x > 0 else max(-self.dividingFactor, temp.x)
                divingFactorY: int = min(self.dividingFactor, temp.y) if temp.y > 0 else max(-self.dividingFactor, temp.y)
            
                # remove from remaining
                temp.x -= divingFactorX
                temp.y -= divingFactorY
                
                # add everything to cords and then fix rect
                self.__cords.x += divingFactorX
                self.__cords.y += divingFactorY
                self.rect.midbottom = self.__cords
                
                # get list of collisions via pygame
                collisions: list = self.detectColission()
                
                # if there's any collision
                if len(collisions) > 1:
                    # loop through them
                    for col in collisions:
                        # if collision wasn't with itself
                        if col is self: continue
                        
                        # check if collision was (bottom me, you top)
                        if abs(self.rect.bottom - col.rect.top) < 5:
                            if self.__velocity.y > 0: 
                                self.__velocity.y = 0
                                temp.y = 0
                            self.rect.bottom = col.rect.top 
                            
                        # check if collision was (bottom you, me top)
                        if abs(self.rect.top - col.rect.bottom) < 5:
                            if self.__velocity.y < 0: 
                                self.__velocity.y = 0
                                temp.y = 0
                            self.rect.top = col.rect.bottom 
                            
                        # check if collision was (right me, you left)
                        if abs(self.rect.right - col.rect.left) < 5:
                            if self.__velocity.x > 0:
                                self.__velocity.x = 0
                                temp.x = 0
                            self.rect.right = col.rect.left
                            
                        # check if collision was (left me, you right)
                        if abs(self.rect.left - col.rect.right) < 5:
                            if self.__velocity.x < 0:
                                self.__velocity.x = 0
                                temp.x = 0
                            self.rect.left = col.rect.right
                            
                    # repair rect
                    self.repairCordsFromRect()
                        
        # adding velocity from gravity
        self.__velocity += self.basicGravity
        
        # TODO: checking if object got outside map
        
        
        # max speed
        if abs(self.__velocity.x) > self.maxSpeed.x:
            self.__velocity.x = self.maxSpeed.x if self.__velocity.x > 0 else  -self.maxSpeed
            # if self.__velocity.x > 0: self.__velocity.x = self.maxSpeed.x
            # else: self.__velocity.x = -self.maxSpeed.x
        
        if abs(self.__velocity.y) > self.maxSpeed.y:
            self.__velocity.y = self.maxSpeed.y if self.__velocity.y > 0 else  -self.maxSpeed        
            # if self.__velocity.y > 0: self.__velocity.y = self.maxSpeed.y
            # else: self.__velocity.y = -self.maxSpeed.y
        
        
    
    def getChunk(self) -> 'Chunk':
        return self.__chunk
    
    
    def detectColission(self) -> list:
        sceneSprites: pygame.sprite.Group = self.getScene().mainBlocks.sprites()
        entitySprites = pygame.sprite.Group = self.getScene().entityGroup.sprites()
        
        return pygame.sprite.spritecollide(self, sceneSprites, False) + pygame.sprite.spritecollide(self, entitySprites, False)
    
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
    
    def repairCordsFromRect(self) -> None:
        self.__cords: Vector2 = Vector2(self.rect.midbottom)
    
    def __init__(self, image: pygame.surface.Surface, chunk: 'Chunk', cords: Vector2, oftype: entityType, forcedUUID: Optional[int] = None, nbtData: Optional[dict] = None):
        super().__init__()
        self.__game = chunk.getGame()
        self.image = image
        self.__chunk = chunk
        self.__cords, self.__velocity, self.__accelaration = cords, Vector2(0,0), Vector2(0,0)
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.__cords
        
        self.__uuid = forcedUUID if forcedUUID != None else uuid4()

        self.__nbtData = nbtData if nbtData != None else {}
        
        self.__type = oftype
        self.setLogParent(parentForLogs=ParentForLogs(name=f"entity_{self.__uuid}", parent=self.__game.getLogParent()))
        
    