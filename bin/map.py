# from bin import Game
from typing import Optional, TypeAlias, NoReturn
import pygame
from pygame.math import Vector2
from pygame.sprite import AbstractGroup
import csv
import os
import asyncio
import json
import random
# from bin.camera import Camera
from bin.abstractClasses import Executor, WorldGenerator, Reason
from bin.logger import Loggable, logType, ParentForLogs
# from bin.tools import getChunkPosFromCords



class chunkNotLoaded(Exception): pass

class Chunk(pygame.sprite.Group, Executor, Loggable):
    '''portion of the world of the size (16,360)'''
    SIZE = Vector2(16,360)

    def unload(self, previousData: Optional[dict] = None) -> dict:  
        '''You have to also remove this chunk from list of actived chunks (python reasons) and add new info to chunk save manually! If you don't wanna mess with this just use map.unloadChunk(self) or self.getScene().unloadChunk(self) instead! That is rather for more precise use than just simple unloading chunk!''' 
        self.log(logType.INFO, f"unloading chunk {self.getChunkPos()}...")
        
        _data = self.save(previousData=previousData)
        self.getScene().remove(self.sprites())
        self.empty()
        
        self.log(logType.SUCCESS, f"unloading chunk {self.getChunkPos()}... SUCCESS")

        return _data
        
    def save(self, previousData: Optional[dict] = None) -> dict:
        '''just saving chunk'''
        
        if previousData == None:
            previousData = {}
        
        self.log(logType.INFO, f"saving chunk {self.getChunkPos()}... (NOT DONE YET)")
        
        #  "gameVersionGenerated": 981,
        #     "gameVersionLastVisited": 312,
        #     "entities": {
        #         "UUID": {
        #             "cords": [12,12],
        #             "id": "twojamama",
        #             "entityData": {
        #                 "health": 0,
        #                 "max_health": 0,
        #                 "customName": "sus",
        #                 "customNameVisible": false,
        #                 "air": 0,
        #                 "max_air": 0,
        #                 "air_per_tick_addition": 0,
        #                 "air_per_tick_removal": 0
        #             }
        
        if 'gameVersionGenerated' not in previousData:
            previousData['gameVersionGenerated'] = 0
        
        chunkData = {
            "gameVersionGenerated": previousData['gameVersionGenerated'],
            "gameVersionLastVisited": 0,
            "blocks": [
                {
                    "id": Block.ID,
                    "idInt": Block.IDInt,
                    "blockPos": f"{str(int(blockPos[0]))}_{str(int(blockPos[1]))}"
                }
                for blockPos, Block in self.__blocks.items()
            ]
            
        }
        
        self.log(logType.SUCCESS, f"saving chunk {self.getChunkPos()}... SUCCESS")
        return chunkData
        # self.getScene().chunkCache[self.getChunkPos()] = self
    
    def getScene(self) -> 'Scene':
        return self.__scene
    
    def getGame(self) -> 'game':
        return self.__scene.getGame()
    
    def iterateByBlock(self) -> enumerate[tuple[int,int], 'Block']: 
        '''allows you to enumarate by blocks. That will option to use loop with tuple of (blockPos, block) per block'''
        return enumerate(self.__blocks)
    
    def getStartingPoint(self) -> Vector2:
        return self.__startPoint
    
    def getEndingPoint(self) -> Vector2:
        return self.__endPoint
    
    def getChunkPos(self) -> int:
        return int(self.__chunkPos)
    
    # not used but works, but very slow (NEED TO BE RECREATED!)
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
                                
                        
                    
    # i've tried either Union['Block', None] and 'block, None' and none of them was working. I don't know why. I leave it for python to figure out what type it would return
    def getBlockByVector(self, blockPosition: Vector2):
        '''allows you to get block by block Position relative to chunk (by Vector)\n
            Args:\n
                * blockPosition: pygame.math.Vector2 -> that vector2
            Returns:\n
                None | Block: result (None if no block found)'''
        return self.__blocks[(blockPosition.x,blockPosition.y)] if (blockPosition.x,blockPosition.y) in self.__blocks else None
 
    # i've tried either Union['Block', None] and 'block, None' and none of them was working. I don't know why. I leave it for python to figure out what type it would return   
    def getBlockByTuple(self, blockPosition: tuple[int,int]):
        '''allows you to get block by block Position relative to chunk (by tuple))\n
            Args:\n
                * blockPosition: tuple[int,int] -> that block position
            Returns:\n
                None | Block: result (None if no block found)'''
        return self.__blocks[(blockPosition[0],blockPosition[1])] if (blockPosition[0],blockPosition[1]) in self.__blocks else None
    
    
    def setBlock(self, blockPosition: tuple[int,int], block: 'Block | str | None', executor: Optional[Executor] = None, reason: Optional[str] = None) -> None:
        '''allows you to set block in specified chunk\n
            Args:\n
                * blockPosition: tuple -> block location relative to chunk
                * block: Block | str | None -> block. None = air (absence of block). giving string will result in using resource manager
                * executor: Optional[Executor] -> autor of this action (instance)
                * reason: Optional[str] -> reason why block will be set
            Returns:\n
                None | Block: result (None if no block found)'''
             
        # deleting previous
        if blockPosition in self.__blocks:
            self.__blocks[blockPosition].kill()
            del self.__blocks[blockPosition]
                
        if block == None: return
                
        # if using resource manager
        if type(block) == str:
            block = Block.newBlockByResourceManager(
                name=block,
                blockPos=blockPosition,
                executor=executor,
                reason=reason,
                chunk=self
            )
            
        self.__blocks[blockPosition] = block

            
        # for security reasons
        if not self.has(block): self.add(block)
        if not self.getScene().has(block): self.getScene().add(block)

        # deleting block if that will be replace with something else or just should be deleted
        # elif block == None or self.checkPositionForBlock(blockPosition):
        #         if blockPosition in self.__blocks:
        #             self.__blocks[blockPosition].kill()
        #             del self.__blocks[blockPosition]
        #         if block == None: return
           
        # setting block
         
        # print(block, type(block))
        # self.__blocks[blockPosition] = block
        # print(block)
        # try:
            
        # if not self.has(block): self.add(block)
        # if not self.getScene().has(block): self.getScene().add(block)
        # except Exception:
        #     print(block, type(block))
        
    def removeBlock(self, blockPosition: tuple[int,int], dontRaiseException: bool = False) -> None | NoReturn:
        '''allows you to remove block\n
            Args:\n
                * blockPosition: tuple -> block location relative to chunk
                * dontRaiseException: bool = False, 
            Returns:\n
                None | NoReturn'''
        if blockPosition not in self.__blocks:
            self.log(logType.ERROR, message=f"Couldn't find block {blockPosition} in the chunk of chunkPos {self.__chunkPos}!")
            if not dontRaiseException:
                raise Exception(f"Block wasn't found! {blockPosition} (chunkPos: {self.__chunkPos})")

        
        self.__blocks[blockPosition].kill()
        del self.__blocks[blockPosition]
        
    def setBlocksAbsolute(self, blocks: dict[tuple[int,int], 'Block']) -> None:
        '''allows to change all blocks at once. You should avoid using it at all costs!'''
        self.__blocks = blocks
        
    def setBlocks(self, blocks: dict[tuple[int,int], 'Block']) -> None:
        '''similar function to self.setBlockAbsolute() but more safe, because that only updates blocks'''
        self.__blocks.update(blocks)
        
    def checkPositionForBlock(self, blockPosition: tuple[int,int], block: Optional['Block | str'] = None, exactCopy: bool = False, nbtData: Optional[dict] = None) -> bool:
        '''check specified blockPos\n
            Args:\n
                * blockPosition: tuple -> specify block Position
                * block: Optional[Block | str] -> Block or block ID (optional). Use it if you want to check for specified block
                * exactCopy: bool = False -> require exact copy
                * nbtData: Optional[dict] -> check for specified nbt data (not implemented yet and idk when it would be or if it wil be)
            Returns:\n
                None | Block: result (None if no block found)'''
        
        # checking basics
        if blockPosition not in self.__blocks:
            return True if block in ['air', 'none'] else False
        if block == None: return True
        
        # exact copy
        if exactCopy:
            return True if self.__blocks[blockPosition] == block else False
        else:
            # the final logic
            # print(blockPosition not in self.__blocks, self.__blocks[blockPosition], block)
            return True if self.__blocks[blockPosition].ID == block.ID else False
        
    def __checkForErrorsWorldGeneratorAsyncio(self, task: asyncio.Task) -> None:
        print(task)
        try:
             _  = task.result()
             print(_)
        except Exception as e:
            print('gada', e)
            
    async def restoreChunkFromChunkData(self, chunkData: dict) -> None:
        try:
            # # blocks
            # blockPosSplit = []
            # for blockPosStr, blockData in chunkData['blocks'].items():
            #     blockPosSplit = blockPosStr.split("_")
            #     blockPos = (int(blockPosSplit[0]), int(blockPosSplit[1]))
            #     # print('s')
            #     self.setBlock(blockPos, blockData['id'], executor=self, reason=Reason.chunkRestore)
            
            
            howManyBlocks = len(chunkData['blocks'])
            
            blockData = chunkData['blocks']
            blockPos = []
            blockdict: dict = {}
            # blockPosSt = list
            for block in range(howManyBlocks):
                blockDict = blockData[block]
                blockPos = blockDict['blockPos'].split("_")
                blockPosSt = (int(blockPos[0]), int(blockPos[1]))
                Block.newBlockByResourceManager(blockDict['id'],
                                                blockPosSt,
                                                executor=self,
                                                reason=Reason.chunkRestore,
                                                chunk=self)
                if block % 100 == 0: await asyncio.sleep(0.1)
            
            
            
            self.log(logType.SUCCESS, "restoring data from save... DONE")
        except Exception as e:
            self.errorWithTraceback("error with restoring data from save", e)
                    
    
    def __init__(self, scene: 'Scene', chunkPos: int = 0, chunkData: Optional[dict] = None) -> None:
        # basics
        self.__scene = scene
        self.setLogParent(ParentForLogs(name=f"chunk_{chunkPos}", parent=self.getScene().getLogParent()))
        
        super().__init__()
        
        # logs
        self.log(logType.INIT, "The chunk is being intialized...")
        
        # basic informations
        self.__chunkPos = chunkPos
        self.__startPoint = Vector2(
            chunkPos * Chunk.SIZE.x * Block.SIZE.x,
            # chunkPos[1] * Chunk.SIZE.y * Block.SIZE.y
            0
        )
        
        self.__endPoint = self.__startPoint + Chunk.SIZE
        
  
        
        # self.__blocks: dict[tuple[int,int], Block] = {}
        
        
        # self.loadChunkFromCsv("test.csv")
        # self.generateChunk()
        
        # intialize blocks 
        self.__blocks: dict[tuple[int,int], Block] = {}
        
        if chunkData != None:
            self.log(logType.INIT, "restoring data from save...")
            asyncio.create_task(self.restoreChunkFromChunkData(chunkData),
                                name=f"chunk_restore_{self.__chunkPos}")
        else:
            # chunk generation
            self.log(logType.INIT, "starting world generation for a chunk...")
            asyncio.create_task(self.getScene().getWorldGenerator().generateChunk(
                chunkPos=self.__chunkPos,
                chunk=self,
                Scene=self.__scene
            ), name=f"world_generator{self.__chunkPos}"
            )
            # .add_done_callback(self.__checkForErrorsWorldGeneratorAsyncio)
            self.log(logType.SUCCESS, "starting world generation for a chunk... DONE")
            
        self.log(logType.SUCCESS, "The chunk is intialized!")


class Block(pygame.sprite.Sprite):
    '''just block :3'''
    
    # informations for every block
    SIZE = Vector2(32,32) # SIZE OF ALL BLOCKS
    
    # basic information about block (info that can be changed in every block)
    MAINTEXTURE: str | None = None  # texture that will be used
    MAINTEXTUREISTRANSPARENT: bool = False # if texture is transparent (that is only for pygame optimization)
    ID: str | None = None   # string ID (UNIQUE, MAIN ID)
    IDInt: int|None = None  # int ID (UNIQUE)
    
    # advanced information about block (info that can be changed in every block)
    listenToMe: bool = False # should game look out for this block to update it necessary (useful for crops or another things like that, that doesn't affect any updates that are caused by other blocks or entities. that's auto updates) {NOT IMPLEMENTED YET}
    listenPriority: int = 1 # priority of listening. The higher the better. {NOT IMPLEMENTED YET}
    
    
    # SCREENSIZE = (1280,720) # SIZE OF SCREEN (IDK IF THAT WAS USED ANYWHERE BUT ILL KEEP IT FOR SECURITY REASONS)
    
    # functions to changed in every block:
    
    def onGenerate(self, cordsRelative: Vector2, cordsAbsolute: Vector2, inChunkPosition: tuple[int,int], chunk: Chunk):
        '''Method executed when chunk is generated, can be changed in every block'''
        pass
    
    def onLoad(self, cordsRelative: Vector2, cordsAbsolute: Vector2, inChunkPosition: tuple[int,int], chunk: Chunk):  
        '''Method executed when chunk is loaded, can be changed in every block'''
        pass
    
    
    # getting neighbours
    
    def getBlockLeft(self, howManyToLeft: int = 1) -> 'Block | None':
        return self.getScene().getBlockByAbsPos((self.__absolutePos[0]-howManyToLeft,self.__absolutePos[1]))
    
    def getBlockRight(self, howManyToRight: int = 1) -> 'Block | None':
        return self.getScene().getBlockByAbsPos((self.__absolutePos[0]+howManyToRight,self.__absolutePos[1]))
 
    def getBlockUp(self, howManyToUp: int = 1) -> 'Block | None':
        return self.getScene().getBlockByAbsPos((self.__absolutePos[0],self.__absolutePos[1]-howManyToUp))
 
    def getBlockDown(self, howManyToUp: int = 1) -> 'Block | None':
        return self.getScene().getBlockByAbsPos((self.__absolutePos[0],self.__absolutePos[1]+howManyToUp))      
    
    def getBlockRelative(self, x: int = 0, y: int = 0) -> 'Block | None':
               return self.getScene().getBlockByAbsPos((self.__absolutePos[0]+x,self.__absolutePos[1]+y))   
            
    # changing block
    
    def changeBlockTo(self, block: 'Block | str | None', executor: Optional[Executor] = None, reason: Optional[Reason|str] = None) -> None:
        self.getChunk().setBlock(self.getBlockPos(), block, executor, reason)
    
    def setToAir(self, executor: Optional[Executor] = None, reason: Optional[Reason|str] = None) -> None:
        '''setting THIS block to air\n
            Args:\n
                * executor: Optional[Executor] -> autor of this action (instance)
                * reason: Optional[str] -> reason why block will be set
            Returns:\n
                None'''
        self.getChunk().setBlock(self.getBlockPos(), None, executor, reason)
         
    def removeBlock(self) -> None:
        '''same as self.setToAir() but doesn't have neither executor or reason and use removeBlock function instead of setBlock in the chunk'''
        self.getChunk().removeBlock(self.getCords())
        
    
    # getting something
    
    
    def getChunk(self) -> Chunk:
        return self.__chunk
    
    def getScene(self) -> 'Scene':
        return self.__chunk.getScene()
    
    def getGame(self) -> 'Game':
        return self.__chunk.getScene().getGame()
    
    def getMainCamera(self) -> 'camera':
        return self.__chunk.getScene().getGame().camera
    
    
    # def changeBlockTo(self, block: 'Block') -> None:
    #     chunk = self.getChunk()
    #     cords = self.getCords()
        
    #     chunk.removeBlock(cords)
    #     chunk.setBlock(cords, block)
        
    # def update(self, surface) -> None:
    #     camera = self.getMainCamera()  
    #     print('s')      
    #     if self.cords.x > camera.cords.x - self.SIZE.x and self.cords.x < camera.cameraEndPoint[0] + self.SIZE.x and self.cords.y + self.SIZE.y > camera.cords.y and self.cords.y < camera.cameraEndPoint[1] + self.SIZE.y:
    #         surface.blit(self.image,
    #                     self.cords - camera.cords)
            
         

        
    
    '''Returns cords relative to chunk starting Points'''
    def getCordsRelative(self) -> Vector2:
        '''gives you cords of left top corner of the block, but relative to chunk.'''   
        return self.__cords
    
    '''Returns cords'''
    def getCords(self) -> Vector2:
        '''gives you cords of left top corner of the block'''
        return self.cordsAbsolute
    
    def getBlockPos(self) -> tuple[int,int]:
        '''That's the same as self.getInChunkPosition()'''
        # return (int(self.__cords.x / Block.SIZE.x),
        #     int(self.__cords.y / Block.SIZE.y)) 
        return self.__inChunkPos      
    
    def getAbsolutePos(self) -> tuple[int,int]:
        return self.__absolutePos
    
    def getInChunkPosition(self) -> tuple[int,int]:
        '''gives you blockPos relative to chunk'''
        # return (int(self.__cords.x / Block.SIZE.x),
        #         int(self.__cords.y / Block.SIZE.y))
        return self.__inChunkPos
        
        
    # methods of creating blocks
        
    '''Create new block using resourceManager'''
    @staticmethod
    def newBlockByResourceManager(name: str, blockPos: tuple[int,int], executor: Optional[Executor] = None, reason: Optional[str] = None, addToEverything: bool = True, chunk: Optional[Chunk] = None) -> 'Block':
        if chunk == None and addToEverything:
            raise Exception("you must indicate specified chunk if you want to add this to scene. If you don't want to do that set addToEverything to false")
        
        rm = chunk.getScene().getGame().getResourceManager()
        
        # if cordsRelative == None:
        #     cords = Vector2(0,0)
            
        blockInfo = rm.getBlockInformation(name)


        _b = blockInfo['class'](
            image=rm.getTexture(blockInfo['class'].MAINTEXTURE),
            blockPos=blockPos,
            chunk=chunk,
            executor = executor,
            reason=reason,
            addToEverything=addToEverything
        )
        
        chunk.setBlock(blockPos, _b)
        
        # if addToEverything:
        #     _b = blockInfo['class'](
        #         image=rm.getTexture(blockInfo['class'].MAINTEXTURE),
        #         blockPos=blockPos,
        #         chunk=chunk,
        #         executor = executor,
        #         reason=reason,
                
        #     )
        #     # print(_b)
        #     chunk.setBlock(blockPos, _b)
        #     # print(chunk.getBlockByTuple(blockPos))
        # else:
        #     _b = blockInfo['class'](
        #         image=rm.getTexture(blockInfo['class'].MAINTEXTURE),
        #         blockPos=blockPos,
        #         chunk=chunk,
        #         executor = executor,
        #         reason=reason
        #     )
        #     chunk.setBlock(blockPos, _b)
        
        return _b
        
    
    
    def __init__(self, image:pygame.surface.Surface, blockPos: tuple[int,int], chunk: Chunk, executor: Optional[Executor] = None, reason: Optional[str] = None, addToEverything: bool = True) -> None:
        '''creating block (TRY TO NOT USE IT!, USE another methods like Block.newBlockByResourceManager() or chunk.setBlock() or scene.setBlock(), using this method is very risky! using this will cause a lot of problems, especially because you have to use relative position! there's no guarantee that everything will work just fine!)\n
            Args:\n
                * image: pygame.surface.Surface -> image
                * blockPos: tuple[int,int] -> position of this block relative to chunk
                * chunk: Chunk -> chunk where this block is located
                * executor: Optional[Executor] -> autor of this action (instance)
                * reason: Optional[str] -> reason why block will be set
            Returns:\n
                None'''
        # just super()
        if addToEverything:
            super().__init__(chunk,chunk.getScene())
        else:
            super().__init__()
            
        # basics
        self.__chunk = chunk
        self.__inChunkPos = blockPos
        self.__absolutePos = (blockPos[0]+chunk.getChunkPos()*Chunk.SIZE.x, blockPos[1])
        self.image = image
        self.__cords: Vector2 = Vector2(blockPos[0] * Block.SIZE.x, blockPos[1] * Block.SIZE.y)
        # print(self.__cords)
        self.cordsAbsolute: Vector2 = Vector2(self.__cords.x + self.__chunk.getStartingPoint().x,
                                        self.__cords.y + self.__chunk.getStartingPoint().y)
        
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.topleft = self.cordsAbsolute
        
        self.doRender = True
        
        # reason handling
        match reason:
            case "world_generator":
                self.onGenerate(cordsAbsolute=self.cordsAbsolute,cordsRelative=self.__cords, inChunkPosition=blockPos, chunk=chunk)
            case"chunk_load":
                self.onLoad(cordsAbsolute=self.cordsAbsolute,cordsRelative=self.__cords, inChunkPosition=blockPos, chunk=chunk)
        
        # ???? co skąd to coś tu jest
        # del chunk_position

# class dupa(): pass
class Scene(pygame.sprite.Group, Executor, Loggable):   
    '''just scene''' 
    RENDERDISTANCE = 3 # SIMULATION DISTANCE
    
    # getting
    def getGame(self) -> 'Game':
        return self.__game
    
    def getName(self, forceGettingFromEngine: bool = False) -> str | None:
        if self.__name is not None and not forceGettingFromEngine:
            return self.__name
        else:
            if not self.__game.isSceneAdded(Scene):
                return None
            
            return self.__game.findNameOfScene(self)
        
            
    def getSeed(self) -> str:
        return self.__seed
    
    def getSeedInt(self) -> int:
        return self.__seedInt
    
    def getWorldGenerator(self) -> WorldGenerator:
        return self.__worldGenerator
    
    
    
    
    async def tick(self) -> None:
        '''thing that happens every tick'''
        # aha = dupa()
        # aha.rect = pygame.rect.Rect(pygame.mouse.get_pos()[0]-self.getGame().camera.cords.x,pygame.mouse.get_pos()[1]-self.getGame().camera.cords.y,1,1)
        # print(pygame.sprite.spritecollide(aha, self.sprites(), False))
        
        
        surfSize = pygame.display.get_surface().get_size()
        centerChunkPos: int = (self.getGame().camera.cords.x + surfSize[0]) // Block.SIZE.x // Chunk.SIZE.x
        
        
        ChunksToBeLoaded: list[Chunk] = []
        
        ChunksToBeLoaded.extend([int(x+centerChunkPos) for x in range(-self.RENDERDISTANCE, self.RENDERDISTANCE+1)])
        
       
        
        chunk: Chunk = None
        
        # unload chunks
        for chunkPos, chunk in self.__activeChunks.copy().items():
            if chunkPos not in ChunksToBeLoaded:
                self.unloadChunk(chunk)
        
        # load chunks
        # for newChunk in [chunk for chunk in ChunksToBeLoaded if chunk not in self.__activeChunks]: 
        for newChunkPos in [chunkPos for chunkPos in ChunksToBeLoaded if not self.isChunkActive(chunkPos)]:
            self.loadChunk(newChunkPos)
        
        
        # checking for chunks that should be loaded/unloaded
        # surfSize = pygame.display.get_surface().get_size()
        # centerChunkPos = ((self.getGame().camera.cords.x + surfSize[0]) // Block.SIZE.x // Chunk.SIZE.x,
        #              (self.getGame().camera.cords.y + surfSize[1]) // Block.SIZE.y // Chunk.SIZE.y)
        
        
        # ChunksToBeLoaded: list[Chunk] = []
        
        # ChunksToBeLoaded.extend([(x+centerChunkPos,0) for x in range(-self.RENDERDISTANCE, self.RENDERDISTANCE+1)])
        
       
        
        # chunk: Chunk = None
        
        # # unload chunks
        # for chunkPos, chunk in self.__activeChunks.copy().items():
        #     if chunkPos not in ChunksToBeLoaded:
        #         self.unloadChunk(chunk)
        
        # # load chunks
        # # for newChunk in [chunk for chunk in ChunksToBeLoaded if chunk not in self.__activeChunks]: 
        # for newChunkPos in [chunkPos for chunkPos in ChunksToBeLoaded if not self.isChunkActive(chunkPos)]:
        #     self.loadChunk(newChunkPos)
            
        # print(self.getGame().clock.get_fps(),len(self.__activeChunks), centerChunkPos, ChunksToBeLoaded)
        # pygame.time.Clock.ge
            
    def loadChunk(self, chunkPos: int):
        '''just loading chunk by chunkPos. Requires chunkPos of type int'''
        if str(chunkPos) in self.__forSaving['chunkData']:
            self.__activeChunks[chunkPos] = Chunk(scene=self, chunkPos=chunkPos, chunkData = self.__forSaving['chunkData'][str(chunkPos)]) 
            return
        
        self.__activeChunks[chunkPos] = Chunk(scene=self, chunkPos=chunkPos) 
    
    def isChunkActive(self, chunkPos: int) -> bool:
        '''check if chunk is active. Requires chunkPos of type int and returns bool'''
        return chunkPos in self.__activeChunks.keys()

        
    def getActiveChunks(self) -> dict[int, Chunk]:
        return self.__activeChunks
    
    def getChunk(self, chunkPos: int) -> Chunk:
        if chunkPos not in self.__activeChunks:
            raise chunkNotLoaded(f"Chunk of cords ${chunkPos} is not loaded, can't access that chunk")
        return self.__activeChunks[chunkPos]
        
    def unloadChunk(self, chunk: Chunk) -> None:
        chunkPos = str(chunk.getChunkPos())
        
        if chunkPos in self.__forSaving['chunkData']:
            data = chunk.unload(previousData=self.__forSaving['chunkData'][chunkPos])
            self.__forSaving['chunkData'][chunkPos].update(data)
            del self.__activeChunks[chunk.getChunkPos()]
            return

        data = chunk.unload()
        self.__forSaving['chunkData'][chunkPos] = data
        # self.__forSaving['chunkData'][str(chunk.getChunkPos())].update(
        #     chunk.unload(previousData=self.__forSaving['chunkData'][str(chunk.getChunkPos())])
        #     )

        del self.__activeChunks[chunk.getChunkPos()]
        
    # def draw(self):
    #     surf = self.__game.getDisplayOrginal()
    #     # for chunk in self.__activeChunks.values():
    #     #     chunk.draw(surf)
    #     self.camera.draw(self.get)
    
    # blocks handling
            
    def setBlockByAbsolutePos(self, pos: tuple[int,int], block: None|Block|str, dontRaiseErrors: bool = False) -> None:
        # if isinstance(pos, Vector2):
        #     pos = tuple(pos)
        
        # chunkPos = (pos[0] // Chunk.SIZE.x, pos[1] // Chunk.SIZE.y)
        chunkPos = pos[0] // Chunk.SIZE.x
        
        if chunkPos not in self.__activeChunks:
            self.log(logType.ERROR, f"Trying to access block of position ${pos} which should be located in chunk ${chunkPos}, but that chunk is not loaded!")
            if dontRaiseErrors: return
            raise chunkNotLoaded(f"Trying to access block of position ${pos} which should be located in chunk ${chunkPos}, but that chunk is not loaded!")
        
        # previousAmountOfBlocks = ((chunkPos-1) * Chunk.SIZE.x, (chunkPos-1) * Chunk.SIZE.y)
        # blockPos = (cords[0] // Chunk.SIZE.x, cords[1] // Chunk.SIZE.y)
        
        BlockPos = (int(pos[0] % Chunk.SIZE.x), int(pos[1] % Chunk.SIZE.y))
        
        self.getChunk(chunkPos).setBlock(BlockPos, block)
        
    def getBlockByAbsPos(self, absolutePos: tuple[int,int]) -> Block | None:
        '''Get block by absolute blockPos'''
        chunkCords = absolutePos[0] // Chunk.SIZE.x
        # chunkStartPoint = (Chunk.SIZE.x * chunkCords, 0) 
        RelativeBlockPos = (absolutePos[0]  // Block.SIZE.x % Chunk.SIZE.x, 
                            absolutePos[1] // Block.SIZE.y)
        
        
        if chunkCords not in self.__activeChunks:
            raise chunkNotLoaded(f"Trying to access block of cords ${absolutePos} which should be located in chunk ${chunkCords}, but that chunk is not loaded!")
        
        
        return self.__activeChunks[chunkCords].getBlockByTuple(RelativeBlockPos)       
        
    def getBlock(self, cords: Vector2) -> Block | None:
        '''Get block by absolute cords'''
        # for some reason in the first line diving by block SIZE is unnecessary (even tho it should be), but that is blocking readability...
        # chunkCords = (cords.x // Block.SIZE.x // Chunk.SIZE.x, cords.y // Block.SIZE.y // Chunk.SIZE.y)
        # print(self.getChunkPosFromCords(cords))
        chunkCords = cords.x // Block.SIZE.x // Chunk.SIZE.x
        # print(chunkCords)
        # chunkStartPoint = (Chunk.SIZE.x * chunkCords, 0) 
        RelativeBlockPos = (cords.x // Block.SIZE.x % Chunk.SIZE.x, 
                            cords.y // Block.SIZE.x)
        
        if RelativeBlockPos[0] < 0: RelativeBlockPos[0] += Chunk.SIZE.x
        
        if chunkCords not in self.__activeChunks:
            raise chunkNotLoaded(f"Trying to access block of cords ${cords} which should be located in chunk ${chunkCords}, but that chunk is not loaded!")
        
        
        return self.__activeChunks[chunkCords].getBlockByTuple(RelativeBlockPos)
             
    
    @staticmethod
    def getChunkPosFromCords(cords: Vector2) -> int:
        return cords.x // Block.SIZE.x // Chunk.SIZE.x
        
    @staticmethod
    def getChunkPosFromAbsPos(cords: tuple[int,int]) -> int:
        return cords[0] // Chunk.SIZE.x
    
    # save managing
    @staticmethod
    def restoreMapFromSave(self, game: 'Game', saveData: dict) -> 'Scene':
        return Scene(game=game,
                name=saveData['worldName'],
                seed=saveData['worldSeed'],
                saveData=saveData)
        
        
    def saveWorld(self) -> None:
        '''allows you to save the world'''
        # ensuring that every chunk is in current state
        for chunkPos, chunk in self.__activeChunks.items():
            if str(chunkPos) in self.__forSaving['chunkData']:
                self.__forSaving['chunkData'][str(chunkPos)] = chunk.save(previousData=self.__forSaving['chunkData'][str(chunkPos)])
            else:
                self.__forSaving['chunkData'][str(chunkPos)] = chunk.save()
        
        # final saving
        with open('data/saves/map.json', "w") as file:
            file.write(json.dumps(self.__forSaving, indent=4))
    
 
    def __init__(self, game: 'Game', name: str, worldGenerator: WorldGenerator, autoAdd: bool = True, inIdle: bool = False, seed: str = "uwusa", saveData: Optional[dict] = None) -> None:
        # basics (required to even basic logging :<)
        self.__game: 'Game' = game
        super().__init__()
        self.setLogParent(ParentForLogs(name=f"scene_{name}", parent=self.getGame().getLogParent()))
        self.log(logType.INIT, "The scene is being intialized...")
        
        
        # save loading
        if saveData == None:
            try:
                with open("bin/json/saveStartData.json") as f:
                    self.__forSaving = json.load(f)
                    self.info("scene will be run on a new save!")
            except Exception as e:
                self.errorWithTraceback("couldn't open json file with save starting point!",e)
        else: 
            self.info("scene will be run on an existing save!")
            self.__forSaving = saveData
        

        

        self.heightCache = {
            "grass_height": {},
            "dirt_height": {},
            "bedrock_height": {}
        }
        
        self.blockToNextCache = {
            
        }
        
        # info
        self.__autoAdd: bool = autoAdd
        self.__name: str = name
        self.idle: bool = inIdle
        self.__seed, self.__seedInt = seed, int("".join([str(ord(char)) for char in seed]))
        self.__worldGenerator = worldGenerator(self)
       
        
        self.__activeChunks: dict[int, Chunk] = {}
        
        # generating basic chunks
        

        # self.__activeChunks[0] = Chunk(scene=self, chunkPos=0)
                 
        if autoAdd:
            self.__game.addScene(scene=self, name=self.__name)
            
        self.log(logType.SUCCESS, "The scene is intialized!")
            
        
            
        
# aliases, should be use only for types  
currentScene: TypeAlias = Scene
activeScene: TypeAlias = Scene

