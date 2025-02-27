import pygame
from pygame.math import Vector2
from bin.map import Chunk, Scene, Block
import math
import asyncio
import time

from bin.tools import timeTrackerPrintAsync,timeTrackerPrint

class Camera:

    # Metoda prywatna do uzyskania dostępnych sprite'ów do renderowania
    def __get_available_sprites_to_render(self, camera_end_points: tuple[int, int], spriteGroup: pygame.sprite.Group) -> list:
        # Lista do przechowania dostępnych sprite'ów 
        available_sprites = []

        # Pierwszy końcowy punkt kamery
        ft_cam_endpoint = camera_end_points[0]
        # Ostatni końcowy punkt kamery
        lt_cam_endpoint = camera_end_points[1]

        # Rozmiar horyzontalny bloku
        block_sz_x = Block.SIZE.x
        # Rozmiar wertykalny bloku
        block_sz_y = Block.SIZE.y

        # Podfunkcja, która przefiltruje sprite'y do renderowania według ustawionych kryteriów
        def filter_sprite(sprite) -> bool:
            # Tupla pozycji sprite'a
            sprite_xy = sprite.getCords()

            # Kordynat na osi Y
            cord_y = self.cords.y
            # Kordynat na osi X
            cord_x = self.cords.x

            # Zwróć informacje czy spełnia sprite poniższe warunki
            return sprite_xy[0] > (cord_x - block_sz_x) and sprite_xy[0] < (ft_cam_endpoint + block_sz_x) \
                    and (sprite_xy[1] + block_sz_y) > cord_y and sprite_xy[1] < (lt_cam_endpoint + block_sz_y)

        # Przefiltrowane sprite'y
        filtered_sprites = filter(filter_sprite, spriteGroup)
        
        # Przypisz skonwertowane na listę przefiltrowane sprite'y do listy dostępnych sprite'ów
        available_sprites = list(filtered_sprites)
     

        # Zwróć dostępnę sprite'y do renderu
        return available_sprites
        

    def __filterSpritesToDrawNonAsync(self) -> None:
        cameraEndPoint = (self.SCREENSIZE[0] + self.cords.x, self.SCREENSIZE[1] + self.cords.y)
        
        # self.spritesTodraw = self.__get_available_sprites_to_render(cameraEndPoint, spriteGroup=spriteGroup)
        
        self.mainBlocks = self.__get_available_sprites_to_render(camera_end_points=cameraEndPoint, spriteGroup=self.sceneToDraw.mainBlocks)

        self.backgroundBlocks = self.__get_available_sprites_to_render(camera_end_points=cameraEndPoint, spriteGroup=self.sceneToDraw.backgroundBlocks)
        
    async def __filterSpritesToDraw(self):
        while True:
            cameraEndPoint = (self.SCREENSIZE[0] + self.cords.x, self.SCREENSIZE[1] + self.cords.y)
            
            self.mainBlocks = self.__get_available_sprites_to_render(camera_end_points=cameraEndPoint, spriteGroup=self.sceneToDraw.mainBlocks)
            await asyncio.sleep(0.05)
            self.backgroundBlocks = self.__get_available_sprites_to_render(camera_end_points=cameraEndPoint, spriteGroup=self.sceneToDraw.backgroundBlocks)
            await asyncio.sleep(0.05)
            
    async def __generateInfo(self):
        while True:

            
            BlockPos = Vector2(pygame.mouse.get_pos())

            chunkPos: int = int(BlockPos[0])
            AbsolutePos = BlockPos.copy()
            absoluteBlockPos = BlockPos.copy()
            
            BlockPos.x = int(( (BlockPos.x + self.cords.x) / Block.SIZE.x ) % Chunk.SIZE.x)
            BlockPos.y = int(( (BlockPos.y + self.cords.y) / Block.SIZE.y ) % Chunk.SIZE.y)
            
            chunkPos = int((chunkPos + self.cords.x) // Block.SIZE.x // Chunk.SIZE.x)
            # chunkPos.y = int((chunkPos.y + self.cords.y) // Block.SIZE.y // Chunk.SIZE.y)
            
            absoluteBlockPos.x = round((absoluteBlockPos.x + self.cords.x) // Block.SIZE.x * 100) / 100
            absoluteBlockPos.y = round((absoluteBlockPos.y + self.cords.y)// Block.SIZE.y * 100) / 100
            # absoluteBlockPos.x = round(AbsolutePos.x // Block.SIZE.x)

            scene_game_clock = self.sceneToDraw.getGame().clock
            
            blockID = "None (air??)"
            lightLevel = None
            try:
                current_scene = self.getGame().getCurrentScene()

                chunk: Chunk = current_scene.getChunk(chunkPos  )
                # print(chunk.__dict__.keys())
                # print(chunk._Chunk__blocks, BlockPos)
        
                block: Block = chunk.getBlockByTuple((BlockPos[0], BlockPos[1]))
                blockID = block.ID
                lightLevel = block.lightValue
            except Exception as e: pass
                # print(e)
            # blockID = blockID.getBlockByTuple((chunkPos[0], chunkPos[1]))
            
            rNum = self.getGame().getResourceManager().getAmountOfResources()

            temp_info = f"BlockPos: {BlockPos} AbsBlockPos: {absoluteBlockPos} Chunk: {chunkPos} cords: {AbsolutePos} | {round(scene_game_clock.get_fps())}FPS {scene_game_clock.get_rawtime()}MS | BlockID: {blockID} | lightLevel: {lightLevel} | rNum: {rNum}"
            
            self.__infoToDraw = self.__font.render(temp_info, False, (100, 100, 100))

            await asyncio.sleep(0.2)
    
    def getGame(self) -> 'Game':
        return self.__game
    
    def draw(self, surface: pygame.surface.Surface):
        # draw background blocks
        for sprite in self.backgroundBlocks:
            surface.blit(sprite.image, sprite.getCords() - self.cords)

        # draw main blocks
        for sprite in self.mainBlocks:
            surface.blit(sprite.image, sprite.getCords() - self.cords)
            
        # draw entities
        for entity in self.sceneToDraw.entityGroup.sprites():
            surface.blit(entity.image, entity.getCords() - self.cords)

        # get all chunks
        active_scene_chunks = self.sceneToDraw.getActiveChunks()
        
        # draw chunkEdges and information
        
        # get starting positions of all active chunks
        chunkEdges =  [chunk.getStartingPoint().x for chunk in active_scene_chunks.values()]
        chunkEdgesSet = set(chunkEdges)
        
        # draw line on every starting position
        for edge in chunkEdgesSet:
            pygame.draw.line(surface, (230, 0, 20), (edge - self.cords.x, 0 - self.cords.y), (edge - self.cords.x, (Chunk.SIZE.y * Block.SIZE.y) - self.cords.y), 1)

        # draw dev information
        surface.blit(self.__infoToDraw, (0,0))
        
        # get mouse position
        mousePos = pygame.mouse.get_pos()

        
        # draw selected frame
        self.pointedBlock.topleft = (
            (mousePos[0] + self.cords.x) // Block.SIZE.x * Block.SIZE.x - self.cords.x,
            (mousePos[1] + self.cords.y) // Block.SIZE.y * Block.SIZE.y - self.cords.y)

        pygame.draw.rect(surface, "red", self.pointedBlock, width=2)
        

        # draw information about selected block (that you would place)
        game = self.getGame()

        g_storage_selected_block = game.storage['selectedBlockName']
        g_selected_block_main_txt = game.getNameSpace()["blocks"][g_storage_selected_block]["MAINTEXTURE_object"]
        
        surface.blit(g_selected_block_main_txt, (10,50))
        surface.blit(self.__font.render(f"{g_storage_selected_block} ({game.storage['selectedBlock']})", False, (100, 100, 100)), (75,50))
        
        
    def moveTo(self, newCords: Vector2, callFilter: bool = True) -> None:
        '''moves camera to a new position and force refiltering sprites'''
        self.cords = newCords

        if callFilter: 
            self.__filterSpritesToDrawNonAsync()
        
    def moveBy(self, by: Vector2, callFilter: bool = True) -> Vector2:
        '''same as self.moveTo(), but using relativePosition to previous position (original position)'''
        self.cords += by

        if callFilter: 
            self.__filterSpritesToDrawNonAsync()

        return self.cords
        
    def __init__(self, cords: Vector2, game: 'Game') -> None:
        self.cords: Vector2 = cords

        self.__game: 'Game' = game
        self.__font = pygame.font.SysFont('Comic Sans MS', 20)
        self.__infoToDraw = pygame.surface.Surface((1, 1))

        self.SCREENSIZE = pygame.display.get_surface().get_size()

        self.mainBlocks = pygame.sprite.Group()
        self.backgroundBlocks = pygame.sprite.Group()
        self.sceneToDraw: Scene = self.__game.getCurrentScene()
        self.pointedBlock = pygame.rect.Rect((0, 0), (Block.SIZE.x, Block.SIZE.y))

        asyncio.create_task(self.__generateInfo(), name="camera_info")
        asyncio.create_task(self.__filterSpritesToDraw(), name="camera_spriteFilter")