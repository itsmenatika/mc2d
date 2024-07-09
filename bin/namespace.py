import pygame
from typing import Any

from bin.tiles.dirt import dirt
from bin.tiles.stone import stone
from bin.tiles.grassBlock import grassBlock
from bin.tiles.grassBetween import grassBetween
from bin.tiles.stoneBetween import stoneBetween
from bin.tiles.coalOre import coalOre
from bin.tiles.diamondOre import diamondOre
from bin.tiles.ironOre import ironOre
from bin.tiles.oak_wood import oakWood
from bin.tiles.bedrock import bedrock

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
        self.__resources['intIds'] = {}
        for type, whatwevegothere in GAME_NAMESPACE.items():
            match type:
                case 'blocks':
                    for blockName, block in whatwevegothere.items(): 
                        try:
                            
                            
                            self.__resources['intIds'][block['intID']] = blockName
                            
                        
                            
                            # main Texture
                            if 'MAINTEXTURE' in block['class'].__dict__:
                                self.__resources[block['class'].MAINTEXTURE] = pygame.image.load(block['class'].MAINTEXTURE).convert_alpha()
                        
                            else:
                                self.__resources[blockName+".png"] = pygame.image.load(blockName+".png").convert_alpha()
                        except Exception as e:
                            raise e
                    
                    
    
    def __init__(self, game: 'Game') -> None:
        self.__game = game
        self.__resources = {}
        self.__resources['GAME_NAMESPACE'] = GAME_NAMESPACE
        self.loadFromNameSpace()


GAME_NAMESPACE = {
    "blocks": {
            "dirt": {
                "intID": 1,
                "class": dirt
            },
            "grass_block": {
                "intID": 2,
                "class": grassBlock
            },
            "stone": {
                "intID": 3,
                "class": stone
            },
            "grass_between": {
                "intID": 4,
                "class": grassBetween
            },
            "stone_between": {
                "intID": 5,
                "class": stoneBetween
            },
            "coal_ore": {
                "intID": 6,
                "class": coalOre
            },
            "oak_wood": {
                "intID": 7,
                "class": oakWood
            },
            "bedrock": {
                "intID": 8,
                "class": bedrock
            },
            "diamond_ore": {
                "intID": 9,
                "class": diamondOre
            },
            "iron_ore": {
                "intID": 10,
                "class": ironOre
            }
    }
}
