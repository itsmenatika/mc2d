from typing import Optional, Callable
import asyncio
from bin.abstractClasses import Executor, EventType
from bin.logger import Loggable, ParentForLogs
# from bin.map import Chunk, Block, Scene

class EventError(Exception): pass

class Event(Executor, Loggable):
    '''class to easy manage preventing events'''
    defaultName = "unkownEvent"
    
    
    # fast event creating
    # @staticmethod
    # def createBlockPlacementByAbsolutePos(self, scene: 'Scene', blockPos: tuple[int,int], block: str | None | 'Block', dontRaiseErrors: bool = True) -> 'event':
    #     return event(
    #         callback=lambda: scene.setBlockByAbsolutePos(blockPos, block, dontRaiseErrors),
    #         eventType=EventType.blockPlacement
    #     )
      
    
    
    
    def isWaiting(self) -> bool: 
        '''check if event still waits for execution'''
        return self.__waiting
    
    def do(self):
        '''forces event to execute. Only use if that required to specified purpose. Internal code of the game will rather not use this function because its time-consuming! (unless you doesn't care lol|sometimes it's easier to just execute this function)'''
        if self.__waiting != True:
            self.logErr("trying to execute event, but event was already executed!")
            
        
        if self.__kwargs == None and self.__args == None:
            if self.__createAsyncioTask:
                asyncio.create_task(self.__callback(), name=self.__shownName)
            else:
                return self.__callback()
        elif self.__kwargs != None and self.__args == None:
            if self.__createAsyncioTask:
                asyncio.create_task(self.__callback(**self.__kwargs), name=self.__shownName)
            else:
                return self.__callback(**self.__kwargs)
        else:
            if self.__createAsyncioTask:
                asyncio.create_task(self.__callback(*self.__args, **self.__kwargs), name=self.__shownName)
            else:
                return self.__callback(*self.__args, **self.__kwargs)
        self.__waiting = False
        
    
    def prevent(self) -> None:
        if not self.__waiting:
            self.logErr("trying to prevent event, but event was already prevented!")
        self.__waiting = False
        
        
    def getEventType(self) -> EventType:
        return self.__eventType
        
    def __init__(self, callback: Callable, argsForCallback: Optional[list] = None, kwargsForCallback: Optional[dict] = None, shownName: Optional[str] = None, createAsyncioTask: bool = False, eventType: EventType = EventType.unknown, previousParentForLogs: Optional[ParentForLogs] = None, *args, **kwargs) -> None:
        
        self.__waiting: bool = True
        self.__callback = callback
        self.__createAsyncioTask = createAsyncioTask
        self.__args = argsForCallback
        self.__kwargs = kwargsForCallback
        self.__eventType = eventType
        
        if shownName != None:
            self.__shownName = shownName
        else:
            self.__shownName = self.defaultName
            
        super().__init__(logParent=ParentForLogs(f"event_{self.__shownName}", parent=previousParentForLogs))
        