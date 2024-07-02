from pygame import Surface, Vector2
from bin.map import Block
from bin.map import Chunk
from bin.abstractClasses import Executor


class bedrock(Block):
    MAINTEXTURE = "bedrock.png"
    ID = "bedrock"
    IDInt = 8
    
    def onGenerate(self, cordsRelative: Vector2, cordsAbsolute: Vector2, inChunkPosition: tuple[int,int], chunk: Chunk):
        print(f"bedrock generated in {cordsAbsolute} {inChunkPosition}")

        
    def __init__(self, image: Surface, cordsRelative: Vector2, chunk: Chunk, executor: Executor | None = None, reason: str | None = None) -> None:
        super().__init__(image, cordsRelative, chunk, executor, reason)
        
    