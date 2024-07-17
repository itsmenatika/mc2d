from pygame import Surface, Vector2
from typing import Optional
from bin.map import Block
from bin.map import Chunk
from bin.abstractClasses import Executor, Reason
from bin.event import Event


class BLOCKID(Block):
    '''just block :3'''
    # basic information about block (info that can be changed in every block)
    MAINTEXTURE: str | None = None  # texture that will be used
    MAINTEXTUREISTRANSPARENT: bool = False # if texture is transparent (that is only for pygame optimization)
    ID: str | None = None   # string ID (UNIQUE, MAIN ID)
    IDInt: int|None = None  # int ID (UNIQUE)
    
    # advanced information about block (info that can be changed in every block)
    listenToMe: bool = False # should game look out for this block to update it necessary (useful for crops or another things like that, that doesn't affect any updates that are caused by other blocks or entities. that's auto updates) {NOT IMPLEMENTED YET}
    listenPriority: int = 1 # priority of listening. The higher the better. {NOT IMPLEMENTED YET}
    
    
    # SCREENSIZE = (1280,720) # SIZE OF SCREEN (IDK IF THAT WAS USED ANYWHERE BUT ILL KEEP IT FOR SECURITY REASONS)
    
    # functions to changed in every block:
    
     

    
    # function run once block is generated by world generator (requirement to be invoked: Reason.worldGenerator)
    def onGenerate(self, cordsRelative: Vector2, cordsAbsolute: Vector2, inChunkPosition: tuple[int,int], chunk: Chunk, executor: Optional[Executor] = None) -> None:
        '''Method executed when chunk is generated, can be changed in every block'''
        pass
    
    # function run once block is loaded from save (requirement to be invoked: Reason.chunkRestore)
    def onLoad(self, cordsRelative: Vector2, cordsAbsolute: Vector2, inChunkPosition: tuple[int,int], chunk: Chunk, executor: Optional[Executor] = None) -> None:  
        '''Method executed when chunk is loaded, can be changed in every block'''
        pass
    
    @staticmethod
    def onPlaceAttempt(blockPosAbsolute: tuple[int,int], inChunkPosition: tuple[int,int], chunk: Chunk, event: Event, reason: Optional[Reason] = None, executor: Optional[Executor] = None, changingBlock: bool = False) -> None:  
        '''method executed when block would be break (if you really want BLOCK OBJECT YOU MUST INTIALIZE EVENT BY event.do() (that function will return object of that block))'''
        pass
    
    def onBreakAttempt(self, blockPosAbsolute: tuple[int,int], inChunkPosition: tuple[int,int], chunk: Chunk, event: Event, reason: Optional[Reason] = None, executor: Optional[Executor] = None) -> None:  
        '''method executed when block would be break'''
        pass
    
    # # TODO: function that run every update
    # # TODO: function that run every update (for listeners)
    
    def update(self, *args, **kwargs):
        raise NotImplementedError('Not implemented')

    def lupdate(self, *args, **kwargs):
        raise NotImplementedError('Not implemented')
        
    # you shouldn't touch too much i in init, only if you're sure what you're doing
    def __init__(self, image: Surface, blockPos: Vector2, chunk: Chunk, executor: Executor | None = None, reason: str | None = None, addToEverything: bool = True) -> None:
        super().__init__(image, blockPos, chunk, executor, reason, addToEverything)
    