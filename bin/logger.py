from enum import Enum
from typing import Optional

import traceback
import sys

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
    def errorWithTraceback(self, message: str, error: Exception) -> None:
            tb = traceback.format_exc()
            self.log(logType.ERROR, message + '\n' + str(tb))
        
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
    def info(self, message: str) -> None:
        self.log(logType.INFO, message)
        
    def log(self, logtype: logType, message: str) -> None:

        self.getGame().getLogger().log(logtype, message, self.__logParent)
        
    def errorWithTraceback(self, message: str, error: Exception) -> None:
        # tb = sys.exc_info()
        # self.log(logType.ERROR, message + '\n' + str(error.with_traceback(tb[2])) + "\n")
        tb = traceback.format_exc()
        self.log(logType.ERROR, message + '\n' + str(tb))
        # tb = sys.exc_info()[2]
        # # traceback.print_exc()
        # # self.getGame().getLogger().log(logType.ERROR, message, self.__logParent)
        # # print( message + "\n" + error.with_traceback(tb) + "\n")
        # self.log(logType.ERROR, message + "\n" + error.with_traceback(tb) + "\n")
        
    def getLogParent(self) -> ParentForLogs:
        return self.__logParent
    
    def setLogParent(self, parentForLogs: ParentForLogs) -> None:
        self.__logParent = parentForLogs
        
    def getGame(self) -> 'game':
        return self.__game
    
    def __init__(self, *args, **kwargs) -> None:
        if "logParent" in kwargs:
            self.__logParent = kwargs['logParent']
            if "game" in kwargs:
                self.__game = kwargs['game']