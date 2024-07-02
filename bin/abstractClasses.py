
import abc

ENTITIES = [
    "player",
    ""
]

class Executor(abc.ABC):


    
    
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
    
    # idk, how to call it with multiple classes...
    # def __init__(self, executorName: str) -> None:
    #     self.__executorName = executorName
        