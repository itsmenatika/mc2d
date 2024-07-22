from pygame import Surface, Vector2
from typing import Optional
from bin.map import Block, Chunk
from bin.abstractClasses import Reason, Executor
from bin.event import Event


class allium(Block):
    MAINTEXTURE = "tiles/allium.png"
    MAINTEXTUREISTRANSPARENT = True
    ID = "allium"
    IDInt = 19
    
    @staticmethod
    def onPlaceAttempt(blockPosAbsolute: tuple[int,int], inChunkPosition: tuple[int,int], chunk: Chunk, event: Event, reason: Optional[Reason] = None, executor: Optional[Executor] = None, changingBlock: bool = False) -> None:
        block = chunk.getScene().getBlockByAbsPos((blockPosAbsolute[0], blockPosAbsolute[1]+1))
        
        if block == None or block.ID not in ("dirt", "grass_block"):
            event.prevent()
   
    def onUpdate(self, blockPosAbsolute: tuple[int, int], inChunkPosition: tuple[int, int], chunk, reason: Reason | None = None, executor: Executor | None = None) -> None:
        block = self.getBlockDown()
        if block == None or block.ID not in ("dirt", "grass_block"):
            self.setToAir(executor=executor, reason=reason)

        
    def __init__(self, image: Surface, blockPos: Vector2, chunk: Chunk, executor: Executor | None = None, reason: str | None = None, addToEverything: bool = True) -> None:
        super().__init__(image, blockPos, chunk, executor, reason, addToEverything)
    