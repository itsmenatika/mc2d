import pygame
from pygame.math import Vector2
import random

from bin.map import Chunk, Scene, Block
from bin.abstractClasses import WorldGenerator, Executor, Reason

from typing import Optional


class worldGeneratorNormal(WorldGenerator):
    def generateHeight(self, x, chunkPos: list[int,int], seedInt: int,  cache: dict, fromLeft: bool = False, startPoint: int = 10,
                       max: Optional[int] = None, min: Optional[int] = None, probability: int = 60, seedName: str = "global") -> int:  
        _s = seedInt % 10
        _xAbsolute = x + chunkPos[0] * Chunk.SIZE.x
        
        if _xAbsolute in cache: return cache[_xAbsolute]
        if _xAbsolute == 0: return startPoint
        
        if x + (chunkPos[0] + 1) * Chunk.SIZE.x not in cache and not fromLeft:
            return self.generateHeight(x, chunkPos, seedInt, cache, True, startPoint=startPoint, max=max, min=min, probability=probability, seedName=seedName)
        
        
        random.seed(f"${self.getScene().getSeed()}_CHUNK_{chunkPos}_h{seedName}_${x}")
        
        wannabe = random.randint(0,100)
        howmuch = random.randint(-1,1)
        
        random.seed(f"${self.getScene().getSeed()}_CHUNK_{chunkPos}")
        
        if fromLeft:
            if x < 0:
                chunkPos[0] += 1
                return self.generateHeight(x, chunkPos, seedInt, cache, True, startPoint=startPoint, max=max, min=min, probability=probability, seedName=seedName)
            
            _n = self.generateHeight(x - 1, chunkPos, seedInt, cache, True, startPoint=startPoint, max=max, min=min, probability=probability, seedName=seedName)
            if(wannabe > probability):
                _n += howmuch      
            
            
            if min is not None and _n < min:
                _n = min
            elif max is not None and _n > max:
                _n = max
                
            cache[_xAbsolute] = _n
            return _n
            
            
            
        
        while x > Chunk.SIZE.x:
            x -= Chunk.SIZE.x
            chunkPos[0] += 1
        
        _n = self.generateHeight(x + 1, chunkPos, seedInt, cache, False,  startPoint=startPoint, max=max, min=min, probability=probability, seedName=seedName)
        if(wannabe > probability):
            _n += howmuch
            
        if min is not None and _n < min:
            _n = min
        elif max is not None and _n > max:
            _n = max
            
        cache[_xAbsolute] = _n
        
        return _n
    
    def generateVeins(self, chunkPos: tuple[int,int], chunk: Optional[Chunk], blockName: str, howMuchVeinsMin: int, howMuchVeinsMax: int, minInVein: int, maxInVein: int, recursive: bool = True, fromWhatSide: None|str = None, blocks: dict[tuple[int, int], Block] = {}, minY: int=0, maxY: int = Chunk.SIZE.y) -> dict[tuple[int, int], Block]: 
        # return {}
        random.seed(f"${self.getScene().getSeed()}_CHUNK_{chunkPos}_VEINS_{blockName}")
        
        
        if recursive:
            fromLeft = self.generateVeins(chunkPos=(chunkPos[0]+1, chunkPos[1]), chunk=chunk, blockName=blockName, howMuchVeinsMin=howMuchVeinsMin, howMuchVeinsMax=howMuchVeinsMax, minInVein=minInVein, maxInVein=maxInVein, recursive=False, fromWhatSide='left', blocks=blocks, minY=minY,maxY=maxY)
            fromRight = self.generateVeins(chunkPos=(chunkPos[0]+1, chunkPos[1]), chunk=chunk, blockName=blockName, howMuchVeinsMin=howMuchVeinsMin, howMuchVeinsMax=howMuchVeinsMax, minInVein=minInVein, maxInVein=maxInVein, recursive=False, fromWhatSide='right', blocks=blocks, minY=minY,maxY=maxY)
            
        
        howmuchveins: int = random.randint(howMuchVeinsMin, howMuchVeinsMax)
        howmuchInVein: int = random.randint(minInVein, maxInVein)
        
        rightBlocks: dict[tuple[int, int], Block] = {}
        leftBlocks: dict[tuple[int, int], Block] = {}
        
        veins = 0
        while veins < howmuchveins:
            x = random.randint(0, Chunk.SIZE.x-1)
            y = random.randint(minY, maxY)
            

            if fromWhatSide == None:
                # print(blocks[(x,y)], veins, not((x,y) in blocks and blocks[(x,y)] == "stone"))
                if not((x,y) in blocks and blocks[(x,y)].ID == "stone"): continue
                
                blocks[(x,y)].kill()
                blocks[(x,y)] = Block.newBlockByResourceManager(
                chunk=chunk,
                name="coal_ore",
                cordsRelative=Vector2(x * Block.SIZE.x, y * Block.SIZE.y),
                executor=self,
                reason=Reason.WorldGenerator
                )
                
                
            veins += 1
            
            howManyHasGenerated: int = 1
            choices = [[1, 0], [-1, 0], [0, 1], [0, -1]] 
            while howManyHasGenerated < howmuchInVein:
                if len(choices) <= 0: break
                addx, addy = random.choice(choices)
                choices.remove([addx,addy])
                
                if fromWhatSide == None:
                    if not((x+addx,y+addy) in blocks and blocks[(x+addx,y+addy)].ID == "stone"): continue
                    if not(x+addx > Chunk.SIZE.x - 1 or x+addx < 0 or y+addy < 0 or y+addy > Chunk.SIZE.y-1):
                        blocks[(x+addx,y+addy)].kill()
                        # print('s',blocks[(x+addx,y+addy)])
                        blocks[(x+addx,y+addy)] = Block.newBlockByResourceManager(
                            chunk=chunk,
                            name="coal_ore",
                            cordsRelative=Vector2((x+addx)* Block.SIZE.x, (y+addy) * Block.SIZE.y),
                            executor=self,
                            reason=Reason.WorldGenerator
                            )
                    choices = [[1, 0], [-1, 0], [0, 1], [0, -1]] 
                        
                if x+addx > Chunk.SIZE.x-1 and fromWhatSide=="right":
                    print((x,y))
                    print(x+addx)
                    rightBlocks[(x+addx - (Chunk.SIZE.x-1), y)] = Block.newBlockByResourceManager(
                    chunk=chunk,
                    name="coal_ore",
                    cordsRelative=Vector2((x+addx - (Chunk.SIZE.x-1))* Block.SIZE.x, y * Block.SIZE.y),
                    executor=self,
                    reason=Reason.WorldGenerator
                    )

                elif x+addx < 0 and fromWhatSide=="left":
                    leftBlocks[abs(x+addx), y] = Block.newBlockByResourceManager(
                    chunk=chunk,
                    name="coal_ore",
                    cordsRelative=Vector2(abs(x+addx)* Block.SIZE.x, y * Block.SIZE.y),
                    executor=self,
                    reason=Reason.WorldGenerator
                    )
                    
                
                x += addx
                y += addy
                howManyHasGenerated += 1
                
        if fromWhatSide == "right": return rightBlocks
        elif fromWhatSide == "left": return leftBlocks
                
        for cords, block in fromLeft.items():
            print(cords in blocks and blocks[cords].ID == "stone")
            if cords in blocks and blocks[cords].ID == "stone":
                blocks[cords].kill
                del blocks[cords]
                
                # blocks[cords] = block
                # print('s', chunkPos, fromLeft, fromRight, cords)
                self.getScene().getGame().camera.cords = Vector2(cords[0] * Block.SIZE.x,
                                                                    cords[1] * Block.SIZE.y)
                # print(blocks)  
                # print("\n\n\n") 
                    
        for cords, block in fromRight.items():
            print(cords in blocks and blocks[cords].ID == "stone")
            if cords in blocks and blocks[cords].ID == "stone":
                self.getScene().remove(blocks[cords])
                blocks[cords].kill()
                del blocks[cords]
                # print(blocks[cords])
                # blocks[cords] = block
                # print('s', chunkPos, fromLeft, fromRight, cords)
                self.getScene().getGame().camera.cords = Vector2(cords[0] * Block.SIZE.x,
                                                                 cords[1] * Block.SIZE.y)
                # print(blocks)   
                # print("\n\n\n")
                
        return {}
        
            
        
        
        

    def generateChunk(self, chunkPos: tuple[int, int], chunk: 'Chunk', Scene: 'Scene') -> dict[tuple[int, int], Block]:
        blocks: dict[tuple[int,int], Block] = {}
        
        
        random.seed(f"${self.getScene().getSeed()}_CHUNK_{chunkPos}")
        
        for x in range(0,int(Chunk.SIZE.x)):
            height = self.generateHeight(x, list(chunkPos), self.getScene().getSeedInt(), self.__cache['grass_height'], False, min=6, max=16, seedName="height")
            blocks[(x,height)] = Block.newBlockByResourceManager(
                chunk=chunk,
                name="grass_block",
                cordsRelative=Vector2(x * Block.SIZE.x,height * Block.SIZE.y),
                executor=self,
                reason=Reason.WorldGenerator
            )
            
            dirtheight = self.generateHeight(x, list(chunkPos), self.getScene().getSeedInt(), self.__cache['dirt_height'], False, startPoint=4, max=5, min=3, seedName="dirtheight")
            

            
            for y in range(0,dirtheight):
                blocks[(x,height+y+1)] = Block.newBlockByResourceManager(
                    chunk=chunk,
                    name="dirt",
                    cordsRelative=Vector2(x * Block.SIZE.x,(height + 1 + y) * Block.SIZE.y),
                    executor=self,
                    reason=Reason.WorldGenerator
                )
                
            currentHeight = height + dirtheight + 1
            for y in range(0,30):
                blocks[(x,y+currentHeight)] = Block.newBlockByResourceManager(
                    chunk=chunk,
                    name="stone",
                    cordsRelative=Vector2(x * Block.SIZE.x,(y + currentHeight) * Block.SIZE.y),
                    executor=self,
                    reason=Reason.WorldGenerator
                ) 
                if y + currentHeight >= 32:   
                    bedrockHeight = self.generateHeight(x, list(chunkPos), self.getScene().getSeedInt(), self.getScene().heightCache['bedrock_height'], False, startPoint=2, max=2, min=1, probability=20)
                    
                    if bedrockHeight == 1:
                        blocks[(x,y+currentHeight + 1)] = Block.newBlockByResourceManager(
                            chunk=chunk,
                            name="stone",
                            cordsRelative=Vector2(x * Block.SIZE.x,(y + currentHeight + 1) * Block.SIZE.y),
                            executor=self,
                            reason=Reason.WorldGenerator
                        )
                        blocks[(x,y+currentHeight + 2)] = Block.newBlockByResourceManager(
                            chunk=chunk,
                            name="bedrock",
                            cordsRelative=Vector2(x * Block.SIZE.x,(y + currentHeight + 2) * Block.SIZE.y),
                            executor=self,
                            reason=Reason.WorldGenerator
                        ) 
                    else:
                        blocks[(x,y+currentHeight + 1)] = Block.newBlockByResourceManager(
                            chunk=chunk,
                            name="bedrock",
                            cordsRelative=Vector2(x * Block.SIZE.x,(y + currentHeight + 1) * Block.SIZE.y),
                            executor=self,
                            reason=Reason.WorldGenerator
                        )
                        blocks[(x,y+currentHeight + 2)] = Block.newBlockByResourceManager(
                            chunk=chunk,
                            name="bedrock",
                            cordsRelative=Vector2(x * Block.SIZE.x,(y + currentHeight + 2) * Block.SIZE.y),
                            executor=self,
                            reason=Reason.WorldGenerator
                        ) 
                    break
                
        blocks = self.generateVeins(chunkPos, chunk, "coal_ore", 2, 5, 2, 5, True, None, blocks, currentHeight+1, 32)
        
        return blocks
        
        # veins = 5
        # while veins > 0:
        #     veins -= 1
        #     x = random.randint(0,Chunk.SIZE.x)
        #     y = random.randint(currentHeight+3, 32)
            
        #     self.__blocks[(x,y)] = Block.newBlockByResourceManager(
        #         chunk=self,
        #         name="coal_ore",
        #         cordsRelative=Vector2(x * Block.SIZE.x,y * Block.SIZE.y),
        #         executor=self,
        #         reason="world_generator"
        #     ) 
            
        #     howmuch = random.randint(0,3)
            
        #     choices = [[1,0], [-1,0], [0,1], [0,-1]]
        #     while howmuch > 0:
        #         if len(choices) == 0: break
                
        #         addx, addy = random.choice(choices)
        #         choices.remove([addx,addy])
        #         if x+addx > 16:
        #             self.getScene().blockToNextCache((self.getChunkPos()[0]+1, self.getChunkPos()[1]))
        #             howmuch -= 1
        #             continue
        #         elif x+addx < 0:
        #             self.getScene().blockToNextCache((self.getChunkPos()[0]-1, self.getChunkPos()[1]))
        #             howmuch -= 1
        #             continue
                
        #         if (x+addx, y+addy) in self.__blocks:
        #             if self.__blocks[(x+addx, y+addy)].ID != "stone": continue
                    
        #             self.__blocks[(x+addx,y+addy)] = Block.newBlockByResourceManager(
        #                 chunk=self,
        #                 name="coal_ore",
        #                 cordsRelative=Vector2(x * Block.SIZE.x,y * Block.SIZE.y),
        #                 executor=self,
        #                 reason="world_generator"
        #             ) 
                    
        #             x += addx
        #             y += addy
                    
        #             howmuch -= 1
        
       
            
                
    def __init__(self, scene: 'Scene') -> None:
        super().__init__(scene)
        
        self.__cache = {
            "grass_height": {},
            "dirt_height": {},
            "bedrock_height": {}
        }
        