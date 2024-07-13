
import abc
from enum import Enum
from typing import Any, TypeAlias

from bin.logger import Loggable, logType, ParentForLogs

ENTITIES = [
    "player",
    ""
]

class Entity(abc.ABC): pass


class Reason(Enum):
    '''reason to perform specified action'''
    WorldGenerator = "world_generator"

class InputType(Enum):
    '''type of input that was given by user'''
    rightClick = "rightClick"
    leftClick = "leftClick"
    keyDown = "keyDown"
    keyUp = "keyUp"
    
class eventType(Enum):
    '''type of event'''
    destroyBlock = "destroy_block"

class Executor(abc.ABC):
    '''class that can execute something'''
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
    
class WorldGenerator(Executor, abc.ABC, Loggable):
    '''world generator that can be used to generate worlds'''
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
    
    @abc.abstractmethod
    def generateChunk(self, chunkPos: tuple[int,int], chunk: 'Chunk', Scene: 'Scene') -> dict[tuple[int,int], 'Block']:
        '''function that will be execute every time when world want new chunk'''
        pass
    
    def __init__(self, scene: 'Scene') -> None:
        super().__init__(logParent=ParentForLogs(name="worldGenerator", parent=scene.getLogParent()))
        self.__scene = scene
        # self.log(logtype.'t')
        
    # idk, how to call it with multiple classes...
    # def __init__(self, executorName: str) -> None:
    #     self.__executorName = executorName
        
        
inputEventInfo: TypeAlias = dict[str, Any]