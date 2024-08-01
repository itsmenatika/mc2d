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
        
        if self.__args == None:
            if self.__kwargs == None:
                if not self.__createAsyncioTask:
                    return self.__callback()
                asyncio.create_task(self.__callback(), name=self.__shownName)
            elif self.__kwargs != None:
                if not self.__createAsyncioTask:
                    return self.__callback(**self.__kwargs)
                asyncio.create_task(self.__callback(**self.__kwargs), name=self.__shownName)
        else:
            if not self.__createAsyncioTask:
                return self.__callback(*self.__args, **self.__kwargs)   
            asyncio.create_task(self.__callback(*self.__args, **self.__kwargs), name=self.__shownName) 

               
        self.__waiting = False
        

    def prevent(self) -> None:
        '''prevents event from any execution'''
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

        self.__shownName = shownName if shownName != None else self.defaultName
            
        super().__init__(logParent=ParentForLogs(f"event_{self.__shownName}", parent=previousParentForLogs))
        