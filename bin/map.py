# from bin import Game
from typing import Iterable
import pygame
from pygame.math import Vector2
from pygame.sprite import AbstractGroup
import csv
import os
import asyncio
import random
# from bin.camera import Camera


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
        grass = pygame.image.load("grass.png").convert_alpha()
        coal = pygame.image.load("coal.png").convert_alpha()
        stone = pygame.image.load("stone.png").convert_alpha()
        stone_between = pygame.image.load("stone_between.png").convert_alpha()
        grass_between = pygame.image.load("grass_between.png").convert_alpha()
        dirt = pygame.image.load("dirt.png").convert_alpha()
        # test.fill((100,100,100))
        
        for x in range(0,int(Chunk.SIZE.x+1)):
            height = random.randint(0,1)
            
            self.__blocks[(x, 10+height)] = Block(
                            image=grass, 
                            cords=Vector2(x * Block.SIZE.x, (10+height) * Block.SIZE.y), 
                            chunk=self)


            self.__blocks[(x, 11+height)] = Block(
                            image=dirt, 
                            cords=Vector2(x * Block.SIZE.x, (11+height) * Block.SIZE.y), 
                            chunk=self)       
            
            self.__blocks[(x, 12+height)] = Block(
                image=dirt, 
                cords=Vector2(x * Block.SIZE.x, (12+height) * Block.SIZE.y), 
                chunk=self)       

            self.__blocks[(x, 13+height)] = Block(
                            image=grass_between, 
                            cords=Vector2(x * Block.SIZE.x, (13+height) * Block.SIZE.y), 
                            chunk=self)            

            self.__blocks[(x, 14+height)] = Block(
                            image=stone_between, 
                            cords=Vector2(x * Block.SIZE.x, (14+height) * Block.SIZE.y), 
                            chunk=self)    

            # self.__blocks[(x, 13+height)] = Block(
            #                 image=stone, 
            #                 cords=Vector2(x * Block.SIZE.x, (10+height) * Block.SIZE.y), 
            #                 chunk=self) 
            
            for y in range(15+height,35):
                if 1 == random.randint(0,60):
                    self.__blocks[(x, y)] = Block(
                                image=coal, 
                                cords=Vector2(x * Block.SIZE.x, y * Block.SIZE.y), 
                                chunk=self)                    
                else:
                    self.__blocks[(x, y)] = Block(
                                image=stone, 
                                cords=Vector2(x * Block.SIZE.x, y * Block.SIZE.y), 
                                chunk=self)
    
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
            chunkPos[0] * Chunk.SIZE.x * Block.SIZE.x + 1,
            chunkPos[1] * Chunk.SIZE.y * Block.SIZE.y + 1
        )
        
  
        
        self.__blocks: dict[tuple[int,int], Block] = {}
        
        
        # self.loadChunkFromCsv("test.csv")
        self.generateChunk()
        
        


class Block(pygame.sprite.Sprite):
    SIZE = Vector2(32,32)
    
    '''Returns cords relative to chunk starting Points'''
    def getCordsRelative(self) -> Vector2:
        return self.__cords
    
    '''Returns cords'''
    def getCords(self) -> Vector2:
        return self.__cordsAbsolute
        
        
    
    def getChunk(self) -> Chunk:
        return self.__chunk
    
    def getScene(self) -> 'Scene':
        return self.__chunk.getScene()
    
    def __init__(self, image:pygame.surface.Surface, cords: Vector2, chunk: Chunk) -> None:
        super().__init__(chunk,chunk.getScene())
        self.__chunk = chunk
        self.image = image
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.topleft = cords
        self.__cords: Vector2 = cords
        self.__cordsAbsolute: Vector2 = Vector2(cords.x + self.__chunk.getStartingPoint().x,
                                        cords.y + self.__chunk.getStartingPoint().y,)
        self.doRender = True

class Scene(pygame.sprite.Group):    
    RENDERDISTANCE = 3
    
    async def tick(self) -> None:
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
    
    def __init__(self, game: 'Game', name: str, autoAdd: bool = True, inIdle: bool = False) -> None:
        super().__init__()
        
        # info
        self.__game: 'Game' = game
        self.__autoAdd: bool = autoAdd
        self.__name: str = name
        self.idle: bool = inIdle
        
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