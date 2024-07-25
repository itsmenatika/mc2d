import pygame
from typing import Any
import importlib
import os
from bin.logger import Loggable, logType, ParentForLogs
from bin.map import Block

# from bin.tiles.dirt import dirt
# from bin.tiles.stone import stone
# from bin.tiles.grassBlock import grassBlock
# from bin.tiles.grassBetween import grassBetween
# from bin.tiles.stoneBetween import stoneBetween
# from bin.tiles.coalOre import coalOre
# from bin.tiles.diamondOre import diamondOre
# from bin.tiles.ironOre import ironOre
# from bin.tiles.oak_wood import oakWood
# from bin.tiles.bedrock import bedrock

class unkownNameSpace(Exception): pass
class exceptionThatShouldntBeWrite(Exception): pass
class resourceManager(Loggable):
    shadow_layouts = []

    for alpha in range(255, 0, -17):
        shadow = pygame.surface.Surface((Block.SIZE.x, Block.SIZE.y), flags=pygame.SRCALPHA)

        shadow.fill((0, 0, 0, alpha))

        shadow_layouts.append(shadow)
        
    # no shadow
    __shadow = pygame.surface.Surface((Block.SIZE.x, Block.SIZE.y), flags=pygame.SRCALPHA)
    __shadow.fill((0, 0, 0, 0))
    shadow_layouts.append(__shadow)
    
    def getAmountOfResources(self) -> int:
        return len(self.__resources)
    
    def applyDarkToTexture(self, image: pygame.surface.Surface, lightValue: int) -> pygame.surface.Surface:
        image = image.copy()
        image.blit(self.shadow_layouts[lightValue], (0,0))
        return image
    
    def getTexture(self, name: str, disableTryingToGet: bool = False, **kwargs):
        if len(kwargs) == 0:
            if name in self.__resources:
                return self.__resources[name]
            
            if not disableTryingToGet:
                return self.loadTextureFromFile(name)
        else:
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
        
        GAME_NAMESPACE['types'] = {
            "air": "block",
            "none_item": "item"
        }
        
        GAME_NAMESPACE['environment']['bin_loc'] = loc
        
        self.log(logType.INIT, "loading tiles...")
        
        # print(os.listdir(loc_tiles))
        loadedBlocks = 0
        totalBlocks = 0
        errorBlocks = 0

        tile_modules_name = os.listdir(loc_tiles)
        
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
                
                
                # if isinstance(mainClassData, Block)
                
                # checking for components in the main class
                if "ID" not in mainClassDict:
                    self.log(logType.ERROR, f"A class of block with the name {name} doesn't have ID!")
                    continue
                
                if type(mainClassData.ID) != str:
                    self.log(logType.ERROR, f"A class of block with the name {name} doesn't have proper ID (that should be string)!")
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
                    # _r2 = "resources/" + module.__dict__[name].MAINTEXTURE
                    self.log(logType.ERROR, f"Path {_mainTextureLoc} provided in MAINTEXTURE do not exist. We could not load block of id {name}!")
                    continue
                
                if name in GAME_NAMESPACE["blocks"]:
                    self.log(logType.ERROR, f"The name {name} is ambiguous! That ID was already used somewhere else!")
                    continue
                 
                # print(GAME_NAMESPACE["IDInts"])
                if mainClassData.IDInt in GAME_NAMESPACE["IDInts"].keys():
                    self.log(logType.ERROR, f"Int ID of {name} is already claimed (trying to possess ID of {mainClassData.IDInt}!\nThis is claimed by the block of id {GAME_NAMESPACE['IDInts'][mainClassData.IDInt]} !")
                    continue
                    # raise Exception(f"Int ID of {name} is already claimed (trying to possess ID of {module.__dict__[name].IDInt}!\nThis is claimed by block of id {GAME_NAMESPACE['IDInts'][module.__dict__[name].IDInt]} !")
                
                
                # claiming this id for this block
                GAME_NAMESPACE["IDInts"][module.__dict__[name].IDInt] = name

                main_texture = pygame.image.load(_mainTextureLoc)
                
                # darkTexture = pygame.surface.Surface((64,64), flags=pygame.SRCALPHA)
                # darkTexture.fill((0,0,0,210))
                # main_texture.blit(darkTexture, (0,0))
                
                # main_texture.set_alpha(pygame.SRCALPHA)
                # pygame.draw.rect(main_texture, pygame.Color(0,0,0,a=230), (0,0,64,64))

                
                # loading texture of the block
                if mainClassData.MAINTEXTUREISTRANSPARENT:
                    mainClassData.mainImageCompiled = self.__resources[mainClassData.MAINTEXTURE] = main_texture.convert_alpha()
                else:
                    mainClassData.mainImageCompiled = self.__resources[mainClassData.MAINTEXTURE] = main_texture.convert()
                    
                
                    # pygame.transform.b
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
                
                self.log(logType.SUCCESS, f"new block added: {name} (INT ID: {mainClassData.IDInt})")
                loadedBlocks+=1
                # print(f"[NAMESPACE] New block added: {name} (INT ID: {module.__dict__[name].IDInt})")
            except ModuleNotFoundError as e:
                self.errorWithTraceback(f"error with importing block {name}, couldn't find module",e)
                self.log(logType.CRASHREPORT, f"Unable to import module \'bin.tiles.{name}\'! Module not found.")
                exit()
            except Exception as e:
                # self.log(logType.ERROR, f"unable to block of id {name}\nERROR:\n {e}\n")
                self.errorWithTraceback(f"unable to block of id {name}", e)
                # print(f"[NAMESPACE] unable to load tile of id {name}\nERROR:\n {e}\n")
                totalBlocks += 1
                
        self.log(logType.SUCCESS, f"loading blocks has ended! LOADED BLOCKS: {loadedBlocks}/{totalBlocks} (failed: {totalBlocks - loadedBlocks})")
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
        "version": "pre-indev",
        "versionInt": 10,
    },
    "IDInts": {},
    "types": {
        "air": "block",
        "none_item": "item"
    },
    "blocksFastLighting": {
        "blockStringName": {
            1: pygame.surface.Surface
        }
    },
    "blocks": {
            # "dirt": {
            #     "intID": 1,
            #     "class": dirt
            # },
            # "grass_block": {
            #     "intID": 2,
            #     "class": grassBlock
            # },
            # "stone": {
            #     "intID": 3,
            #     "class": stone
            # },
            # "grass_between": {
            #     "intID": 4,
            #     "class": grassBetween
            # },
            # "stone_between": {
            #     "intID": 5,
            #     "class": stoneBetween
            # },
            # "coal_ore": {
            #     "intID": 6,
            #     "class": coalOre
            # },
            # "oak_wood": {
            #     "intID": 7,
            #     "class": oakWood
            # },
            # "bedrock": {
            #     "intID": 8,
            #     "class": bedrock
            # },
            # "diamond_ore": {
            #     "intID": 9,
            #     "class": diamondOre
            # },
            # "iron_ore": {
            #     "intID": 10,
            #     "class": ironOre
            # }
    }
}
