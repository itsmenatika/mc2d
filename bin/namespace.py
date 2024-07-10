import pygame
from typing import Any
import importlib
import os

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
class resourceManager:
    def getTexture(self, name: str, disableTryingToGet: bool = False):
        if name in self.__resources:
            return self.__resources[name]
        
        if not disableTryingToGet:
            return self.loadTextureFromFile(name)
            
    def loadTextureFromFile(self, name: str):
        self.__resources[name] = pygame.image.load(name).convert_alpha()
        return self.__resources[name]
    
    def get(self, name: str):
        if name in self.__resources:
            return self.__resources[name]
        
    def getBlockInformation(self, name: str):
        return self.__resources['GAME_NAMESPACE']['blocks'][name]
    
    def loadFromNameSpace(self) -> None:
        print("reloading namespace...")
        self.__resources['intIds'] = {}
        loc = os.path.dirname(os.path.abspath(__file__))
        
        loc_tiles = os.path.join(loc, "tiles")
        
        GAME_NAMESPACE['types'] = {
            "air": "block",
            "none_item": "item"
        }
        
        print("[NAMESPACE] Loading tiles...")
        
        print(os.listdir(loc_tiles))
        for tile in os.listdir(loc_tiles):
            name = "".join(tile.split(".")[:-1])
            if name == "__pycache__" or name == "": continue
            try:
                module = importlib.import_module(f"bin.tiles.{name}")
                if name not in module.__dict__:
                    raise Exception("no main class with the same name as the file")
                
                if "IDInt" not in module.__dict__[name].__dict__:
                    raise Exception("main class doesnt have IDInt")
                
                if "MAINTEXTURE" not in module.__dict__[name].__dict__:
                    raise Exception("main class doesnt have MAINTEXTURE")
                
                GAME_NAMESPACE["blocks"][name] = {
                    "module": module,
                    "id": name,
                    "type": "block",
                    "class": module.__dict__[name],
                    "idInt": module.__dict__[name].IDInt,
                    "MAINTEXTURE": module.__dict__[name].MAINTEXTURE
                }
                
                self.__resources[module.__dict__[name].MAINTEXTURE] = pygame.image.load(module.__dict__[name].MAINTEXTURE).convert_alpha()
                
            except Exception as e:
                print(f"[NAMESPACE] unable to load tile of id {name}\nERROR:\n {e}\n")
        
       
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
                    
                    
    
    def __init__(self, game: 'Game') -> None:
        self.__game = game
        self.__resources = {}
        self.__resources['GAME_NAMESPACE'] = GAME_NAMESPACE
        self.loadFromNameSpace()


GAME_NAMESPACE = {
    "environment": {
        "bin_loc": "unknown",
        "version": "pre-indev",
        "versionInt": 10,
    },
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
