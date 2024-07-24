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
                    if block != None:
                        block.lightValue = currentLight
                        currentLight = max(currentLight-4, 0)
                   
                   
        for chunk in chunks.values():
            for y in range(0, int(chunk.SIZE.y)):
                for x in range(0, int(chunk.SIZE.x)):
                    block = chunk.getBlockByTuple((x,y))
                    if block != None:
                        up = block.getBlockUp()
                        if up == None: up = 0
                        else: up = up.lightValue
                        
                        down = block.getBlockDown()
                        if down == None: down = 0
                        else: down = down.lightValue
                        
                        right = block.getBlockRight() 
                        if right == None: right = 0
                        else: right = right.lightValue
                        
                        left = block.getBlockLeft() 
                        if left == None: left = 0    
                        else: left = left.lightValue               
                        
                        block.lightValue = max(
                        up, down, right-2, left-2, 2
                        )-2
                        
                        block.recompileLight()
        
    
    def __init__(self, scene: 'Scene') -> None:
        self.__scene = scene
        super().__init__(logParent=ParentForLogs("lightingSystem", parent=self.__scene.getLogParent()))
    