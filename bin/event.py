from typing import Optional, Callable
import asyncio
from bin.abstractClasses import Executor
from bin.logger import Loggable

class eventError(Exception): pass

class event(Executor, Loggable):
    '''class to easy manage preventing events'''
    defaultName = "unkownEvent"
    
    def isWaiting(self) -> bool: 
        '''check if event still waits for execution'''
        return self.__waiting
    
    def do(self) -> None:
        '''forces event to execute. Only use if that required to specified purpose. Internal code of the game will rather not use this function because its time-consuming!'''
        if self.__waiting != True:
            self.logErr("trying to execute event, but event was already executed!")
            
        
        if self.__kwargs == None and self.__args == None:
            if self.__createAsyncioTask:
                asyncio.create_task(self.__callback(), name=self.__shownName)
            else:
                self.__callback()
        elif self.__kwargs != None and self.__args == None:
            if self.__createAsyncioTask:
                asyncio.create_task(self.__callback(**self.__kwargs), name=self.__shownName)
            else:
                self.__callback(**self.__kwargs)
        else:
            if self.__createAsyncioTask:
                asyncio.create_task(self.__callback(*self.__args, **self.__kwargs), name=self.__shownName)
            else:
                self.__callback(*self.__args, **self.__kwargs)
        self.__waiting = False
        
    
    def prevent(self) -> None:
        if not self.__waiting:
            self.logErr("trying to prevent event, but event was already prevented!")
        self.__waiting = False
        
        
    def __init__(self, callback: Callable, argsForCallback: Optional[list] = None, kwargsForCallback: Optional[dict] = None, shownName: Optional[str] = None, createAsyncioTask: bool = False) -> None:
        self.__waiting: bool = True
        self.__callback = callback
        self.__createAsyncioTask = createAsyncioTask
        self._args = argsForCallback
        self.__kwargs = kwargsForCallback
        
        if shownName != None:
            self.__shownName = shownName
        else:
            self.__shownName = self.defaultName
        