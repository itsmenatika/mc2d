import pygame
from pygame.math import Vector2
from bin.map import Chunk, Scene, Block
import math
import asyncio


class Camera:
    async def __filterSpritesToDraw(self):
        while True:
            
            cameraEndPoint = (self.SCREENSIZE[0] + self.cords.x,
            self.SCREENSIZE[1] + self.cords.y)
            
            self.spritesTodraw = list(filter(lambda sprite: sprite.getCords().x > self.cords.x - Block.SIZE.x and sprite.getCords().x < cameraEndPoint[0] + Block.SIZE.x and sprite.getCords().y + Block.SIZE.y > self.cords.y and sprite.getCords().y < cameraEndPoint[1] + Block.SIZE.y, self.sceneToDraw.sprites()))
            await asyncio.sleep(0.1)
    async def __generateInfo(self):
        while True:

            
            BlockPos = Vector2(pygame.mouse.get_pos())
            chunkPos = BlockPos.copy()
            AbsolutePos = BlockPos.copy()
            
            BlockPos.x = int(( (BlockPos.x + self.cords.x) / Block.SIZE.x ) % Chunk.SIZE.x)
            BlockPos.y = int(( (BlockPos.y + self.cords.y) / Block.SIZE.y ) % Chunk.SIZE.y)
            
            chunkPos.x = int((chunkPos.x + self.cords.x) // Block.SIZE.x // Chunk.SIZE.x)
            chunkPos.y = int((chunkPos.y + self.cords.y) // Block.SIZE.y // Chunk.SIZE.y)
            
            AbsolutePos.x = round(AbsolutePos.x + self.cords.x * 100)/100
            AbsolutePos.y = round(AbsolutePos.y + self.cords.y * 100)/100
            
            blockID = "None (air??)"
            try:
                chunk: Chunk = self.getGame().getCurrentScene().getChunk((chunkPos[0], chunkPos[1]))
                # print(chunk.__dict__.keys())
                # print(chunk._Chunk__blocks, BlockPos)
                blockID = chunk.getBlockByTuple((BlockPos[0], BlockPos[1])).ID
            except Exception as e: pass
                # print(e)
            # blockID = blockID.getBlockByTuple((chunkPos[0], chunkPos[1]))
            
            self.__infoToDraw = self.__font.render(f"BlockPos: {BlockPos} Chunk: {chunkPos} {round(self.sceneToDraw.getGame().clock.get_fps())}FPS {self.sceneToDraw.getGame().clock.get_rawtime()}MS AbsPOS: {AbsolutePos} BlockID: {blockID}", False, (100,100,100))
            await asyncio.sleep(0.2)
    
    def getGame(self) -> 'Game':
        return self.__game
    def draw(self, surface: pygame.surface.Surface):
        # sceneToDraw: Scene = self.__game.getCurrentScene()
        
        # screensize = pygame.display.get_surface().get_size()
        
        # chunk: Chunk = None
        sprite: Block = None

        for sprite in self.spritesTodraw:
            surface.blit(sprite.image, sprite.getCords() - self.cords)
        # for sprite in sceneToDraw.sprites():
        #     cords = sprite.getCords()
            
        #     if cords.x > self.cords.x - Block.SIZE.x and cords.x < cameraEndPoint[0] + Block.SIZE.x and cords.y + Block.SIZE.y > self.cords.y and cords.y < cameraEndPoint[1] + Block.SIZE.y:
        #         surface.blit(sprite.image,
        #                     cords - self.cords)
            
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
        
        chunkEdges =  [chunk.getStartingPoint().x for chunk in self.sceneToDraw.getActiveChunks().values()]
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
        self.SCREENSIZE = pygame.display.get_surface().get_size()
        self.spritesTodraw = pygame.sprite.Group()
        self.sceneToDraw: Scene = self.__game.getCurrentScene()
        
        asyncio.create_task(self.__generateInfo(), name="camera_info")
        asyncio.create_task(self.__filterSpritesToDraw(), name="camera_spriteFilter")