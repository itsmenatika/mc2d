import pygame
from pygame.math import Vector2
import random
import asyncio

from bin.map import Chunk, Scene, Block
from bin.abstractClasses import WorldGenerator, Executor, Reason

from typing import Optional


stats = []

class worldGeneratorNormal(WorldGenerator):
    def generateTress(self, chunkPos: list[int,int], chunk: Chunk, blocks: dict[tuple[int, int], Block], howMuchMin: int, howMuchMax: int, get: Optional[str] = None) -> dict[tuple[int, int], Block]:
        if get is None:
            fromLeft = self.generateTress((chunkPos[0]-1,chunkPos[1]), chunk, blocks, 1, 2, get="left")
            fromRight = self.generateTress((chunkPos[0]+1,chunkPos[1]), chunk, blocks, 1, 2, get="right")
        random.seed(f"${self.getScene().getSeed()}_CHUNK_{chunkPos[0]}_trees")
        
        howMuchTrees: int = random.randint(howMuchMin, howMuchMax)
        
        _taken = []
        _recent = random.randint(0, Chunk.SIZE.x-1)
        _taken.extend([_recent, _recent+1, _recent+2, _recent-1, _recent-2])
        treesPos = [_recent]
        for _ in range(howMuchTrees):
            _recent = _recent + random.randint(3,4) * random.choice([-1,1])
            print(_taken, _recent, chunkPos)
            if len(set(_taken).intersection([_recent, _recent-1, _recent+1])) != 0: continue
            treesPos.append(_recent)
            _taken.extend([_recent, _recent+1, _recent+2, _recent-1, _recent-2])
            
            
        # if get == "right":
        #     return  filter(lambda pos: pos >= Chunk.SIZE.x, treesPos)
        # elif get == "left":
        #     return filter(lambda pos: pos < 0, treesPos)
            
        treesPos = filter(lambda pos: pos >= 0 and pos < Chunk.SIZE.x, treesPos)
        
        newBlocks = {}
        for pos in treesPos:
            heightTree = self.generateHeight(pos, list(chunkPos), self.getScene().getSeedInt(), self.__cache['grass_height'], False, min=70, max=80, seedName="height", startPoint=75)
            newBlocks[(pos,heightTree-1)] = "oak_wood"
            newBlocks[(pos,heightTree-2)] = "oak_wood"
            newBlocks[(pos,heightTree-3)] = "oak_wood"
            newBlocks[(pos,heightTree-4)] = "oak_wood"
            newBlocks[(pos,heightTree-5)] = "oak_leaves"
            newBlocks[(pos+1,heightTree-4)] = "oak_leaves"
            newBlocks[(pos-1,heightTree-4)] = "oak_leaves"
            newBlocks[(pos+1,heightTree-3)] = "oak_leaves"
            newBlocks[(pos-1,heightTree-3)] = "oak_leaves"
            newBlocks[(pos+2,heightTree-3)] = "oak_leaves"
            newBlocks[(pos-2,heightTree-3)] = "oak_leaves"
            
        
            # print(newBlocks)
        if get == "left":
            return {(key[0]-Chunk.SIZE.x, key[1]): item for key, item in newBlocks.items() if key[0] >= Chunk.SIZE.x}
        elif get == "right":
            return {(Chunk.SIZE.x+key[0], key[1]): item for key, item in newBlocks.items() if key[0] < 0}
        # if get == "right": 
        #     # _f = dict(filter(lambda pos: pos.keys()[0] < 0, newBlocks))
        #     # print(_f)
        #     return {()}
        #     return {(Chunk.SIZE.x+key[0], key[1]): item for key, item in newBlocks.items() if key[0] >= Chunk.SIZE.x }
        #     # return filter(lambda pos: pos.keys()[0] < 0, newBlocks)
        # elif get == "left":
        #     # _f = dict(filter(lambda pos: pos.keys()[0] >= Chunk.SIZE.x, newBlocks))
        #     return {(key[0]-Chunk.SIZE.x, key[0]): item for key, item in newBlocks.items() if key[0] < 0}
        
        _final = {key: item for key, item in newBlocks.items() if key[0] >= 0 and key[0] < Chunk.SIZE.x}
        _final.update(fromLeft)
        _final.update(fromRight)
        
        print('dw', _final, newBlocks)
        for pos, block in _final.items():
            Block.newBlockByResourceManager(
                chunk=chunk,
                name=block,
                blockPos=pos,
                executor=self,
                reason=Reason.WorldGenerator
            )
            
       
            
                
        # treesPos = [pos for pos in treesPos if pos not in _err]
        # for tree in treesPos:
        #     heightTree = self.generateHeight(tree, list(chunkPos), self.getScene().getSeedInt(), self.__cache['grass_height'], False, min=70, max=80, seedName="height", startPoint=75)
            
        #     blocks[(tree, heightTree-1)] = Block.newBlockByResourceManager(
        #         chunk=chunk,
        #         name="oak_wood",
        #         blockPos=Vector2(tree,heightTree-1),
        #         executor=self,
        #         reason=Reason.WorldGenerator,
        #     )
            
        #     blocks[(tree, heightTree-2)] = Block.newBlockByResourceManager(
        #         chunk=chunk,
        #         name="oak_wood",
        #         blockPos=(tree,(heightTree-2)),
        #         executor=self,
        #         reason=Reason.WorldGenerator,
        #     )
            
        #     blocks[(tree, heightTree-3)] = Block.newBlockByResourceManager(
        #         chunk=chunk,
        #         name="oak_wood",
        #         blockPos=Vector2(tree,heightTree-3),
        #         executor=self,
        #         reason=Reason.WorldGenerator,
        #     )
            
        return blocks
         
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
        """Function to generate ores in specified chunk (VERSION TWO)

        Args:
            chunkPos (tuple[int,int]): position of chunk which generates ores
            chunk (Optional[Chunk]): orginalChunk
            blockName (str): block id
            howMuchVeinsMin (int): how much veins will be generated (minimum)
            howMuchVeinsMax (int): how much veins will be generated (maximum)
            minInVein (int): how much ores can be generated in one vein (minimum)
            maxInVein (int):  how much ores can be generated in one vein (maximum)
            recursive (bool, optional): If that function will be invoked by itself for neighbouring chunks with objective to get ores that will appear in main chunk. Default is True.
            fromWhatSide (None | str, optional): by which chunk it was executed
            blocks (dict[tuple[int, int], Block], optional): blocks that are in the main chunk
            minY (int, optional): minimal y to generate a ore
            maxY (int, optional): maximum y to generate a ore
        """
        
             # getting ores from neighbouring chunks
        if recursive:
            fromLeft = self.generateVeins(chunkPos=(chunkPos[0]-1, chunkPos[1]), chunk=chunk, blockName=blockName, howMuchVeinsMin=howMuchVeinsMin, howMuchVeinsMax=howMuchVeinsMax, minInVein=minInVein, maxInVein=maxInVein, recursive=False, fromWhatSide='left', blocks=blocks, minY=minY,maxY=maxY)
            fromRight = self.generateVeins(chunkPos=(chunkPos[0]+1, chunkPos[1]), chunk=chunk, blockName=blockName, howMuchVeinsMin=howMuchVeinsMin, howMuchVeinsMax=howMuchVeinsMax, minInVein=minInVein, maxInVein=maxInVein, recursive=False, fromWhatSide='right', blocks=blocks, minY=minY,maxY=maxY)
        
        # setting seed
        random.seed(f"${self.getScene().getSeed()}_CHUNK_{int(chunkPos[0])}_VEINS_{blockName}")    
        
        howManyVeins: int = random.randint(howMuchVeinsMin, howMuchVeinsMax)
        everyVein: list[tuple[int,int]] = []
        
        # moles
        for veinNumber in range(0, howManyVeins):
            # intialize mole
            blocksMole: list[tuple[int,int]] = []
            howManyInThisVein = random.randint(minInVein, maxInVein)
            choices: list[list[int,int]] = [[1, 0], [-1, 0], [0, 1], [0, -1]] 
            # choices: list[list[int,int]] = [[1, 0]] 
            
            # first block
            currentBlock: tuple[int,int] = (random.randint(0, Chunk.SIZE.x-1), random.randint(minY, maxY))
        
            blocksMole.append((currentBlock[0], currentBlock[1]))
            
            while True:                
                # end if no choices
                if len(choices) <= 0:
                    everyVein.extend(blocksMole)
                    break
                
                # go forward
                addx, addy = random.choice(choices)
                
                # if there was block already here
                if (currentBlock[0]+addx, currentBlock[1]+addy) in blocksMole:
                    choices.remove([addx,addy])
                    continue
                
                # if succeeded
                blocksMole.append((currentBlock[0]+addx, currentBlock[1]+addy))
                choices: list[list[int,int]] = [[1, 0], [-1, 0], [0, 1], [0, -1]] 
                currentBlock: tuple[int,int] = (currentBlock[0]+addx, currentBlock[1]+addy)
                
                # if enough blocks
                if len(blocksMole) >= howManyInThisVein:
                    everyVein.extend(blocksMole)
                    break
                
        # return if fromWhatSide is not None (for recursive)
        if fromWhatSide is not None:
            if fromWhatSide == "right":
                return list(filter(lambda block: block[0] < 0, everyVein))
            elif fromWhatSide == "left":
                return list(filter(lambda block: block[0] >= Chunk.SIZE.x, everyVein))
            

            
        # final
        
        
        # first = list(map(lambda ore: (int(Chunk.SIZE.x+ore[0]), ore[1]), fromRight))
        # if len(first) > 1:
        #     first = first[0]
        #     self.getScene().getGame().camera.cords = Vector2(first[0] * Block.SIZE.x + chunk.getStartingPoint()[0], first[1] * Block.SIZE.y + chunk.getStartingPoint()[1])
            
        # first = list(map(lambda ore: (ore[0]-chunk.SIZE.x+1, ore[1]), fromRight))
        # if len(first) > 1:
        #     first = first[0]
        #     self.getScene().getGame().camera.cords = Vector2(first[0] * Block.SIZE.x + chunk.getStartingPoint()[0], first[1] * Block.SIZE.y + chunk.getStartingPoint()[1])
        
        everyVein.extend(map(lambda ore: (int(ore[0]-chunk.SIZE.x), ore[1]), fromLeft))
        everyVein.extend(map(lambda ore: (int(Chunk.SIZE.x+ore[0]), ore[1]), fromRight))
        
        
        
        
        # def oreRepair(ore):
        #     if ore[0] < 0:
        #         print('da', ore[0], (abs(ore[0]), ore[0]))
        #         return (abs(ore[0]), ore[0])
        #     elif ore[0] >= Chunk.SIZE.x:
        #         print('da', ore[0], (abs(ore[0]), ore[0]))
        #         return (abs(ore[0])-Chunk.SIZE.x+1, ore[1])
        #     else:
        #         return ore
            
            
        # everyVein = list(map(oreRepair, everyVein))
        

        for block in everyVein:
            if block in blocks and blocks[block].ID == "stone":
                blocks[block].kill()
                del blocks[block]
                Block.newBlockByResourceManager(
                    chunk=chunk,
                    name=blockName,
                    blockPos=block,
                    executor=self,
                    reason=Reason.WorldGenerator
                )
                
       
                
                
                
                    
                
                
            
            
            
            
        
    
    # def generateVeins(self, chunkPos: tuple[int,int], chunk: Optional[Chunk], blockName: str, howMuchVeinsMin: int, howMuchVeinsMax: int, minInVein: int, maxInVein: int, recursive: bool = True, fromWhatSide: None|str = None, blocks: dict[tuple[int, int], Block] = {}, minY: int=0, maxY: int = Chunk.SIZE.y) -> dict[tuple[int, int], Block]: 
    #     """Function to generate ores in specified chunk

    #     Args:
    #         chunkPos (tuple[int,int]): position of chunk which generates ores
    #         chunk (Optional[Chunk]): orginalChunk
    #         blockName (str): block id
    #         howMuchVeinsMin (int): how much veins will be generated (minimum)
    #         howMuchVeinsMax (int): how much veins will be generated (maximum)
    #         minInVein (int): how much ores can be generated in one vein (minimum)
    #         maxInVein (int):  how much ores can be generated in one vein (maximum)
    #         recursive (bool, optional): If that function will be invoked by itself for neighbouring chunks with objective to get ores that will appear in main chunk. Default is True.
    #         fromWhatSide (None | str, optional): by which chunk it was executed
    #         blocks (dict[tuple[int, int], Block], optional): blocks that are in the main chunk
    #         minY (int, optional): minimal y to generate a ore
    #         maxY (int, optional): maximum y to generate a ore

    #     Returns:
    #         dict[tuple[int, int], Block]: _description_
    #     """
    #     # return {}
        
        
        
    #     # getting ores from neighbouring chunks
    #     if recursive:
    #         fromLeft = self.generateVeins(chunkPos=(chunkPos[0]+1, chunkPos[1]), chunk=chunk, blockName=blockName, howMuchVeinsMin=howMuchVeinsMin, howMuchVeinsMax=howMuchVeinsMax, minInVein=minInVein, maxInVein=maxInVein, recursive=False, fromWhatSide='left', blocks=blocks, minY=minY,maxY=maxY)
    #         fromRight = self.generateVeins(chunkPos=(chunkPos[0]+1, chunkPos[1]), chunk=chunk, blockName=blockName, howMuchVeinsMin=howMuchVeinsMin, howMuchVeinsMax=howMuchVeinsMax, minInVein=minInVein, maxInVein=maxInVein, recursive=False, fromWhatSide='right', blocks=blocks, minY=minY,maxY=maxY)
            
    #     # setting seed
    #     random.seed(f"${self.getScene().getSeed()}_CHUNK_{chunkPos}_VEINS_{blockName}")    
        
    #     # randomize how many veins will be in this chunk
    #     howmuchveins: int = random.randint(howMuchVeinsMin, howMuchVeinsMax)
      
        
    #     # used in recursive, lists for collecting ores that would respawn beyond current chunk
    #     rightBlocks: list[tuple[int, int]] = []
    #     leftBlocks: list[tuple[int, int]] = []
        
    #     # only for debugging
    #     gina = []
        
    #     # loop that are executed for every vein
    #     veins = 0
    #     while veins < howmuchveins:
    #         # randomize how much ores will be in this vein
    #         howmuchInVein: int = random.randint(minInVein, maxInVein)
    #         # randomize location of first ore
    #         x = random.randint(0, Chunk.SIZE.x-1)
    #         y = random.randint(minY, maxY)
            
    #         # for debugging
    #         gina.append((x,y))

    #         # check if this Orginal chunk (not from recursive)
    #         if fromWhatSide == None:
    #             # check if this space is available
    #             if not((x,y) in blocks and blocks[(x,y)].ID == "stone"): continue
                
    #             # replace stone with ore
    #             blocks[(x,y)].kill()
    #             blocks[(x,y)] = Block.newBlockByResourceManager(
    #             chunk=chunk,
    #             name="coal_ore",
    #             cordsRelative=Vector2(x * Block.SIZE.x, y * Block.SIZE.y),
    #             executor=self,
    #             reason=Reason.WorldGenerator
    #             )
                
    #         # if it went that far, that means that location of vein can be correct
    #         veins += 1
            
    #         # intialize a mole that will look for locations of new ores in this vein
    #         howManyHasGenerated: int = 1
    #         choices = [[1, 0], [-1, 0], [0, 1], [0, -1]] 
            
    #         # loop for the mole
    #         while howManyHasGenerated < howmuchInVein:
    #             # if there's no choices, then it's probably means that mole is either in loop or there's no more space
    #             if len(choices) <= 0: break
                
    #             # that was for debugging, to check if that's fault of bad seeding
    #             # random.seed(f"${self.getScene().getSeed()}_CHUNK_{chunkPos}_VEINS_{blockName}_{x}_{y}")
                
    #             # randomize direction in which mole will go
    #             addx, addy = random.choice(choices)
                
    #             # remove that from choices
    #             choices.remove([addx,addy])
                
    #             # debugging
    #             gina.append((x+addx, y+addy))
                
    #             # if this orginal chunk (not from recursive)
    #             if fromWhatSide == None:
    #                 # check if that space is available
    #                 if not((x+addx,y+addy) in blocks and blocks[(x+addx,y+addy)].ID == "stone"): continue
                    
    #                 # replace stone with a new ore, if that's not beyond chunk
    #                 if not(x+addx > Chunk.SIZE.x - 1 or x+addx < 0 or y+addy < 0 or y+addy > Chunk.SIZE.y-1):
    #                     blocks[(x+addx,y+addy)].kill()
    #                     # print('s',blocks[(x+addx,y+addy)])
    #                     blocks[(x+addx,y+addy)] = Block.newBlockByResourceManager(
    #                         chunk=chunk,
    #                         name="coal_ore",
    #                         cordsRelative=Vector2((x+addx)* Block.SIZE.x, (y+addy) * Block.SIZE.y),
    #                         executor=self,
    #                         reason=Reason.WorldGenerator
    #                         )
                    
    #                 # get back the full set of choices
    #                 choices = [[1, 0], [-1, 0], [0, 1], [0, -1]] 
                        
    #             # handling ores that went too far to the right
    #             if x+addx > Chunk.SIZE.x and fromWhatSide=="right": 
    #                 print(gina)
    #                 rightBlocks.append((x+addx-Chunk.SIZE.x, y))
    #                 # print((x,y))
    #                 # print(x+addx)
    #                 # rightBlocks[(x+addx - (Chunk.SIZE.x-1), y)] = Block.newBlockByResourceManager(
    #                 # chunk=chunk,
    #                 # name="coal_ore",
    #                 # cordsRelative=Vector2((x+addx - (Chunk.SIZE.x-1))* Block.SIZE.x, y * Block.SIZE.y),
    #                 # executor=self,
    #                 # reason=Reason.WorldGenerator
    #                 # )

    #             # handling ores that went too far to the left
    #             elif x+addx < 0 and fromWhatSide=="left": 
    #                 print(Chunk.SIZE.x-(x+addx), x, x+addx)
    #                 print(gina)
    #                 leftBlocks.append((Chunk.SIZE.x+(x+addx), y))
    #                 # leftBlocks[abs(x+addx), y] = Block.newBlockByResourceManager(
    #                 # chunk=chunk,
    #                 # name="coal_ore",
    #                 # cordsRelative=Vector2(abs(x+addx)* Block.SIZE.x, y * Block.SIZE.y),
    #                 # executor=self,
    #                 # reason=Reason.WorldGenerator
    #                 # )
                    
                
    #             # prepare next iteration of the mole
    #             x += addx
    #             y += addy
    #             howManyHasGenerated += 1
                
    #     # if that was recursive, just return values
    #     if fromWhatSide == "right": return rightBlocks
    #     elif fromWhatSide == "left": return leftBlocks
        
    #     # add ores that was generated by neigbhouring chunk from the left
    #     for cords in fromLeft:
    #         cords = (int(cords[0]), int(cords[1]))
    #         blocks[cords].kill()
    #         del blocks[cords]
    #         # blocks[cords] = Block.newBlockByResourceManager(
    #         #     chunk=chunk,
    #         #     name="coal_ore",
    #         #     cordsRelative=Vector2(cords[0] * Block.SIZE.x, cords[1] * Block.SIZE.y),
    #         #     executor=self,
    #         #     reason=Reason.WorldGenerator
    #         #     )
            
    #     # add ores that was generated by neigbhouring chunk from the right
    #     for cords in fromRight:
    #         cords = (int(cords[0]), int(cords[1]))
    #         blocks[cords].kill()
    #         del blocks[cords]
    #         # blocks[cords] = Block.newBlockByResourceManager(
    #         #     chunk=chunk,
    #         #     name="coal_ore",
    #         #     cordsRelative=Vector2(cords[0] * Block.SIZE.x, cords[1] * Block.SIZE.y),
    #         #     executor=self,
    #         #     reason=Reason.WorldGenerator
    #         #     )
                
                
    #     # for cords, block in fromLeft.items():
    #     #     print(cords in blocks and blocks[cords].ID == "stone")
    #     #     if cords in blocks and blocks[cords].ID == "stone":
    #     #         blocks[cords].kill
    #     #         del blocks[cords]
                
    #     #         # blocks[cords] = block
    #     #         # print('s', chunkPos, fromLeft, fromRight, cords)
    #     #         self.getScene().getGame().camera.cords = Vector2(cords[0] * Block.SIZE.x,
    #     #                                                             cords[1] * Block.SIZE.y)
    #     #         # print(blocks)  
    #     #         # print("\n\n\n") 
                    
    #     # for cords, block in fromRight.items():
    #     #     print(cords in blocks and blocks[cords].ID == "stone")
    #     #     if cords in blocks and blocks[cords].ID == "stone":
    #     #         self.getScene().remove(blocks[cords])
    #     #         blocks[cords].kill()
    #     #         del blocks[cords]
    #     #         # print(blocks[cords])
    #     #         # blocks[cords] = block
    #     #         # print('s', chunkPos, fromLeft, fromRight, cords)
    #     #         self.getScene().getGame().camera.cords = Vector2(cords[0] * Block.SIZE.x,
    #     #                                                          cords[1] * Block.SIZE.y)
    #     #         # print(blocks)   
    #     #         # print("\n\n\n")
                
        
    #     # return final result
    #     return blocks
        
            
        
    async def __waitForAnother(self): pass
        

    async def generateChunk(self, chunkPos: tuple[int, int], chunk: 'Chunk', Scene: 'Scene') -> dict[tuple[int, int], Block]:
        blocks: dict[tuple[int,int], Block] = {}
        
        
        random.seed(f"${self.getScene().getSeed()}_CHUNK_{chunkPos}")
        
        for x in range(0,int(Chunk.SIZE.x)):
            height = self.generateHeight(x, list(chunkPos), self.getScene().getSeedInt(), self.__cache['grass_height'], False, min=70, max=80, seedName="height", startPoint=75)
            blocks[(x,height)] = Block.newBlockByResourceManager(
                chunk=chunk,
                name="grass_block",
                blockPos=Vector2(x,height),
                executor=self,
                reason=Reason.WorldGenerator
            )
            
            dirtheight = self.generateHeight(x, list(chunkPos), self.getScene().getSeedInt(), self.__cache['dirt_height'], False, startPoint=4, max=5, min=3, seedName="dirtheight")
            
            
            for y in range(0,dirtheight):
                blocks[(x,height+y+1)] = Block.newBlockByResourceManager(
                    chunk=chunk,
                    name="dirt",
                    blockPos=(x,height + 1 + y),
                    executor=self,
                    reason=Reason.WorldGenerator
                )
                
            currentHeight = height + dirtheight + 1
            for y in range(0,200):
                blocks[(x,y+currentHeight)] = Block.newBlockByResourceManager(
                    chunk=chunk,
                    name="stone",
                    blockPos=(x,y + currentHeight),
                    executor=self,
                    reason=Reason.WorldGenerator
                ) 
                if y + currentHeight >= 200:   
                    bedrockHeight = self.generateHeight(x, list(chunkPos), self.getScene().getSeedInt(), self.getScene().heightCache['bedrock_height'], False, startPoint=2, max=2, min=1, probability=20)
                    
                    if bedrockHeight == 1:
                        blocks[(x,y+currentHeight + 1)] = Block.newBlockByResourceManager(
                            chunk=chunk,
                            name="stone",
                            blockPos=(x,y + currentHeight + 1),
                            executor=self,
                            reason=Reason.WorldGenerator
                        )
                        blocks[(x,y+currentHeight + 2)] = Block.newBlockByResourceManager(
                            chunk=chunk,
                            name="bedrock",
                            blockPos=(x,y + currentHeight + 2),
                            executor=self,
                            reason=Reason.WorldGenerator
                        ) 
                    else:
                        blocks[(x,y+currentHeight + 1)] = Block.newBlockByResourceManager(
                            chunk=chunk,
                            name="bedrock",
                            blockPos=(x,y + currentHeight + 1),
                            executor=self,
                            reason=Reason.WorldGenerator
                        )
                        blocks[(x,y+currentHeight + 2)] = Block.newBlockByResourceManager(
                            chunk=chunk,
                            name="bedrock",
                            blockPos=(x,y + currentHeight + 2),
                            executor=self,
                            reason=Reason.WorldGenerator
                        ) 
                    break
                
        # ores
        await asyncio.sleep(0.1)
        self.generateVeins(chunkPos=chunkPos,
                           chunk=chunk,
                           blockName="coal_ore",
                           howMuchVeinsMin=10,
                           howMuchVeinsMax=16,
                           minInVein=2,
                           maxInVein=4,
                           recursive=True,
                           fromWhatSide=None,
                           blocks=blocks,
                           minY=60,
                           maxY=170)
        
        await asyncio.sleep(0.1)
        self.generateVeins(chunkPos=chunkPos,
                           chunk=chunk,
                           blockName="iron_ore",
                           howMuchVeinsMin=2,
                           howMuchVeinsMax=6,
                           minInVein=2,
                           maxInVein=4,
                           recursive=True,
                           fromWhatSide=None,
                           blocks=blocks,
                           minY=90,
                           maxY=150)
        
        await asyncio.sleep(0.1)
        self.generateVeins(chunkPos=chunkPos,
                           chunk=chunk,
                           blockName="iron_ore",
                           howMuchVeinsMin=2,
                           howMuchVeinsMax=5,
                           minInVein=2,
                           maxInVein=4,
                           recursive=True,
                           fromWhatSide=None,
                           blocks=blocks,
                           minY=151,
                           maxY=185)
        
        await asyncio.sleep(0.1)
        self.generateVeins(chunkPos=chunkPos,
                           chunk=chunk,
                           blockName="coal_ore",
                           howMuchVeinsMin=2,
                           howMuchVeinsMax=4,
                           minInVein=2,
                           maxInVein=3,
                           recursive=True,
                           fromWhatSide=None,
                           blocks=blocks,
                           minY=151,
                           maxY=190)
        
        await asyncio.sleep(0.1)
        self.generateVeins(chunkPos=chunkPos,
                           chunk=chunk,
                           blockName="diamond_ore",
                           howMuchVeinsMin=1,
                           howMuchVeinsMax=2,
                           minInVein=1,
                           maxInVein=2,
                           recursive=True,
                           fromWhatSide=None,
                           blocks=blocks,
                           minY=170,
                           maxY=200)
        
        await asyncio.sleep(0.1)
        self.generateTress(chunkPos, chunk, blocks, 1, 2)
        
        # self.generateVeins(chunkPos, chunk, "coal_ore", 1, 1, 6, 6, True, None, blocks, currentHeight+3, 32)
        
        global stats
        
       
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
        