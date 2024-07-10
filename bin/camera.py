import pygame
from pygame.math import Vector2
from bin.map import Chunk, Scene, Block
import math
import asyncio


class Camera:
    async def __generateInfo(self):
        while True:
            sceneToDraw: Scene = self.__game.getCurrentScene()
            
            BlockPos = Vector2(pygame.mouse.get_pos())
            
            BlockPos.x = int(( (BlockPos.x + self.cords.x) / Block.SIZE.x ) % Chunk.SIZE.x)
            BlockPos.y = int(( (BlockPos.y + self.cords.y) / Block.SIZE.y ) % Chunk.SIZE.y)
            
            chunkPos = Vector2(pygame.mouse.get_pos())
            
            chunkPos.x = int((chunkPos.x + self.cords.x) // Block.SIZE.x // Chunk.SIZE.x)
            chunkPos.y = int((chunkPos.y + self.cords.y) // Block.SIZE.y // Chunk.SIZE.y)
            
            self.__infoToDraw = self.__font.render(f"BlockPos: {BlockPos} CHUNK: {chunkPos} {round(sceneToDraw.getGame().clock.get_fps())}FPS {sceneToDraw.getGame().clock.get_rawtime()}MS", False, (100,100,100))
            await asyncio.sleep(0.2)
    
    def getGame(self) -> 'Game':
        return self.__game
    def draw(self, surface: pygame.surface.Surface):
        sceneToDraw: Scene = self.__game.getCurrentScene()
        
        screensize = pygame.display.get_surface().get_size()
        cameraEndPoint = (screensize[0] + self.cords.x,
                    screensize[1] + self.cords.y)
        
        chunk: Chunk = None
        sprite: Block = None
        for sprite in sceneToDraw.sprites():
            cords = sprite.getCords()
            
            if cords.x > self.cords.x - Block.SIZE.x and cords.x < cameraEndPoint[0] + Block.SIZE.x and cords.y + Block.SIZE.y > self.cords.y and cords.y < cameraEndPoint[1] + Block.SIZE.y:
                surface.blit(sprite.image,
                            cords - self.cords)
            
        # for chunk in sceneToDraw.getActiveChunks().values():
        #     for sprite in chunk.sprites():
        #         if not sprite.doRender: continue
        #         # spritecords = sprite.getCordsRelative() - self.cords + chunk.getStartingPoint()
        #         cords = sprite.getCords()
                
        #         if cords.x > self.cords.x - Block.SIZE.x and cords.x < cameraEndPoint[0] + Block.SIZE.x and cords.y + Block.SIZE.y > self.cords.y and cords.y < cameraEndPoint[1] + Block.SIZE.y:
        #             surface.blit(sprite.image,
        #                         cords - self.cords)
        
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


        
        surface.blit(self.__infoToDraw, (0,0))
        
        
    def __init__(self, cords: Vector2, game: 'Game') -> None:
        self.cords: Vector2 = cords
        self.__game: 'Game' = game
        self.__font = pygame.font.SysFont('Comic Sans MS', 20)
        self.__infoToDraw = pygame.surface.Surface((1,1))
        
        asyncio.create_task(self.__generateInfo(), name="camera_info")