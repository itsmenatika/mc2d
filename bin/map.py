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
from bin.abstractClasses import Executor, WorldGenerator

class chunkNotLoaded(Exception): pass

class Chunk(pygame.sprite.Group, Executor):
    SIZE = Vector2(16,360)
    
    '''You have to also remove this chunk from list of actived chunks (python reasons). If you don't wanna mess with this just use map.unloadChunk(chunk) instead!'''
    def unload(self) -> None:
        self.save()
        self.getScene().remove(self.sprites())
        self.empty()
        
    def save(self) -> None:
        pass
        # self.getScene().chunkCache[self.getChunkPos()] = self
    
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
    
    
    # def generateHeight(self, x, chunkPos: list[int,int], seedInt: int,  cache: dict, fromLeft: bool = False, startPoint: int = 10,
    #                    max: Optional[int] = None, min: Optional[int] = None, probability: int = 60, seedName: str = "global") -> int:  
    #     _s = seedInt % 10
    #     _xAbsolute = x + chunkPos[0] * Chunk.SIZE.x
        
    #     if _xAbsolute in cache: return cache[_xAbsolute]
    #     if _xAbsolute == 0: return startPoint
        
    #     if x + (chunkPos[0] + 1) * Chunk.SIZE.x not in cache and not fromLeft:
    #         return self.generateHeight(x, chunkPos, seedInt, cache, True, startPoint=startPoint, max=max, min=min, probability=probability, seedName=seedName)
        
        
    #     random.seed(f"${self.getScene().getSeed()}_CHUNK_{self.getChunkPos()}_h{seedName}_${x}")
        
    #     wannabe = random.randint(0,100)
    #     howmuch = random.randint(-1,1)
        
    #     random.seed(f"${self.getScene().getSeed()}_CHUNK_{self.getChunkPos()}")
        
    #     if fromLeft:
    #         if x < 0:
    #             chunkPos[0] += 1
    #             return self.generateHeight(x, chunkPos, seedInt, cache, True, startPoint=startPoint, max=max, min=min, probability=probability, seedName=seedName)
            
    #         _n = self.generateHeight(x - 1, chunkPos, seedInt, cache, True, startPoint=startPoint, max=max, min=min, probability=probability, seedName=seedName)
    #         if(wannabe > probability):
    #             _n += howmuch      
            
            
    #         if min is not None and _n < min:
    #             _n = min
    #         elif max is not None and _n > max:
    #             _n = max
                
    #         cache[_xAbsolute] = _n
    #         return _n
            
            
            
        
    #     while x > Chunk.SIZE.x:
    #         x -= Chunk.SIZE.x
    #         chunkPos[0] += 1
        
    #     _n = self.generateHeight(x + 1, chunkPos, seedInt, cache, False,  startPoint=startPoint, max=max, min=min, probability=probability, seedName=seedName)
    #     if(wannabe > probability):
    #         _n += howmuch
            
    #     if min is not None and _n < min:
    #         _n = min
    #     elif max is not None and _n > max:
    #         _n = max
            
    #     cache[_xAbsolute] = _n
        
    #     return _n
      
            
    
    def height(self, x, chunkPos: tuple[int,int], seedInt: int) -> int:
        print(seedInt)
    
    def generateChunk(self) -> None:
        random.seed(f"${self.getScene().getSeed()}_CHUNK_{self.getChunkPos()}")
        
        for x in range(0,int(Chunk.SIZE.x)):
            height = self.generateHeight(x, list(self.getChunkPos()), self.getScene().getSeedInt(), self.getScene().heightCache['grass_height'], False, min=6, max=16, seedName="height")
            self.__blocks[(x,height)] = Block.newBlockByResourceManager(
                chunk=self,
                name="grass_block",
                cordsRelative=Vector2(x * Block.SIZE.x,height * Block.SIZE.y),
                executor=self,
                reason="world_generator"
            )
            
            dirtheight = self.generateHeight(x, list(self.getChunkPos()), self.getScene().getSeedInt(), self.getScene().heightCache['dirt_height'], False, startPoint=4, max=5, min=3, seedName="dirtheight")
            

            
            for y in range(0,dirtheight):
                self.__blocks[(x,height+y+1)] = Block.newBlockByResourceManager(
                    chunk=self,
                    name="dirt",
                    cordsRelative=Vector2(x * Block.SIZE.x,(height + 1 + y) * Block.SIZE.y),
                    executor=self,
                    reason="world_generator"
                )
                
            currentHeight = height + dirtheight + 1
            for y in range(0,30):
                self.__blocks[(x,y+currentHeight)] = Block.newBlockByResourceManager(
                    chunk=self,
                    name="stone",
                    cordsRelative=Vector2(x * Block.SIZE.x,(y + currentHeight) * Block.SIZE.y),
                    executor=self,
                    reason="world_generator"
                ) 
                if y + currentHeight >= 32:   
                    bedrockHeight = self.generateHeight(x, list(self.getChunkPos()), self.getScene().getSeedInt(), self.getScene().heightCache['bedrock_height'], False, startPoint=2, max=2, min=1, probability=20)
                    
                    if bedrockHeight == 1:
                        self.__blocks[(x,y+currentHeight + 1)] = Block.newBlockByResourceManager(
                            chunk=self,
                            name="stone",
                            cordsRelative=Vector2(x * Block.SIZE.x,(y + currentHeight + 1) * Block.SIZE.y),
                            executor=self,
                            reason="world_generator"
                        )
                        self.__blocks[(x,y+currentHeight + 2)] = Block.newBlockByResourceManager(
                            chunk=self,
                            name="bedrock",
                            cordsRelative=Vector2(x * Block.SIZE.x,(y + currentHeight + 2) * Block.SIZE.y),
                            executor=self,
                            reason="world_generator"
                        ) 
                    else:
                        self.__blocks[(x,y+currentHeight + 1)] = Block.newBlockByResourceManager(
                            chunk=self,
                            name="bedrock",
                            cordsRelative=Vector2(x * Block.SIZE.x,(y + currentHeight + 1) * Block.SIZE.y),
                            executor=self,
                            reason="world_generator"
                        )
                        self.__blocks[(x,y+currentHeight + 2)] = Block.newBlockByResourceManager(
                            chunk=self,
                            name="bedrock",
                            cordsRelative=Vector2(x * Block.SIZE.x,(y + currentHeight + 2) * Block.SIZE.y),
                            executor=self,
                            reason="world_generator"
                        ) 
                    break
        
        veins = 5
        while veins > 0:
            veins -= 1
            x = random.randint(0,Chunk.SIZE.x)
            y = random.randint(currentHeight+3, 32)
            
            self.__blocks[(x,y)] = Block.newBlockByResourceManager(
                chunk=self,
                name="coal_ore",
                cordsRelative=Vector2(x * Block.SIZE.x,y * Block.SIZE.y),
                executor=self,
                reason="world_generator"
            ) 
            
            howmuch = random.randint(0,3)
            
            choices = [[1,0], [-1,0], [0,1], [0,-1]]
            while howmuch > 0:
                if len(choices) == 0: break
                
                addx, addy = random.choice(choices)
                choices.remove([addx,addy])
                if x+addx > 16:
                    self.getScene().blockToNextCache((self.getChunkPos()[0]+1, self.getChunkPos()[1]))
                    howmuch -= 1
                    continue
                elif x+addx < 0:
                    self.getScene().blockToNextCache((self.getChunkPos()[0]-1, self.getChunkPos()[1]))
                    howmuch -= 1
                    continue
                
                if (x+addx, y+addy) in self.__blocks:
                    if self.__blocks[(x+addx, y+addy)].ID != "stone": continue
                    
                    self.__blocks[(x+addx,y+addy)] = Block.newBlockByResourceManager(
                        chunk=self,
                        name="coal_ore",
                        cordsRelative=Vector2(x * Block.SIZE.x,y * Block.SIZE.y),
                        executor=self,
                        reason="world_generator"
                    ) 
                    
                    x += addx
                    y += addy
                    
                    howmuch -= 1
                    
            
            
                

            
            
                
                
                
            
        
    


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
        
        self.__endPoint = self.__startPoint + Chunk.SIZE
        
  
        
        # self.__blocks: dict[tuple[int,int], Block] = {}
        
        
        # self.loadChunkFromCsv("test.csv")
        # self.generateChunk()
        self.__blocks: dict[tuple[int,int], Block] = self.getScene().getWorldGenerator().generateChunk(
            chunkPos=self.__chunkPos,
            chunk=self,
            Scene=self.__map
        )  
        


class Block(pygame.sprite.Sprite):
    MAINTEXTURE: str | None = None
    ID: str | None = None
    IDInt: int|None = None
    
    
    SIZE = Vector2(32,32)
    
    
    '''Method executed when chunk is generated'''
    def onGenerate(self, cordsRelative: Vector2, cordsAbsolute: Vector2, inChunkPosition: tuple[int,int], chunk: Chunk):
        pass

    '''Method executed when chunk is loaded'''
    def onLoad(self, cordsRelative: Vector2, cordsAbsolute: Vector2, inChunkPosition: tuple[int,int], chunk: Chunk):
        pass
    
    '''Returns cords relative to chunk starting Points'''
    def getCordsRelative(self) -> Vector2:
        return self.__cords
    
    '''Returns cords'''
    def getCords(self) -> Vector2:
        return self.__cordsAbsolute
    
    def getInChunkPosition(self) -> tuple[int,int]:
        return (int(self.__cords.x / Block.SIZE.x),
                int(self.__cords.y / Block.SIZE.y))
        
    '''Create new block using resourceManager'''
    @staticmethod
    def newBlockByResourceManager(chunk: Chunk, name: str, cordsRelative: Optional[Vector2] = None, executor: Optional[Executor] = None, reason: Optional[str] = None) -> 'Block':
        rm = chunk.getScene().getGame().getResourceManager()
        
        if cordsRelative == None:
            cords = Vector2(0,0)
            
        blockInfo = rm.getBlockInformation(name)
        
        return blockInfo['class'](
            image=rm.getTexture(blockInfo['class'].MAINTEXTURE),
            cordsRelative=cordsRelative,
            chunk=chunk,
            executor = executor,
            reason=reason
        )
        
    
    def getChunk(self) -> Chunk:
        return self.__chunk
    
    def getScene(self) -> 'Scene':
        return self.__chunk.getScene()
    
    def __init__(self, image:pygame.surface.Surface, cordsRelative: Vector2, chunk: Chunk, executor: Optional[Executor] = None, reason: Optional[str] = None) -> None:
        super().__init__(chunk,chunk.getScene())
        self.__chunk = chunk
        self.image = image
        self.__cords: Vector2 = cordsRelative
        self.__cordsAbsolute: Vector2 = Vector2(cordsRelative.x + self.__chunk.getStartingPoint().x,
                                        cordsRelative.y + self.__chunk.getStartingPoint().y)
        
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.topleft = self.__cordsAbsolute
        
        self.doRender = True
        
        if reason=="world_generator":
            inChunkPosition = (int(self.__cords.x / Block.SIZE.x),
                               int(self.__cords.y / Block.SIZE.y))
            self.onGenerate(cordsAbsolute=self.__cordsAbsolute,cordsRelative=self.__cords, inChunkPosition=inChunkPosition, chunk=chunk)
        elif reason == "chunk_load":
            inChunkPosition = (int(self.__cords.x / Block.SIZE.x),
                               int(self.__cords.y / Block.SIZE.y))
            self.onLoad(cordsAbsolute=self.__cordsAbsolute,cordsRelative=self.__cords, inChunkPosition=inChunkPosition, chunk=chunk)
            

# class dupa(): pass
class Scene(pygame.sprite.Group):    
    RENDERDISTANCE = 3
    
    async def tick(self) -> None:
        # aha = dupa()
        # aha.rect = pygame.rect.Rect(pygame.mouse.get_pos()[0]-self.getGame().camera.cords.x,pygame.mouse.get_pos()[1]-self.getGame().camera.cords.y,1,1)
        # print(pygame.sprite.spritecollide(aha, self.sprites(), False))
        
        
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
        
    def getSeed(self) -> str:
        return self.__seed
    
    def getSeedInt(self) -> int:
        return self.__seedInt
    
    def getWorldGenerator(self) -> WorldGenerator:
        return self.__worldGenerator
    
    def __init__(self, game: 'Game', name: str, worldGenerator: WorldGenerator, autoAdd: bool = True, inIdle: bool = False, seed: str = "uwusa") -> None:
        super().__init__()
        
        self.heightCache = {
            "grass_height": {},
            "dirt_height": {},
            "bedrock_height": {}
        }
        
        self.blockToNextCache = {
            
        }
        
        # info
        self.__game: 'Game' = game
        self.__autoAdd: bool = autoAdd
        self.__name: str = name
        self.idle: bool = inIdle
        self.__seed, self.__seedInt = seed, int("".join([str(ord(char)) for char in seed]))
        self.__worldGenerator = worldGenerator(self)
       
        
        self.__activeChunks: dict[tuple[int,int], Chunk] = {}
        
        for x in range(3):
            self.__activeChunks[(x,0)] = Chunk(map=self, chunkPos=(x,0)) 
                 
        if autoAdd:
            self.__game.addScene(scene=self, name=self.__name)
            
        
            
        
            
