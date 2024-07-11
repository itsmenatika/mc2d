from enum import Enum
from typing import Optional

class logType(Enum):
    Warning = "warning"
    ERROR = "error"
    INFO = "info"
    CRASHREPORT = "CRASHREPORT"
    PYTHONERROR = "PYTHONERROR"
    INIT = "init"
    SUCCESS = "success"
    
class ParentForLogs:

    def getParent(self) -> 'ParentForLogs':
        return self.__parent
    
    def getFull(self) -> str:
        final = self.name
        parent = self.getParent()
        
        while parent != None:
            final = parent.name + "." + final
            parent = parent.getParent()
            
        return final
            
    def __str__(self) -> str:
        return self.getFull()
    
    def __init__(self, name: str, parent: Optional['ParentForLogs'] = None) -> None:
        self.name = name
        self.__parent = parent
    

class Logger:
    def log(self, logtype: logType, message: str, parent: Optional[ParentForLogs] = None):
        if parent:
            fromWhere = str(parent)
        else:
            fromWhere = "gameEngine"
            
            
        finalMessage = f"[{fromWhere}/{logtype.value}]: {message}"
        self.__logs.append(finalMessage)
        
        print(finalMessage)
        
    def clear(self) -> None:
        self.__logs.clear()
        
    def getLogs(self) -> list[str]:
        return self.__logs
    
    def getGame(self) -> 'Game':
        return self.__game
    
    def getCurrentScene(self) -> 'Scene':
        return self.__game.getCurrentScene()
    
    def __init__(self, game: 'Game') -> None:
        self.__game = game
        self.__logs: list[str] = []
        
        
class Loggable:
    def log(self, logtype: logType, message: str) -> None:
        self.getGame().getLogger().log(logtype, message, self.__logParent)
        
    def getLogParent(self) -> ParentForLogs:
        return self.__logParent
    
    def setLogParent(self, parentForLogs: ParentForLogs) -> None:
        self.__logParent = parentForLogs
    
    def __init__(self, *args, **kwargs) -> None:
        self.__logParent = kwargs['logParent']