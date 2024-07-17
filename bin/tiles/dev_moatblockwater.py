from pygame import Surface, Vector2
from typing import Optional

from bin.map import Block, Chunk
from bin.abstractClasses import Executor, Reason
from bin.event import Event




class dev_moatblockwater(Block):
    MAINTEXTURE = "tiles/dev_block.png"
    MAINTEXTUREISTRANSPARENT = False
    ID = "dev_wallblockwater"
    IDInt = 17
    
    @staticmethod
    def onPlaceAttempt(blockPosAbsolute: tuple[int,int], inChunkPosition: tuple[int,int], chunk: Chunk, event: Event, reason: Optional[Reason] = None, executor: Optional[Executor] = None, changingBlock: bool = False) -> None: 
        event.prevent()
        
        scene = chunk.getScene()
        
        for i in range(0,20):
            scene.setBlockByAbsolutePos((blockPosAbsolute[0], blockPosAbsolute[1]+i), None)
            
        # we don't have water yet :c
        scene.setBlockByAbsolutePos((blockPosAbsolute[0], blockPosAbsolute[1]+i+1), "diamond_block")
    
    def __init__(self, image: Surface, blockPos: Vector2, chunk: Chunk, executor: Executor | None = None, reason: str | None = None, addToEverything: bool = True) -> None:
        super().__init__(image, blockPos, chunk, executor, reason, addToEverything)