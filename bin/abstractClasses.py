
import abc
from enum import Enum
from typing import Any, TypeAlias

ENTITIES = [
    "player",
    ""
]

class Entity(abc.ABC): pass


class Reason(Enum):
    WorldGenerator = "world_generator"

class InputType(Enum):
    rightClick = "rightClick"
    leftClick = "leftClick"
    
class eventType(Enum):
    destroyBlock = "destroy_block"

class Executor(abc.ABC):
    __whoami = None

    def isWorldGenerator(self) -> bool:
        return isinstance(self, WorldGenerator)
    
    def isChunk(self) -> bool:
        return self.__executorName == "chunk"
    
    def isScene(self) -> bool:
        return self.__executorName == "scene" or self.__executorName == "map"
  
    def isPlayer(self) -> bool:
        return self.__executorName == "player"  
    
    def isEntity(self) -> bool:
        return self.__executorName == "player"
    
    def setExecutorName(self, executorName: str) -> None:
        self.__executorName = executorName
    
class WorldGenerator(Executor, abc.ABC):
    __whoami = "worldGenerator"
    
    def getScene(self) -> 'Scene':
        return self.__scene
    
    def getSeed(self) -> tuple[str, int]:
        return (self.__scene.getSeed(), self.__scene.getSeedInt())
    
    def getSeedInt(self) -> int:
        return self.__scene.getSeedInt()
    
    def getSeedOrginal(self) -> str:
        return self.__scene.getSeed()
    
    @abc.abstractmethod
    def generateChunk(self, chunkPos: tuple[int,int], chunk: 'Chunk', Scene: 'Scene') -> dict[tuple[int,int], 'Block']: pass
    
    def __init__(self, scene: 'Scene') -> None:
        self.__scene = scene
        
    # idk, how to call it with multiple classes...
    # def __init__(self, executorName: str) -> None:
    #     self.__executorName = executorName
        
        
inputEventInfo: TypeAlias = dict[str, Any]