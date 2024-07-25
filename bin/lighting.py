# external imports
import pygame
import asyncio
from pygame.math import Vector2


# internal imports
from bin.logger import logType, Loggable, ParentForLogs
# from bin.map import Chunk, Block, Scene
from bin.abstractClasses import Executor

class lightingManager(Loggable, Executor):
    def getGame(self) -> 'game':
        return self.__scene.getGame()
    
    def getScene(self) -> 'Scene':
        return self.__scene
    
    def recompileBlocks(self):
        '''recompiles lighting for the blocks'''
        
        skyLight: int = 15
        
        chunks: dict[int, 'Chunk'] = self.__scene.getActiveChunks()
        # chunkSize: Vector2 = chunks.values()[chunks.keys()[0]].ChunkSize
        
        # chunk: Chunk
        # block: Block
        
        # basic values
        for chunk in chunks.values():
            for x in range(0, int(chunk.SIZE.x)):
                currentLight = skyLight
                
                for y in range(0, int(chunk.SIZE.y)):
                    block = chunk.getBlockByTuple((x,y))
                    
                    if block == None:
                        continue
                        # if currentLight == 15: print('s')
                        
                    currentLight = max(block.lightValue - block.lightingAbsorption, 0)  
                          
        # check for neighbouring blocks
        chunkInCorrectOrder = dict(sorted(chunks.items(), key=lambda item: item[0]))
        # print(chunkInCorrectOrder)
        for chunk in chunkInCorrectOrder.values():
            for y in range(0, int(chunk.SIZE.y)):
                for x in range(0, int(chunk.SIZE.x)):
                    
                    block = chunk.getBlockByTuple((x,y))
                    
                    if block == None:
                        continue
                        
                    up = block.getBlockUp()
                    up = 0 if up == None else up.lightValue
 
                    down = block.getBlockDown()
                    down = 0 if down == None else down.lightValue
                        
                    right = block.getBlockRight()
                    right = 0 if right == None else right.lightValue
                        
                    left = block.getBlockLeft()
                    left = 0 if left == None else left.lightValue           
                        
                    block.lightValue = max(
                        up-2, down-2, right-1, left-1, 2, block.lightValue
                    ) - 2
                        
                    block.recompileLight()
                        
        
    
    def __init__(self, scene: 'Scene') -> None:
        self.__scene = scene
        super().__init__(logParent=ParentForLogs("lightingSystem", parent=self.__scene.getLogParent()))
    