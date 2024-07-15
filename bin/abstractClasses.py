
from abc import abstractmethod, ABC
from enum import Enum
from typing import Any, TypeAlias

from bin.logger import Loggable, logType, ParentForLogs

ENTITIES = [
    "player",
    ""
]


inputEventInfo: TypeAlias = dict[str, Any]


class Entity(ABC): pass

class Reason(Enum):
    '''reason to perform specified action'''
    worldGenerator = "world_generator"
    chunkRestore = "chunk_restore"

class InputType(Enum):
    '''type of input that was given by user'''
    rightClick = "rightClick"
    leftClick = "leftClick"
    wheelClick = "wheelClick"
    keyDown = "keyDown"
    keyUp = "keyUp"
    
class eventType(Enum):
    '''type of event'''
    destroyBlock = "destroy_block"

class Executor(ABC):
    __whoami = None

    def isWorldGenerator(self) -> bool:
        return isinstance(self, WorldGenerator)
    
    def isChunk(self) -> bool:
        return self.__executorName == "chunk"
    
    def isScene(self) -> bool:
        return self.__executorName in ["scene", "map"]
  
    def isPlayer(self) -> bool:
        return self.__executorName == "player"  
    
    def isEntity(self) -> bool:
        return self.__executorName == "player"
    
    def setExecutorName(self, executorName: str) -> None:
        self.__executorName = executorName
    
class WorldGenerator(Executor, ABC, Loggable):
    __whoami = "worldGenerator"
    
    def getGame(self) -> 'game':
        return self.__scene.getGame()
    
    def getScene(self) -> 'Scene':
        return self.__scene
    
    def getSeed(self) -> tuple[str, int]:
        return (self.__scene.getSeed(), self.__scene.getSeedInt())
    
    def getSeedInt(self) -> int:
        return self.__scene.getSeedInt()
    
    def getSeedOrginal(self) -> str:
        return self.__scene.getSeed()
    
    @abstractmethod
    def generateChunk(self, chunkPos: tuple[int,int], chunk: 'Chunk', Scene: 'Scene') -> dict[tuple[int,int], 'Block']: pass
    
    def __init__(self, scene: 'Scene') -> None:
        super().__init__(logParent=ParentForLogs(name="worldGenerator", parent=scene.getLogParent()))
        self.__scene = scene
        # self.log(logtype.'t')
        
    # idk, how to call it with multiple classes...
    # def __init__(self, executorName: str) -> None:
    #     self.__executorName = executorName