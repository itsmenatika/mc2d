import pygame
from pygame.math import Vector2
from bin.map import Chunk, Scene, Block
import math
import asyncio
import time

from bin.tools import timeTrackerPrintAsync,timeTrackerPrint

class Camera:

    # Metoda prywatna do uzyskania dostępnych sprite'ów do renderowania
    def __get_available_sprites_to_render(self, camera_end_points: tuple[int, int]) -> list:
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
        filtered_sprites = filter(filter_sprite, self.sceneToDraw.sprites())
        
        # Przypisz skonwertowane na listę przefiltrowane sprite'y do listy dostępnych sprite'ów
        available_sprites = list(filtered_sprites)
     

        # Zwróć dostępnę sprite'y do renderu
        return available_sprites
        
    def __filterSpritesToDrawNonAsync(self) -> None:
        cameraEndPoint = (self.SCREENSIZE[0] + self.cords.x, self.SCREENSIZE[1] + self.cords.y)
        
        self.spritesTodraw = self.__get_available_sprites_to_render(cameraEndPoint)
        
    async def __filterSpritesToDraw(self):
        while True:
            self.__filterSpritesToDrawNonAsync()

            await asyncio.sleep(0.1)
            
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
        
        active_scene_chunks = self.sceneToDraw.getActiveChunks()
        
        # draw chunkEdges and information
        chunkEdges =  [chunk.getStartingPoint().x for chunk in active_scene_chunks.values()]
        # chunkEdges.extend(
        #     [chunk.getEndingPoint().x for chunk in sceneToDraw.getActiveChunks().values()]
        # )
        chunkEdgesSet = set(chunkEdges)
        
        # Nie wiem jak to by nazwać
        temp = Chunk.SIZE.y * Block.SIZE.y

        for edge in chunkEdgesSet:
            pygame.draw.line(surface, (230, 0, 20), (edge - self.cords.x, 0 - self.cords.y), (edge - self.cords.x, temp - self.cords.y), 1)

        surface.blit(self.__infoToDraw, (0,0))
        
        mousePos = pygame.mouse.get_pos()

        pointed_block_zx = (mousePos[0] + self.cords.x) // Block.SIZE.x * Block.SIZE.x - self.cords.x
        pointed_block_zy = (mousePos[1] + self.cords.y) // Block.SIZE.y * Block.SIZE.y - self.cords.y
        
        # self.cords = Vector2(0,0)
        
        self.pointedBlock.topleft = (pointed_block_zx, pointed_block_zy)

        pygame.draw.rect(surface, "red", self.pointedBlock, width=2)


        game = self.getGame()

        g_storage_selected_block = game.storage['selectedBlockName']
        g_selected_block_main_txt = game.getNameSpace()["blocks"][g_storage_selected_block]["MAINTEXTURE_object"]
        
        surface.blit(g_selected_block_main_txt, (10,50))
        surface.blit(self.__font.render(f"{g_storage_selected_block} ({game.storage['selectedBlock']})", False, (100, 100, 100)), (75,50))
        
        
    # @property
    # def cords(self):
    #     return self.cords
        
    # @property.setter
    # def cords(self, setTo):
    #     self.__cords = setTo
    #     self.__filterSpritesToDrawNonAsync()
    
    def moveTo(self, newCords: Vector2, callFilter: bool = True) -> None:
        self.cords = newCords

        if callFilter: 
            self.__filterSpritesToDrawNonAsync()
        
    def moveBy(self, by: Vector2, callFilter: bool = True) -> Vector2:
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

        self.spritesTodraw = pygame.sprite.Group()
        self.sceneToDraw: Scene = self.__game.getCurrentScene()
        self.pointedBlock = pygame.rect.Rect((0, 0), (Block.SIZE.x, Block.SIZE.y))

        asyncio.create_task(self.__generateInfo(), name="camera_info")
        asyncio.create_task(self.__filterSpritesToDraw(), name="camera_spriteFilter")