import pygame
from pygame.math import Vector2
from bin.map import Chunk, Scene, Block


class Camera:
    def getGame(self) -> 'Game':
        return self.__game
    def draw(self, surface: pygame.surface.Surface):
        sceneToDraw: Scene = self.__game.getCurrentScene()
        
        screensize = pygame.display.get_surface().get_size()
        cameraEndPoint = (screensize[0] + self.cords.x,
                    screensize[1] + self.cords.y)
        
        chunk: Chunk = None
        sprite: Block = None
        for chunk in sceneToDraw.getActiveChunks().values():
            for sprite in chunk.sprites():
                if not sprite.doRender: continue
                # spritecords = sprite.getCordsRelative() - self.cords + chunk.getStartingPoint()
                cords = sprite.getCords()
                
                if cords.x > self.cords.x - Block.SIZE.x and cords.x < cameraEndPoint[0] + Block.SIZE.x and cords.y + Block.SIZE.y > self.cords.y and cords.y < cameraEndPoint[1] + Block.SIZE.y:
                    surface.blit(sprite.image,
                                cords - self.cords)
        
        
    def __init__(self, cords: Vector2, game: 'Game') -> None:
        self.cords: Vector2 = cords
        self.__game: 'Game' = game