# external imports
import pygame
from typing import Any
import importlib
import os
import time

# internal imports
from bin.logger import Loggable, logType, ParentForLogs
from bin.map import Block


class unkownNameSpace(Exception): pass
class exceptionThatShouldntBeWrite(Exception): pass
class resourceManager(Loggable):
    shadow_layouts = []

    for alpha in range(255, -17, -17):
        shadow = pygame.surface.Surface((Block.SIZE.x, Block.SIZE.y), flags=pygame.SRCALPHA)

        shadow.fill((0, 0, 0, alpha))

        shadow_layouts.append(shadow)
        
    # no shadow
    # __shadow = pygame.surface.Surface((Block.SIZE.x, Block.SIZE.y), flags=pygame.SRCALPHA)
    # __shadow.fill((0, 0, 0, 0))
    # shadow_layouts.append(__shadow)
    
    def getAmountOfResources(self) -> int:
        return len(self.__resources)
    
    def applyDarkToTexture(self, image: pygame.surface.Surface, lightValue: int) -> pygame.surface.Surface:
        image = image.copy()
        image.blit(self.shadow_layouts[lightValue], (0,0))
        return image
    
    def getTexture(self, name: str, disableTryingToGet: bool = False, **kwargs):
        if len(kwargs) != 0:
            nname = name + "_f%" 
            if 'lightValue' in kwargs: 
                nname += f"l={kwargs['lightValue']}&"
                
            if nname in self.__resources:
                return self.__resources[nname]
            
            image = self.getTexture(name)
            
            if 'lightValue' in kwargs:
                image = self.applyDarkToTexture(image, kwargs['lightValue'])
                
            
            self.__resources[nname] = image
            return self.__resources[nname]
        
        if name in self.__resources:
            return self.__resources[name]
            
        if not disableTryingToGet:
            return self.loadTextureFromFile(name)
        
        

            
    def loadTextureFromFile(self, name: str):
        self.__resources[name] = pygame.image.load(name).convert()
        return self.__resources[name]
    
    def get(self, name: str):
        if name in self.__resources:
            return self.__resources[name]
        
    def getBlockInformation(self, name: str):
        return self.__resources['GAME_NAMESPACE']['blocks'][name]
    
    def loadFromNameSpace(self) -> None:
        self.log(logType.INIT, "intializing namespace...")
        self.__resources['intIds'] = {}
        loc = os.path.dirname(os.path.abspath(__file__))
        
        loc_tiles = os.path.join(loc, "tiles")
        loc_entities = os.path.join(loc, "entities")
        
        # GAME_NAMESPACE['types'] = {
        #     "air": "block",
        #     "none_item": "item"
        # }
        
        
        # setting environment
        GAME_NAMESPACE['environment']['bin_loc'] = loc
        GAME_NAMESPACE['environment']['tiles_loc'] = loc_tiles
        GAME_NAMESPACE['environment']['entities_loc'] = loc_entities
        
        
        # --------------------------------
        # tiles
        # --------------------------------
        
        self.log(logType.INIT, "loading tiles...")
        
        # print(os.listdir(loc_tiles))
        loadedBlocks = 0
        totalBlocks = 0

        tile_modules_name = os.listdir(loc_tiles)
        
        startTime = time.time()
        
        for tile in tile_modules_name:
            name = "".join(tile.split(".")[:-1])
            if name == "__pycache__" or name == "" or name == "_example": continue
            try:
                totalBlocks += 1
                
                module = importlib.import_module(f"bin.tiles.{name}")

                
                # check for structure
                if name not in module.__dict__:
                    self.log(logType.ERROR, f"File {tile} doesn't provide the main class of the block and was expected to do so. Class should be named {name}")
                    continue
                
                # this should be below previous one because it has event checked if that even exist yet
                mainClassData = module.__dict__[name]
                mainClassDict = mainClassData.__dict__
                
                
                # checking for components in the main class
                if "ID" not in mainClassDict:
                    self.log(logType.ERROR, f"A class of block with the name {name} doesn't have ID!")
                    continue
                
                if type(mainClassData.ID) != str:
                    self.log(logType.ERROR, f"A class of block with the name {name} doesn't have proper ID (that should be string)!")
                    continue
                
                if mainClassData.ID != name:
                    self.log(logType.ERROR, f"A class of entity with the name {name} doesn't have proper ID (it's doesnt match name (it's {mainClassData.ID} but that should {name}))!")
                    continue    
            
                if "IDInt" not in mainClassDict:
                    self.log(logType.ERROR, f"A class of block with the name {name} doesn't have IDInt!")
                    continue
                    
                if type(mainClassData.IDInt) != int:
                    self.log(logType.ERROR, f"A class of block with the name {name} doesn't have proper IDInt (that should be int)!")
                    continue
                
                if "MAINTEXTURE" not in mainClassDict:
                    self.log(logType.ERROR, f"A class of block with the name {name} doesn't have MAINTEXTURE!")
                    continue
                
                
                if type(mainClassData.MAINTEXTURE) != str:
                    self.log(logType.ERROR, f"A class of block with the name {name} doesn't have proper MAINTEXTURE (that should be string)!")
                    continue
                
                if "MAINTEXTUREISTRANSPARENT" not in mainClassDict:
                    self.log(logType.ERROR, f"A class of block with the name {name} doesn't have MAINTEXTUREISTRANSPARENT!")
                    continue
                
                if type(mainClassData.MAINTEXTUREISTRANSPARENT) != bool:
                    self.log(logType.ERROR, f"A class of block with the name {name} doesn't have proper MAINTEXTUREISTRANSPARENT (that should be bool)!")
                    continue
                
                _mainTextureLoc = os.path.join("resources", mainClassData.MAINTEXTURE).replace("/","\\")
                if not os.path.exists(_mainTextureLoc):
                    self.log(logType.ERROR, f"Path {_mainTextureLoc} provided in MAINTEXTURE does not exist. We could not load the main texture of the block of id {name}! we will load default texture instead! (make sure that path provided here is right!)")
                    
                    main_texture = pygame.image.load(os.path.join("resources", "tiles", "default.png"))
                else:
                    main_texture = pygame.image.load(_mainTextureLoc)
                
                if name in GAME_NAMESPACE["blocks"] or name in GAME_NAMESPACE["id_type"]:
                    self.log(logType.ERROR, f"The name {name} is ambiguous! That ID was already used somewhere else!")
                    continue
                 
                if mainClassData.IDInt in GAME_NAMESPACE["IDInts"].keys():
                    self.log(logType.ERROR, f"Int ID of {name} is already claimed (trying to possess ID of {mainClassData.IDInt}!\nThis is claimed by the block of id {GAME_NAMESPACE['IDInts'][mainClassData.IDInt]} !")
                    continue
                
                
                # claiming this id for this block
                GAME_NAMESPACE["IDInts"][module.__dict__[name].IDInt] = name
                
                
                # loading texture of the block
                if mainClassData.MAINTEXTUREISTRANSPARENT:
                    mainClassData.mainImageCompiled = self.__resources[mainClassData.MAINTEXTURE] = main_texture.convert_alpha()
                else:
                    mainClassData.mainImageCompiled = self.__resources[mainClassData.MAINTEXTURE] = main_texture.convert()
                    
                
                # creating namespace for the block
                GAME_NAMESPACE["blocks"][name] = {
                    "module": module,
                    "id": name,
                    "type": "block",
                    "class": mainClassData,
                    "idInt": mainClassData.IDInt,
                    "MAINTEXTURE_loc": mainClassData.MAINTEXTURE,
                    "MAINTEXTURE_loc_with": _mainTextureLoc,
                    "ISMAINTEXTURETRANSPARENT": mainClassData.MAINTEXTUREISTRANSPARENT,
                    "MAINTEXTURE_object": self.__resources[mainClassData.MAINTEXTURE],
                    "MAINTEXTURE_get": lambda: self.getTexture(mainClassData.MAINTEXTURE)
                }
                
                GAME_NAMESPACE["id_type"][name] = "block"
                
                self.log(logType.SUCCESS, f"new block added: {name} (INT ID: {mainClassData.IDInt})")
                loadedBlocks+=1
                # print(f"[NAMESPACE] New block added: {name} (INT ID: {module.__dict__[name].IDInt})")
            except ModuleNotFoundError as e:
                self.errorWithTraceback(f"error with importing block {name}, couldn't find module, even though module was expected. Check your integrity of game files via launcher! An error provided by the game:",e)
                self.log(logType.CRASHREPORT, f"Unable to import module \'bin.tiles.{name}\'! Module not found. Check your files integrity. That error shouldn't have occur under any circumstances!")
                exit()
            except Exception as e:
                # self.log(logType.ERROR, f"unable to block of id {name}\nERROR:\n {e}\n")
                self.errorWithTraceback(f"Unexpected error occured during trying to load block of id '{name}', more details about detail is depicted below:", e)
                # print(f"[NAMESPACE] unable to load tile of id {name}\nERROR:\n {e}\n")
                totalBlocks += 1
                
        self.log(logType.SUCCESS, f"loading blocks has ended! LOADED BLOCKS: {loadedBlocks}/{totalBlocks} (failed: {totalBlocks - loadedBlocks})")
        
        
        
        # entities
        self.log(logType.INIT, "loading entities...")
        
        loadedEntities: int = 0
        totalEntities: int = 0

        entities_modules_name: list[str] = os.listdir(loc_entities)
        
        for entity in entities_modules_name:
            name: str = "".join(entity.split(".")[:-1])
            if name == "__pycache__" or name == "" or name.startswith("_"): continue
            try:
                totalEntities += 1
                
                module = importlib.import_module(f"bin.entities.{name}")

                
                # check for structure
                if name not in module.__dict__:
                    self.log(logType.ERROR, f"File {entity} doesn't provide the main class of the entity and was expected to do so. Class should be named {name}")
                    continue
                
                # this should be below previous one because it has event checked if that even exist yet
                mainClassData = module.__dict__[name]
                mainClassDict = mainClassData.__dict__
                
                # checking for components in the main class
                if "ID" not in mainClassDict:
                    self.log(logType.ERROR, f"A class of entity with the name {name} doesn't have ID!")
                    continue
                
                if type(mainClassData.ID) != str:
                    self.log(logType.ERROR, f"A class of entity with the name {name} doesn't have proper ID (that should be string)!")
                    continue
                               
                if mainClassData.ID != name:
                    self.log(logType.ERROR, f"A class of entity with the name {name} doesn't have proper ID (it's doesnt match name (it's {mainClassData.ID} but that should {name}))!")
                    continue
                
                if "MAINTEXTURE" not in mainClassDict:
                    self.log(logType.ERROR, f"A class of entity with the name {name} doesn't have MAINTEXTURE!")
                    continue
                
                
                if type(mainClassData.MAINTEXTURE) != str:
                    self.log(logType.ERROR, f"A class of entity with the name {name} doesn't have proper MAINTEXTURE (that should be string)!")
                    continue
                
                if "MAINTEXTUREISTRANSPARENT" not in mainClassDict:
                    self.log(logType.ERROR, f"A class of entity with the name {name} doesn't have MAINTEXTUREISTRANSPARENT!")
                    continue
                
                if type(mainClassData.MAINTEXTUREISTRANSPARENT) != bool:
                    self.log(logType.ERROR, f"A class of entity with the name {name} doesn't have proper MAINTEXTUREISTRANSPARENT (that should be bool)!")
                    continue
                
                _mainTextureLoc = os.path.join("resources", mainClassData.MAINTEXTURE).replace("/","\\")
                if not os.path.exists(_mainTextureLoc):
                    # _r2 = "resources/" + module.__dict__[name].MAINTEXTURE
                    self.log(logType.ERROR, f"Path {_mainTextureLoc} provided in MAINTEXTURE does not exist. We could not load the main texture of the entity of id {name}! we will load default tile texture instead! (make sure that path provided here is right!)")
                    
                    main_texture = pygame.image.load(os.path.join("resources", "tiles", "default.png"))
                else:
                    main_texture = pygame.image.load(_mainTextureLoc)
                
                if name in GAME_NAMESPACE["entities"] or name in GAME_NAMESPACE["id_type"]:
                    self.log(logType.ERROR, f"The name {name} is ambiguous! That ID was already used somewhere else!")
                    continue
                
                # loading texture of the entity
                if mainClassData.MAINTEXTUREISTRANSPARENT:
                    mainClassData.MAINTEXTURE_RENDER = self.__resources[mainClassData.MAINTEXTURE] = main_texture.convert_alpha()
                else:
                    mainClassData.MAINTEXTURE_RENDER = self.__resources[mainClassData.MAINTEXTURE] = main_texture.convert()
                    
                
                    # pygame.transform.b
                # creating namespace for the block
                GAME_NAMESPACE["entity"][name] = {
                    "module": module,
                    "id": name,
                    "type": "entity",
                    "class": mainClassData,
                    "MAINTEXTURE_loc": mainClassData.MAINTEXTURE,
                    "MAINTEXTURE_loc_with": _mainTextureLoc,
                    "ISMAINTEXTURETRANSPARENT": mainClassData.MAINTEXTUREISTRANSPARENT,
                    "MAINTEXTURE_RENDER": self.__resources[mainClassData.MAINTEXTURE],
                    "MAINTEXTURE_object": self.__resources[mainClassData.MAINTEXTURE],
                    "MAINTEXTURE_get": lambda: self.getTexture(mainClassData.MAINTEXTURE)
                }
                
                GAME_NAMESPACE["id_type"][name] = "entity"
                
                self.log(logType.SUCCESS, f"new entity added: {name}")
                loadedEntities+=1
                # print(f"[NAMESPACE] New block added: {name} (INT ID: {module.__dict__[name].IDInt})")
            except ModuleNotFoundError as e:
                self.errorWithTraceback(f"error with importing entity {name}, couldn't find module, even though module was expected. Check your integrity of game files via launcher! An error provided by the game:",e)
                self.log(logType.CRASHREPORT, f"Unable to import module \'bin.tiles.{name}\'! Module not found. Check your files integrity. That error shouldn't have occur under any circumstances!")
                exit()
            except Exception as e:
                # self.log(logType.ERROR, f"unable to block of id {name}\nERROR:\n {e}\n")
                self.errorWithTraceback(f"Unexpected error occured during trying to load entity of id '{name}', more details about detail is depicted below:", e)
                # print(f"[NAMESPACE] unable to load tile of id {name}\nERROR:\n {e}\n")
                totalEntities += 1
                
        self.log(logType.SUCCESS, f"loading entities has ended! LOADED entities: {loadedEntities}/{totalEntities} (failed: {totalEntities - loadedEntities})")        
        
        endTime = time.time()
        
        
        self.log(logType.INFO, f"Loading the namespace has taken: {round(endTime-startTime,2)} seconds")
        self.log(logType.SUCCESS, "namespace has been loaded successfully...")
           
    def getGame(self) -> 'Game':
        return self.__game         
                    
    def getNameSpace(self) -> dict:
        return GAME_NAMESPACE
    
    def __init__(self, game: 'Game') -> None:
        super().__init__(logParent=ParentForLogs(name="resourceManager", parent=game.getLogParent()))
        self.__game = game
        self.log(logType.INIT, "intializing resource Manager...")
        self.__resources = {}
        self.__resources['GAME_NAMESPACE'] = GAME_NAMESPACE
        self.loadFromNameSpace()


GAME_NAMESPACE = {
    "environment": {
        "bin_loc": "unknown",
        "version": "unkown",
        "versionInt": -0,
    },
    "IDInts": {},
    "blocksFastLighting": {
        "blockStringName": {
            1: pygame.surface.Surface
        }
    },
    "id_type": {
        
    },
    "blocks": {
    },
    "entities": {
        
    }
}
