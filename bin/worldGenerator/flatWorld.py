from bin.abstractClasses import WorldGenerator, Reason
from bin.logger import logType
from bin.map import Chunk, Scene, Block
import asyncio

class flatWorldGenerator(WorldGenerator):
    async def generateChunk(self, chunkPos: tuple[int, int], chunk: 'Chunk', Scene: 'Scene'):
        self.log(logType.INFO, f"generating chunk {chunkPos}...")
        
        for x in range(0, int(Chunk.SIZE.x)):
            Block.newBlockByResourceManager(name="grass_block", 
                                            blockPos=(x,35),
                                            executor=self,
                                            reason=Reason.worldGenerator,
                                            chunk=chunk)

            for g in range(0,5):
                Block.newBlockByResourceManager(name="dirt", 
                                            blockPos=(x,36+g),
                                            executor=self,
                                            reason=Reason.worldGenerator,
                                            chunk=chunk) 
            
            for g in range(0+g,60+g):
                Block.newBlockByResourceManager(name="stone", 
                                            blockPos=(x,36+g),
                                            executor=self,
                                            reason=Reason.worldGenerator,
                                            chunk=chunk) 

                
            Block.newBlockByResourceManager(name="bedrock", 
                                            blockPos=(x,36+g+1),
                                            executor=self,
                                            reason=Reason.worldGenerator,
                                            chunk=chunk)                
            
            await asyncio.sleep(0.1)
            
        self.log(logType.SUCCESS, f"generating chunk {chunkPos}... DONE")
        