from pygame.math import Vector2
from bin.map import Block, Chunk

import time
from typing import Callable
from functools import wraps

def getBlockPosAbsFromCords(cords: Vector2) -> tuple[int,int]:
    return (cords.x // Block.SIZE.x, cords.y // Block.SIZE.y)

def getChunkPosFromCords(cords: Vector2) -> int:
    return cords.x // Chunk.SIZE.x


def timeTrackerPrint(functionSignature: str) -> Callable:
    '''allows you to measure time and then printing it into the console'''
    def timeTrackerPrintInner(function: Callable) -> Callable:
        '''allows you to measure time and then printing it into the console'''
        @wraps(function)
        def tracker(*args, **kwargs):
            start = time.time()
            function(*args, **kwargs)
            end = time.time()
            print(f"{functionSignature} -> {end-start}")
            
        return tracker
    return timeTrackerPrintInner


def timeTrackerPrintAsync(functionSignature: str) -> Callable:
    '''allows you to measure time and then printing it into the console'''
    def timeTrackerPrintAsyncInner(function: Callable) -> Callable:
        '''allows you to measure time and then printing it into the console'''
        @wraps(function)
        async def tracker(*args, **kwargs):
            start = time.time()
            await function(*args, **kwargs)
            end = time.time()
            print(f"{functionSignature} -> {end-start}")
            
        return tracker
    return timeTrackerPrintAsyncInner