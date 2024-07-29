# external imports
import pygame
from pygame.math import Vector2

# internal imports
from bin.entity import Entity, entityType

# ----------------------
# ADDITIONAL INFOMATION
# ----------------------
# 1. You can access any texture that you've specified in class variables by typing just self.[TEXTURE_NAME]_RENDER, 
# because during intialization of the namespace, resourceManager leaves this variable.
# you shall not use pygame.image.load() or similar things because that slower 
# (namespace is intialized once and you use the same texture for multiple objects)
# 2. all files starting with _ will be ignored and won't be loaded by resourceManager (they won't be loaded into game)
# 3. you shouldn't include methods in your class that you want to change! 
# it will just unnecessarily make loading time and size of the file longer/bigger
# 4. File name, class name and string id should be as following: [stringID].py, [stringID], [stringID]
# 5. you can include as many things in this file as you want (even imports or another classes),
# you only can't include any others blocks or entities.
# If you want them use existing methods or resourceManager
# 6. idInt works only for blocks and string id is prioritized
# 7. idInts and stringIds can't be ambigious, you can't use them over again. Every id have to specify one block.
# 8. paths for images, etc. starts with "resources/" you don't need to add that.
# 9. hi?


class _example(Entity):
    ID = "id"
    
    def __init__(self, image: pygame.Surface, chunk: 'Chunk', cords: Vector2, oftype: entityType, forcedUUID: int | None = None, nbtData: dict | None = None):
        super().__init__(image, chunk, cords, oftype, forcedUUID, nbtData)