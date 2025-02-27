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
        
        # basic values (light from the sky) (1st iteration of light engine)
        for chunk in chunks.values():
            for x in range(0, int(chunk.SIZE.x)):
                # set current light to sky light
                currentLight = skyLight
                
                for y in range(0, int(chunk.SIZE.y)):
                    block = chunk.getBlockByTuple((x,y))
                    # if no block, try getting block from the background
                    if block == None:
                        block = chunk.getBlockByTuple((x,y), background=True)
                    
                    # if theres still no block, continue
                    if block == None: continue
                        # if currentLight == 15: print('s')
                        
                    # calculate strength of current light beam
                    # if block.isInBackground():
                    block.lightValue = currentLight
                    
                    blockOp = block.getOppositeLayer()
                    if blockOp != None:
                        blockOp.lightValue = currentLight
                        # print(currentLight, blockOp, block)  
                        # blockOp.recompileLight()
                    
                    currentLight = max(currentLight - block.lightingAbsorption, 0)
                    # if currentLight > 15: print(currentLight, block)  
                    # block.recompileLight()
                    
        # add additional light sources like torches of lava (2nd iteration of light engine) (not done yet)
                          
        # check for neighbouring blocks add mix them together (3nd iteration of light engine) (this need some reworking (im considering creating additional table, not important that much, because that are only small bugs)
        # return
        # sort blocks
        chunkInCorrectOrder = dict(sorted(chunks.items(), key=lambda item: item[0]))
        
        lightTable = []
        
        # print(chunkInCorrectOrder)
        for chunk in chunkInCorrectOrder.values():
            for y in range(0, int(chunk.SIZE.y)):
                for x in range(0, int(chunk.SIZE.x)):
                    
                    # get block
                    block = chunk.getBlockByTuple((x,y))
                    background: bool = False
                    
                    # if no block get block from the background
                    if block == None: 
                        block = chunk.getBlockByTuple((x,y), background=True)
                        background = True
                    # is still None, then you should continue
                    if block == None: continue
                        
                    # get block neighbours (if no neighbours then set 0, in the future it should get backgroundForced tile instead)
                    up = block.getBlockUp()
                    if up == None: 
                        up = block.getBlockUp(backgroundForced=not background)

                    up = 0 if up == None else up.lightValue
 

                    down = block.getBlockDown()
                    
                    if down == None: 
                        down = block.getBlockDown(backgroundForced=not background)

                    down = 0 if down == None else down.lightValue
                        

                    right = block.getBlockRight()

                    if right == None: 
                        right = block.getBlockRight(backgroundForced=not background)

                    right = 0 if right == None else right.lightValue
                        

                    left = block.getBlockLeft()

                    if left == None: 
                        left = block.getBlockLeft(backgroundForced=not background)

                    left = 0 if left == None else left.lightValue           
                        
                        
                    lightTable.append(data := (block.isInBackground(), block, max(
                        up-2, down-2, right-1, left-1, 2, block.lightValue
                    ) - 2))
                    
                    block.lightValue = data[2]
                    block.recompileLight()

        # # print(lightTable)
        # # final compile (4th iteration)
        # for data in lightTable:
        #     # x, y = cord
        #     # if data[0]: block = chunk.getBlockByTuple(cord, background=True)
        #     # else: block = chunk.getBlockByTuple(cord)
            
        #     # print(block)

        #     block = data[1]
            
        #     # if data[1]:
        #     #     block.lightValue = max(data[2] -1, 0)
        #     # else:
        #     #     block.lightValue = data[2]
            
        #     block.lightValue = data[2]
            
        #     # print(block.lightValue)
        #     # print(block.lightValue)
        #     block.recompileLight()
            
            # blockOp = block.getOppositeLayer()
            # if blockOp != None:
            #     if not data[1]: data[2] -= 1
            #     blockOp.lightValue = max(data[2],0)
            #     blockOp.recompileLight()
                        
                    # calculate max of this values -2
                    # block.lightValue = max(
                    #     up-2, down-2, right-1, left-1, 2, block.lightValue
                    # ) - 2
                       
                    # blockOp = block.getOppositeLayer()
                    # if blockOp != None:
                    #     blockOp.lightValue = block.lightValue
                    #     blockOp.recompileLight()
                    #     # print(blockOp.lightValue)
                       
                    # # tell block to recompile its image to fix the new assigned light value 
                    # block.recompileLight()
                        
        
    
    def __init__(self, scene: 'Scene') -> None:
        self.__scene = scene
        super().__init__(logParent=ParentForLogs("lightingSystem", parent=self.__scene.getLogParent()))
    