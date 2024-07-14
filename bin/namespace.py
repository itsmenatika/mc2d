import pygame
from typing import Any
import importlib
import os
from bin.logger import Loggable, logType, ParentForLogs

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
    def getTexture(self, name: str, disableTryingToGet: bool = False):
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

                module_data = module.__dict__[name]
                module_dict_data = module_data.__dict__
                
                # check for structure
                if name not in module.__dict__:
                    self.log(logType.ERROR, "File {tile} doesn't provide the main class of the block and was expected to do so. Class should be named {name}")
                    continue
                
                # checking for components in the main class
                if "ID" not in module_dict_data:
                    self.log(logType.ERROR, "A class of block with the name {name} doesn't have ID!")
                    continue
                
                if type(module_data.ID) != str:
                    self.log(logType.ERROR, "A class of block with the name {name} doesn't have proper ID (that should be string)!")
                    continue
                
                if "IDInt" not in module_dict_data:
                    self.log(logType.ERROR, "A class of block with the name {name} doesn't have IDInt!")
                    continue
                    
                if type(module_data.IDInt) != int:
                    self.log(logType.ERROR, "A class of block with the name {name} doesn't have proper IDInt (that should be int)!")
                    continue
                
                if "MAINTEXTURE" not in module_dict_data:
                    self.log(logType.ERROR, "A class of block with the name {name} doesn't have MAINTEXTURE!")
                    continue
                
                
                if type(module_data.MAINTEXTURE) != str:
                    self.log(logType.ERROR, "A class of block with the name {name} doesn't have proper MAINTEXTURE (that should be string)!")
                    continue
                
                if "MAINTEXTUREISTRANSPARENT" not in module_dict_data:
                    self.log(logType.ERROR, "A class of block with the name {name} doesn't have MAINTEXTUREISTRANSPARENT!")
                    continue
                
                if type(module_data.MAINTEXTUREISTRANSPARENT) != bool:
                    self.log(logType.ERROR, "A class of block with the name {name} doesn't have proper MAINTEXTUREISTRANSPARENT (that should be bool)!")
                    continue
                
                _mainTextureLoc = os.path.join("resources", module_data.MAINTEXTURE).replace("/","\\")
                if not os.path.exists(_mainTextureLoc):
                    # _r2 = "resources/" + module.__dict__[name].MAINTEXTURE
                    self.log(logType.ERROR, f"Path {_mainTextureLoc} provided in MAINTEXTURE do not exist. We could not load block of id {name}!")
                    continue
                
                if name in GAME_NAMESPACE["blocks"]:
                    self.log(logType.ERROR, "The name {name} is ambiguous! That ID was already used somewhere else!")
                    continue
                 
                # print(GAME_NAMESPACE["IDInts"])
                if module_data.IDInt in GAME_NAMESPACE["IDInts"].keys():
                    self.log(logType.ERROR, "Int ID of {name} is already claimed (trying to possess ID of {module_data.IDInt}!\nThis is claimed by the block of id {GAME_NAMESPACE['IDInts'][module_data.IDInt]} !")
                    continue
                    # raise Exception(f"Int ID of {name} is already claimed (trying to possess ID of {module.__dict__[name].IDInt}!\nThis is claimed by block of id {GAME_NAMESPACE['IDInts'][module.__dict__[name].IDInt]} !")
                
                
                GAME_NAMESPACE["IDInts"][module.__dict__[name].IDInt] = name

                main_texture = pygame.image.load(_mainTextureLoc)

                self.__resources[module_data.MAINTEXTURE] = main_texture.convert()

                if module_data.MAINTEXTUREISTRANSPARENT:
                    self.__resources[module_data.MAINTEXTURE] = main_texture.convert_alpha()
                
                GAME_NAMESPACE["blocks"][name] = {
                    "module": module,
                    "id": name,
                    "type": "block",
                    "class": module_data,
                    "idInt": module_data.IDInt,
                    "MAINTEXTURE_loc": module_data.MAINTEXTURE,
                    "MAINTEXTURE_loc_with": _mainTextureLoc,
                    "ISMAINTEXTURETRANSPARENT": module_data.MAINTEXTUREISTRANSPARENT,
                    "MAINTEXTURE_object": self.__resources[module_data.MAINTEXTURE],
                    "MAINTEXTURE_get": lambda: self.getTexture(module_data.MAINTEXTURE)
                }
                
                self.log(logType.SUCCESS, f"new block added: {name} (INT ID: {module_data.IDInt})")
                loadedBlocks+=1
                # print(f"[NAMESPACE] New block added: {name} (INT ID: {module.__dict__[name].IDInt})")
            except ModuleNotFoundError:
                self.log(logType.CRASHREPORT, "Unable to import module \'bin.tiles{name}\'! Module not found.")
            except Exception as e:
                # self.log(logType.ERROR, f"unable to block of id {name}\nERROR:\n {e}\n")
                self.errorWithTraceback(f"unable to block of id {name}", e)
                # print(f"[NAMESPACE] unable to load tile of id {name}\nERROR:\n {e}\n")
                totalBlocks += 1
                
        self.log(logType.SUCCESS, f"loading blocks has ended! LOADED BLOCKS: {loadedBlocks}/{totalBlocks} (failed: {totalBlocks - loadedBlocks})")
        self.log(logType.SUCCESS, "namespace has been loaded successfully...")

        
       
        # for type, whatwevegothere in GAME_NAMESPACE.items():
        #     match type:
        #         case 'blocks':
        #             for blockName, block in whatwevegothere.items(): 
        #                 try:
                            
                            
        #                     self.__resources['intIds'][block['intID']] = blockName
                            
                        
                            
        #                     # main Texture
        #                     if 'MAINTEXTURE' in block['class'].__dict__:
        #                         self.__resources[block['class'].MAINTEXTURE] = pygame.image.load(block['class'].MAINTEXTURE).convert_alpha()
                        
        #                     else:
        #                         self.__resources[blockName+".png"] = pygame.image.load(blockName+".png").convert_alpha()
        #                 except Exception as e:
        #                     raise e
           
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
