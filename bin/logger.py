from enum import Enum
from typing import Optional
import traceback
import sys
import platform
import psutil
import os
from datetime import datetime


# # Enumerator kolorów
# class ColorType(Enum):
#     BLACK        = "\033[0;30m"
#     RED          = "\033[0;31m"
#     GREEN        = "\033[0;32m"
#     BROWN        = "\033[0;33m"
#     BLUE         = "\033[0;34m"
#     PURPLE       = "\033[0;35m"
#     CYAN         = "\033[0;36m"
#     LIGHT_GRAY   = "\033[0;37m"
#     DARK_GRAY    = "\033[1;30m"
#     LIGHT_RED    = "\033[1;31m"
#     LIGHT_GREEN  = "\033[1;32m"
#     YELLOW       = "\033[1;33m"
#     LIGHT_BLUE   = "\033[1;34m"
#     LIGHT_PURPLE = "\033[1;35m"
#     LIGHT_CYAN   = "\033[1;36m"
#     LIGHT_WHITE  = "\033[1;37m"
#     END          = "\033[0m"


class logType(Enum):
    '''type of log message'''
    Warning = "warning"
    ERROR = "error"
    INFO = "info"
    CRASHREPORT = "CRASHREPORT"
    PYTHONERROR = "PYTHONERROR"
    INIT = "init"
    SUCCESS = "success"
    
class ParentForLogs:
    '''This is node which indicates where you are (this will as indicator in logs (name will be between dots))'''
    def getParent(self) -> 'ParentForLogs':
        '''returns parent of this node'''
        return self.__parent
    
    def getFull(self) -> str:
        '''get full indicator'''
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
    '''Logger is used to loging stuff. Only one with intialized during the game.'''
    
    logFile = "data/logs/latest.log"
    
    def errorWithTraceback(self, message: str, error: Exception) -> None:
        '''logs error with traceback\n
            Args:\n
                * message: str -> message about why that has happen
                * error: Exception -> exception
            Returns:\n
                None'''
        tb = traceback.format_exc()
        self.log(logType.ERROR, message + '\n' + str(tb))
        
    def log(self, logtype: logType, message: str, parent: Optional[ParentForLogs] = None):
        '''function which should be used to logging stuff\n
            Args:\n
                * logtype: logType -> type of log
                * message: str -> message about why that has happen
                * parent: Optional[ParentForLogs] -> optional argument. That is where you indicates "path for error"
            Returns:\n
                None'''

        fromWhere = "gameEngine" if not parent else str(parent)
        timenow = datetime.now().time().strftime("%X:%f")
            
        finalMessage = f"{timenow} [{fromWhere}/{logtype.value}]: {message}"
        self.__logs.append(finalMessage)
        
        print(finalMessage)
        
        with open(self.logFile, "a+") as f:
            f.write(finalMessage+"\n")
        
    def clear(self) -> None:
        '''clear all logs'''
        self.__logs.clear()
        
    def getLogs(self) -> list[str]:
        '''Returns all logs'''
        return self.__logs
    
    def getGame(self) -> 'Game':
        '''just gives you the game'''
        return self.__game
    
    def getCurrentScene(self) -> 'Scene':
        '''gives you the current main scene that is running in the game'''
        return self.__game.getCurrentScene()
    
    def __init__(self, game: 'Game') -> None:
        self.__game = game
        self.__logs: list[str] = []
        
        # YOU REALLY SHOULD KEEP IT, THAT ERASES PREVIOUS LOGS        
        with open(self.logFile, 'w') as f:
            pass
        
      
        date = datetime.now()
        ram = psutil.virtual_memory()
        
        self.log(logType.INIT, "---------------------")
        self.log(logType.INIT, f"Logs for mc2D, VERSION OF mc2D: {self.__game.getVersion()} (INT VERSION: {self.__game.getVersionInt()})")
        self.log(logType.INIT, "")
        self.log(logType.INIT, f"date: {date}")
        self.log(logType.INIT, f"System: {platform.system()}")
        self.log(logType.INIT, f"System\'s version: {platform.version()}")
        self.log(logType.INIT, f"Architecture: {platform.machine()}")
        self.log(logType.INIT, f"Processor: {platform.processor()}")
        self.log(logType.INIT, "")
        self.log(logType.INIT, f"Total available ram: {round(ram.total / (1024.0 ** 3),3)}GB")
        self.log(logType.INIT, f"Total available ram to allocate: {round(ram.available / (1024.0 ** 3),3)}GB")
        self.log(logType.INIT, f"RAM In-use: {ram.percent}%")
        self.log(logType.INIT, "")
        self.log(logType.INIT, f"Python compiler: {platform.python_compiler()}")
        self.log(logType.INIT, "---------------------")
        
        
class Loggable:
    '''this class should be inherited by every class that want to be Loggable. That class provides you with useful pack of functions to logging your self'''
    
    def info(self, message: str) -> None:
        '''shortcut for self.log(logType.INFO, message)'''
        self.log(logType.INFO, message)
        
    def logErr(self, message: str) -> None:
        '''shortcut for self.log(logType.ERROR, message)'''
        self.log(logType.ERROR, message)
        
    def log(self, logtype: logType, message: str) -> None:

        self.getGame().getLogger().log(logtype, message, self.__logParent)
        
    def errorWithTraceback(self, message: str, error: Exception) -> None:
        tb = traceback.format_exc()
        self.log(logType.ERROR, message + '\n' + str(tb))
        
    def getLogParent(self) -> ParentForLogs:
        return self.__logParent
    
    def setLogParent(self, parentForLogs: ParentForLogs) -> None:
        self.__logParent = parentForLogs
        
    def getGame(self) -> 'game':
        return self.__game
    
    def __init__(self, *args, **kwargs) -> None:
        if not "logParent" in kwargs:
            return
        
        if "game" in kwargs:
            self.__game = kwargs['game']
        
        self.__logParent = kwargs['logParent']

        