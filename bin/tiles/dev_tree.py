from pygame import Surface, Vector2
from typing import Optional

from bin.map import Block, Chunk
from bin.abstractClasses import Executor, Reason
from bin.event import Event




class dev_tree(Block):
    MAINTEXTURE = "tiles/dev_block.png"
    MAINTEXTUREISTRANSPARENT = False
    ID = "dev_tree"
    IDInt = 18
    
    @staticmethod
    def onPlaceAttempt(blockPosAbsolute: tuple[int,int], inChunkPosition: tuple[int,int], chunk: Chunk, event: Event, background: bool = False, reason: Optional[Reason] = None, executor: Optional[Executor] = None, changingBlock: bool = False) -> None: 
        event.prevent()
        
        scene = chunk.getScene()
        
        scene.setBlockByAbsolutePos((blockPosAbsolute[0], blockPosAbsolute[1]), "oak_wood")
        scene.setBlockByAbsolutePos((blockPosAbsolute[0], blockPosAbsolute[1]-1), "oak_wood")
        scene.setBlockByAbsolutePos((blockPosAbsolute[0], blockPosAbsolute[1]-2), "oak_wood")
        scene.setBlockByAbsolutePos((blockPosAbsolute[0], blockPosAbsolute[1]-3), "oak_wood")
        scene.setBlockByAbsolutePos((blockPosAbsolute[0], blockPosAbsolute[1]-4), "oak_leaves")
        scene.setBlockByAbsolutePos((blockPosAbsolute[0]+1, blockPosAbsolute[1]-3), "oak_leaves")
        scene.setBlockByAbsolutePos((blockPosAbsolute[0]-1, blockPosAbsolute[1]-3), "oak_leaves")
        scene.setBlockByAbsolutePos((blockPosAbsolute[0]+1, blockPosAbsolute[1]-2), "oak_leaves")
        scene.setBlockByAbsolutePos((blockPosAbsolute[0]-1, blockPosAbsolute[1]-2), "oak_leaves")
        scene.setBlockByAbsolutePos((blockPosAbsolute[0]+2, blockPosAbsolute[1]-2), "oak_leaves")
        scene.setBlockByAbsolutePos((blockPosAbsolute[0]-2, blockPosAbsolute[1]-2), "oak_leaves")
            
        # we don't have water yet :c
        # scene.setBlockByAbsolutePos((blockPosAbsolute[0], blockPosAbsolute[1]+i+1), "diamond_block")
    
