import pygame
import asyncio

from bin.map import Scene, Chunk
from bin.camera import Camera

from pygame.math import Vector2
from bin.namespace import resourceManager
from bin.worldgenerator import worldGeneratorNormal

class gameEngineError(Exception): pass

class Game:
    '''That get your just display that is used to display game'''
    def getDisplayOrginal(self) -> pygame.surface.Surface:
        return self.__display
    
    '''Get events from pygame'''
    def getEvents(self) -> list[pygame.event.Event]:
        return self.__events
    
    async def __drawLoop(self) -> None:
        # self.__currentScene.draw()
        self.__display.fill((0,0,0))
        self.camera.draw(self.getDisplayOrginal())
        pygame.display.update()
        
    async def __eventHandler(self) -> None:
        self.__events = pygame.event.get()
        for event in self.__events:
            if event.type == pygame.QUIT:
                self.__isGameOn = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.camera.cords.x -= 100
                elif event.key == pygame.K_RIGHT:
                    self.camera.cords.x += 100
                elif event.key == pygame.K_UP:
                    self.camera.cords.y -= 100
                elif event.key == pygame.K_DOWN:
                    self.camera.cords.y += 100
                    
            
    async def __onRun(self) -> None:
        t = Scene(self, name="test", worldGenerator=worldGeneratorNormal)
        self.setCurrentScene(t)
    
    async def __gameLoop(self) -> None:
        await self.__onRun()
        def executeScene(scene: Scene) -> Scene:
            if not scene.idle:
                scene.tick()
            return scene
            
        
        while self.__isGameOn:
            await self.__eventHandler()
            
            for scene in self.__scenes.values():
                if not scene.idle: await scene.tick()
            
            await self.__drawLoop()
            await self.__functionToGetAnotherMoreSpace()
            self.clock.tick()
            # print(self.clock.get_fps())
            
            
            
        
    
    async def __functionToGetAnotherMoreSpace(self) -> None:
        pass
    
    
    
    def addScene(self, scene: Scene, name: str = "scene") -> None:
        if name not in self.__scenes:
            self.__scenes[name] = scene
        else:
            raise gameEngineError(f"scene of name ${name} already do exist!")
        
    def removeScene(self, name: str) -> None:
        if name in self.__scenes:
            if self.__currentScene == self.__scenes[name]:
                self.__currentScene = None
            del self.__scenes[name]
        else:
            raise gameEngineError(f"scene of name ${name} doesnt exist!")
        
    def findNameOfScene(self, scene: Scene) -> str | None:
        for name, sceneT in self.__scenes:
            if scene == sceneT:
                return name
        return None
    
    
    def isSceneAdded(self, scene: Scene) -> bool:
        return True if scene in self.__scenes.values() else False
    
    def getScene(self, name: str) -> None | Scene:
        return self.__scenes.get(name, default=None)
    
            
        
            
    
    def setCurrentScene(self, scene: Scene) -> None:
        self.__currentScene = scene
        
    def getCurrentScene(self) -> Scene:
        return self.__currentScene
        
    def getResourceManager(self) -> resourceManager:
        return self.__resourceManager

    
    def __init__(self, resolution: tuple[int,int]) -> None:
        # save data
        self.__resolution = resolution
        self.__isGameOn: bool = True
        self.__scenes: dict[str,Scene] = {}
        self.__currentScene: None | Scene = None
        
        
        self.camera = Camera(cords=Vector2(0,0), game=self)
        
        
        
        # pygame issues
        pygame.init()
        pygame.font.init()
        self.__display = pygame.display.set_mode(self.__resolution)
        pygame.display.set_caption("Kantraft")
        self.clock = pygame.time.Clock()
        
   
        self.__resourceManager = resourceManager(self)
        
        # asyncio
        # self.__eventLoop = asyncio.new_event_loop()
        # asyncio.set_event_loop(self.__eventLoop)
        # asyncio.create_task(self.__gameLoop(), name="gameLoop")
        asyncio.run(self.__gameLoop())
        
        
        