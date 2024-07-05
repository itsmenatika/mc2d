import pygame
from pygame.math import Vector2
from bin.map import Chunk, Scene, Block
import math


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
        
        # chunks edges
        # Chunk.getStartingPoint()
        # print(sceneToDraw.getActiveChunks().values())
        # print([chunk.getEndingPoint() for chunk in sceneToDraw.getActiveChunks().values()])
        # chunkEdges = set([chunk.getStartingPoint() for chunk in sceneToDraw.getActiveChunks().values()].extend(
        #                 [chunk.getEndingPoint() for chunk in sceneToDraw.getActiveChunks().values()]))
        
        chunkEdges =  [chunk.getStartingPoint().x for chunk in sceneToDraw.getActiveChunks().values()]
        # chunkEdges.extend(
        #     [chunk.getEndingPoint().x for chunk in sceneToDraw.getActiveChunks().values()]
        # )
        chunkEdgesSet = set(chunkEdges)
        
        for edge in chunkEdgesSet:
            pygame.draw.line(surface, (230,0,20), (edge-self.cords.x, 0-self.cords.y), (edge-self.cords.x, (Chunk.SIZE.y*Block.SIZE.y)-self.cords.y), 2)

        
        BlockPos = Vector2(pygame.mouse.get_pos())
        
        BlockPos.x = int(( (BlockPos.x + self.cords.x) / Block.SIZE.x ) % Chunk.SIZE.x)
        BlockPos.y = int(( (BlockPos.y + self.cords.y) / Block.SIZE.y ) % Chunk.SIZE.y)
        
        font = pygame.font.SysFont('Comic Sans MS', 20)
        tak = font.render(f"{BlockPos}", False, (100,100,100))
        
        surface.blit(tak, (0,0))
        
        
    def __init__(self, cords: Vector2, game: 'Game') -> None:
        self.cords: Vector2 = cords
        self.__game: 'Game' = game