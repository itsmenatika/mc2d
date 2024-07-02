# from bin import Game
from typing import Iterable, Optional
import pygame
from pygame.math import Vector2
from pygame.sprite import AbstractGroup
import csv
import os
import asyncio
import random
# from bin.camera import Camera
from functools import reduce


class chunkNotLoaded(Exception): pass

class Chunk(pygame.sprite.Group):
    SIZE = Vector2(16,360)
    
    '''You have to also remove this chunk from list of actived chunks (python reasons). If you don't wanna mess with this just use map.unloadChunk(chunk) instead!'''
    def unload(self) -> None:
        self.save()
        self.getScene().remove(self.sprites())
        self.empty()
        
    def save(self) -> None:
        pass
    
    def getScene(self) -> 'Scene':
        return self.__map
    
    def iterateByBlock(self): 
        return enumerate(self.__blocks)
    
    def getStartingPoint(self) -> Vector2:
        return self.__startPoint
    
    def getEndingPoint(self) -> Vector2:
        return self.__endPoint
    
    def getChunkPos(self) -> tuple[int,int]:
        return self.__chunkPos
    
    def generateChunk(self) -> None:
        random.seed(f"${self.getScene().getSeed()}_CHUNK_{self.getChunkPos()}")
        
        heightCounter = 0
        treeCounter = 0
        height = 0
        
        for x in range(0,int(Chunk.SIZE.x)):
            heightCounter += 1
            if random.randint(0,100) > 90:
                heightCounter = 0
                height += random.randint(-1,1)
                if random.randint(0,100) > 90:
                    height += random.randint(0,3)
            elif heightCounter > 4 and random.randint(0,100) > 50:
                heightCounter = 0
                height += random.randint(-1,1)
                if random.randint(0,100) > 90:
                    height += random.randint(0,3)
                    
            if treeCounter > 3 and random.randint(0,3) == 1:
                treeCounter = 0
                self.__blocks[(x,9+height)] = Block.newBlockByResourceManager(
                        chunk=self,
                        name="oak_wood",
                        cords=Vector2(x * Block.SIZE.x, (9+height) * Block.SIZE.y)
                    )  
                self.__blocks[(x,8+height)] = Block.newBlockByResourceManager(
                        chunk=self,
                        name="oak_wood",
                        cords=Vector2(x * Block.SIZE.x, (8+height) * Block.SIZE.y)
                    )  
                self.__blocks[(x,7+height)] = Block.newBlockByResourceManager(
                        chunk=self,
                        name="oak_wood",
                        cords=Vector2(x * Block.SIZE.x, (7+height) * Block.SIZE.y)
                    ) 
            
            treeCounter += 1
                
                
            
            self.__blocks[(x,10+height)] = Block.newBlockByResourceManager(
                        chunk=self,
                        name="grass_block",
                        cords=Vector2(x * Block.SIZE.x, (10+height) * Block.SIZE.y)
                    )  


            self.__blocks[(x,11+height)] = Block.newBlockByResourceManager(
                        chunk=self,
                        name="dirt",
                        cords=Vector2(x * Block.SIZE.x, (11+height) * Block.SIZE.y)
                    )  
            
            self.__blocks[(x,12+height)] = Block.newBlockByResourceManager(
                        chunk=self,
                        name="dirt",
                        cords=Vector2(x * Block.SIZE.x, (12+height) * Block.SIZE.y)
                    )      

            self.__blocks[(x,13+height)] = Block.newBlockByResourceManager(
                        chunk=self,
                        name="grass_between",
                        cords=Vector2(x * Block.SIZE.x, (13+height) * Block.SIZE.y)
                    )             

            self.__blocks[(x,14+height)] = Block.newBlockByResourceManager(
                        chunk=self,
                        name="stone_between",
                        cords=Vector2(x * Block.SIZE.x, (14+height) * Block.SIZE.y)
                    )    

            # self.__blocks[(x, 13+height)] = Block(
            #                 image=stone, 
            #                 cords=Vector2(x * Block.SIZE.x, (10+height) * Block.SIZE.y), 
            #                 chunk=self) 
            
            for y in range(15+height,35):
                if 1 == random.randint(0,60):
                    self.__blocks[(x,y)] = Block.newBlockByResourceManager(
                        chunk=self,
                        name="coal_ore",
                        cords=Vector2(x * Block.SIZE.x, y * Block.SIZE.y)
                    )                 
                else:
                    self.__blocks[(x,y)] = Block.newBlockByResourceManager(
                        chunk=self,
                        name="stone",
                        cords=Vector2(x * Block.SIZE.x, y * Block.SIZE.y)
                    )
                    # self.__blocks[(x, y)] = Block(
                    #             image=stone, 
                    #             cords=Vector2(x * Block.SIZE.x, y * Block.SIZE.y), 
                    #             chunk=self)
    
    def loadChunkFromCsv(self, csvSource: str) -> None:
        with open(csvSource) as csvFile:
            data = csv.reader(csvFile, delimiter=",")
            
            for y, row in enumerate(data):
                for x, blockData in enumerate(row):
                    test = pygame.surface.Surface((32,32)).convert_alpha()
                    test.fill((100,100,100))
                    # block(test, self.__activeChunks[(0,0)])
                    test2 = pygame.surface.Surface((32,32)).convert_alpha()
                    test2.fill((0,0,0))
                    match blockData:
                        case '22':
                            self.__blocks[(x, y)] = Block(
                                image=test.copy(), 
                                cords=Vector2(x * Block.SIZE.x, y * Block.SIZE.y), 
                                chunk=self)
                        case '-1':
                                t = self.__blocks[(x, y)] = Block(
                                image=test2.copy(), 
                                cords=Vector2(x * Block.SIZE.x, y * Block.SIZE.y), 
                                chunk=self)
                                t.doRender = False
                                
                        
                    
    
    def getBlockByVector(self, cords: Vector2) -> 'Block':
        return self.__blocks[(cords.x,cords.y)] if (cords.x,cords.y) in self.__blocks else None
    
    def getBlockByTuple(self, cords: tuple | list) -> 'Block':
        return self.__blocks[(cords[0],cords[1])] if (cords[0],cords[1]) in self.__blocks else None
    
    def __init__(self, map: 'Scene', chunkPos: Vector2 = Vector2(0,0)) -> None:
        super().__init__()
        self.__map = map
        
        self.__chunkPos = chunkPos
        self.__startPoint = Vector2(
            chunkPos[0] * Chunk.SIZE.x * Block.SIZE.x,
            chunkPos[1] * Chunk.SIZE.y * Block.SIZE.y
        )
        
  
        
        self.__blocks: dict[tuple[int,int], Block] = {}
        
        
        # self.loadChunkFromCsv("test.csv")
        self.generateChunk()
        
        


class Block(pygame.sprite.Sprite):
    MAINTEXTURE: str | None = None
    ID: str | None = None
    IDInt: int|None = None
    
    
    SIZE = Vector2(32,32)
    
    '''Returns cords relative to chunk starting Points'''
    def getCordsRelative(self) -> Vector2:
        return self.__cords
    
    '''Returns cords'''
    def getCords(self) -> Vector2:
        return self.__cordsAbsolute
        
    '''Create new block using resourceManager'''
    @staticmethod
    def newBlockByResourceManager(chunk: Chunk, name: str, cords: Optional[Vector2] = None) -> 'Block':
        rm = chunk.getScene().getGame().getResourceManager()
        
        if cords == None:
            cords = Vector2(0,0)
            
        blockInfo = rm.getBlockInformation(name)
        
        return blockInfo['class'](
            image=rm.getTexture(blockInfo['class'].MAINTEXTURE),
            cords=cords,
            chunk=chunk
        )
        
    
    def getChunk(self) -> Chunk:
        return self.__chunk
    
    def getScene(self) -> 'Scene':
        return self.__chunk.getScene()
    
    def __init__(self, image:pygame.surface.Surface, cords: Vector2, chunk: Chunk) -> None:
        super().__init__(chunk,chunk.getScene())
        self.__chunk = chunk
        self.image = image
        self.__cords: Vector2 = cords
        self.__cordsAbsolute: Vector2 = Vector2(cords.x + self.__chunk.getStartingPoint().x,
                                        cords.y + self.__chunk.getStartingPoint().y)
        
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.topleft = self.__cordsAbsolute
        
        self.doRender = True

class dupa(): pass
class Scene(pygame.sprite.Group):    
    RENDERDISTANCE = 3
    
    async def tick(self) -> None:
        aha = dupa()
        aha.rect = pygame.rect.Rect(pygame.mouse.get_pos()[0]-self.getGame().camera.cords.x,pygame.mouse.get_pos()[1]-self.getGame().camera.cords.y,1,1)
        print(pygame.sprite.spritecollide(aha, self.sprites(), False))
        
        
        surfSize = pygame.display.get_surface().get_size()
        centerChunkPos = ((self.getGame().camera.cords.x + surfSize[0]) // Block.SIZE.x // Chunk.SIZE.x,
                     (self.getGame().camera.cords.y + surfSize[1]) // Block.SIZE.y // Chunk.SIZE.y)
        
        
        ChunksToBeLoaded: list[Chunk] = []
        
        ChunksToBeLoaded.extend([(x+centerChunkPos[0],0) for x in range(-self.RENDERDISTANCE, self.RENDERDISTANCE+1)])
        
       
        
        chunk: Chunk = None
        
        # unload chunks
        for chunkPos, chunk in self.__activeChunks.copy().items():
            if chunkPos not in ChunksToBeLoaded:
                self.unloadChunk(chunk)
        
        # load chunks
        # for newChunk in [chunk for chunk in ChunksToBeLoaded if chunk not in self.__activeChunks]: 
        for newChunkPos in [chunkPos for chunkPos in ChunksToBeLoaded if not self.isChunkActive(chunkPos)]:
            self.loadChunk(newChunkPos)
            
        # print(self.getGame().clock.get_fps(),len(self.__activeChunks), centerChunkPos, ChunksToBeLoaded)
        # pygame.time.Clock.ge
            
    def loadChunk(self, chunkPos: tuple[int,int]):
         self.__activeChunks[chunkPos] = Chunk(map=self, chunkPos=chunkPos) 
    
    def isChunkActive(self, chunkPos: tuple[int,int]) -> bool:
        return chunkPos in self.__activeChunks.keys()
    
    def getGame(self) -> 'Game':
        return self.__game
    
    def getName(self, forceGettingFromEngine: bool = False) -> str | None:
        if self.__name is not None and not forceGettingFromEngine:
            return self.__name
        else:
            if not self.__game.isSceneAdded(Scene):
                return None
            
            return self.__game.findNameOfScene(self)
        
    def getActiveChunks(self) -> dict[tuple[int,int], Chunk]:
        return self.__activeChunks
        
    # def draw(self):
    #     surf = self.__game.getDisplayOrginal()
    #     # for chunk in self.__activeChunks.values():
    #     #     chunk.draw(surf)
    #     self.camera.draw(self.get)
            
    
    def getBlock(self, cords: Vector2) -> Block:
        chunkCords = (cords.x // Chunk.SIZE.x, cords.y // Chunk.SIZE.y)
        chunkStartPoint = (Chunk.SIZE.x * chunkCords[0], Chunk.SIZE.y * chunkCords[1]) 
        RelativeBlockPos = ((cords.x - chunkStartPoint[0]) // Block.SIZE.y, 
                            (cords.y - chunkStartPoint[1]) // Block.SIZE.x)
        
        
        if chunkCords not in self.__activeChunks:
            raise chunkNotLoaded(f"Trying to access block of cords ${cords} which should be located in chunk ${chunkCords}, but that chunk is not loaded!")
        
        
        return self.__activeChunks[chunkCords].getBlockByTuple(RelativeBlockPos)
             
        
    def getChunk(self, chunkPos: tuple[int,int]) -> Chunk:
        if chunkPos not in self.__activeChunks:
            raise chunkNotLoaded(f"Chunk of cords ${chunkPos} is not loaded, can't access that chunk")
        return self.__activeChunks[chunkPos]
        
    def unloadChunk(self, chunk: Chunk) -> None:
        chunk.unload()
        del self.__activeChunks[chunk.getChunkPos()]
        
    def getSeed(self) -> None:
        return self.__seed
    
    def __init__(self, game: 'Game', name: str, autoAdd: bool = True, inIdle: bool = False, seed: str = "sus") -> None:
        super().__init__()
        
        # info
        self.__game: 'Game' = game
        self.__autoAdd: bool = autoAdd
        self.__name: str = name
        self.idle: bool = inIdle
        self.__seed, self.__seedInt = seed, int("".join([str(ord(char)) for char in seed]))
       
        
        self.__activeChunks: dict[tuple[int,int], Chunk] = {}
        
        for x in range(3):
            self.__activeChunks[(x,0)] = Chunk(map=self, chunkPos=(x,0)) 
            
        # self.unloadChunk(self.getChunk((1,0)))
        # self.unloadChunk(self.getChunk((0,0)))
        # self.unloadChunk(self.getChunk((2,0)))
            
        # print(self.__activeChunks[1,0].getBlockByTuple((0,0)).groups())

        
        # test = pygame.surface.Surface((200,200))
        # test.fill((100,100,100))
        # block(test, self.__activeChunks[(0,0)])
        
        
        
        if autoAdd:
            self.__game.addScene(scene=self, name=self.__name)
            
        
            
        # print(
        #     self.getBlock(Vector2(10,32))
        # )