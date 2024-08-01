from pygame import Surface, Vector2
from typing import Optional
from bin.map import Block, Chunk
from bin.abstractClasses import Reason, Executor
from bin.event import Event


class allium(Block):
    MAINTEXTURE = "tiles/allium.png"
    MAINTEXTUREISTRANSPARENT = True
    ID = "allium"
    IDInt = 20
    
    # lighting information
    
    lightingAbsorption = 0 # tells lighting engine how that should be treated (if that should absorb the light)
    
    @staticmethod
    def onPlaceAttempt(blockPosAbsolute: tuple[int,int], inChunkPosition: tuple[int,int], chunk: Chunk, event: Event, background: bool = False, reason: Optional[Reason] = None, executor: Optional[Executor] = None, changingBlock: bool = False) -> None:
        block = chunk.getScene().getBlockByAbsPos((blockPosAbsolute[0], blockPosAbsolute[1]+1))
        if block == None or block.ID not in ("dirt", "grass_block"):
            event.prevent()
   
    def onUpdate(self, blockPosAbsolute: tuple[int, int], inChunkPosition: tuple[int, int], chunk, background: bool = False, reason: Reason | None = None, executor: Executor | None = None) -> None:
        block = self.getBlockDown()
        if block == None or block.ID not in ("dirt", "grass_block"):
            self.setToAir(executor=executor, reason=reason)

    