import pygame
import asyncio
from typing import Optional, Iterable, ItemsView, Union

from bin.map import Scene, Chunk, currentScene, Block
from bin.camera import Camera

from pygame.math import Vector2
from bin.namespace import resourceManager
from bin.worldgenerator import worldGeneratorNormal
from bin.abstractClasses import InputType, inputEventInfo

class gameEngineError(Exception): pass
class invalidName(gameEngineError): pass


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
        pygame.display.flip()
        
    async def __eventHandler(self) -> None:
        self.__events = pygame.event.get()
        for event in self.__events:
            match event.type:
                case pygame.QUIT:
                    self.__isGameOn = False
                case pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        # self.camera.cords.x -= 200
                        self.camera.moveBy(Vector2(-200,0))
                    elif event.key == pygame.K_RIGHT:
                        # self.camera.cords.x += 200
                        self.camera.moveBy(Vector2(200,0))
                    elif event.key == pygame.K_UP:
                        # self.camera.cords.y -= 200
                        self.camera.moveBy(Vector2(0,-200))
                    elif event.key == pygame.K_DOWN:
                        # self.camera.cords.y += 200
                        self.camera.moveBy(Vector2(0,200))
                case pygame.MOUSEBUTTONDOWN:
                    # callable[['Game', currentScene, InputType,inputEventInfo], bool]
                    buttonsClicked: tuple[bool, bool, bool] = pygame.mouse.get_pressed()
                    mousePos = pygame.mouse.get_pos()
                    
                    # print(self.__inputEventsList)
                    if buttonsClicked[0]:
                        for eventName, event in self.__inputEventsList["leftClick"].items():
                            if event[1]['enabled']:
                                if event[0](self, self.getCurrentScene(), InputType.leftClick, {
                                    "buttonClicked": buttonsClicked,
                                    "mousePos": mousePos
                                }): break
                    elif buttonsClicked[2]:
                        for eventName, event in self.__inputEventsList["rightClick"].items():
                            if event[1]['enabled']:
                                if event[0](self, self.getCurrentScene(), InputType.leftClick, {
                                    "buttonClicked": buttonsClicked,
                                    "mousePos": mousePos
                                }): break
                
               
                    
            
    async def __onRun(self) -> None:
        t = Scene(self, name="test", worldGenerator=worldGeneratorNormal)
        self.setCurrentScene(t)
        self.camera = Camera(cords=Vector2(0,70), game=self)
        
        def destroyBlock(game, currentScene: Scene, typeEvent, info):
            blockLocation = Vector2((info['mousePos'][0] + self.camera.cords.x) // Block.SIZE.x,
                                    (info['mousePos'][1] + self.camera.cords.y) // Block.SIZE.y) 

            currentScene.setBlockByAbsolutePos(blockLocation, None, notRaiseErrors=True)
            
            
        def addBlock(game, currentScene: Scene, typeEvent, info):
            blockLocation = Vector2((info['mousePos'][0] + self.camera.cords.x) // Block.SIZE.x,
                                    (info['mousePos'][1] + self.camera.cords.y) // Block.SIZE.y) 


            currentScene.setBlockByAbsolutePos(blockLocation,"stone",notRaiseErrors=True)
        
        
        self.addInputEvent("test", InputType.leftClick, destroyBlock)
        self.addInputEvent("test2", InputType.rightClick, addBlock)
        
    
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
            
            await self.__functionToGetAnotherMoreSpace()
            await self.__drawLoop()
            self.clock.tick(120)
            # self.clock.get_rawtime()
            # print(self.clock.get_fps())
            
            
            
        
    
    async def __functionToGetAnotherMoreSpace(self) -> None:
        await asyncio.sleep(0.01)
    
    
    
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

    def getNameSpace(self) -> dict:
        return self.__resourceManager.getNameSpace()
    
    # ------
    # input events management
    # ------
    
    def doesInputEventNameDoExist(self, name: str, forcedType: Optional[InputType] = None) -> bool:
        '''Check if event name do exist of any type'''
        if forcedType != None and forcedType != str:
                forcedType = forcedType.value
                
        if name in self.__inputEventsList["rightClick"]:
            if forcedType is None: return True
            elif forcedType == "rightClick": return True
        if name in self.__inputEventsList["leftClick"]:
            if forcedType is None: return True
            elif forcedType == "leftClick": return True
            
        return False
        
    
    def addInputEvent(self, name: str, typeOfInputTypeEvent: Union[str, InputType], function: callable, key: Optional[int] = None, forcedSceneName: Optional[str] = None, dontRaiseAnyErrors: bool = False, setIfDoExist: bool = False, startAsEnabled: bool = True) -> None:            
        if typeOfInputTypeEvent != str:
                typeOfInputTypeEvent = typeOfInputTypeEvent.value
        # callable[['Game', currentScene, InputType,inputEventInfo], bool]
        # name Checking
        if self.doesInputEventNameDoExist(name):
            if not dontRaiseAnyErrors:
                raise invalidName(f"name '{name}' is already claimed as name for an event!")
            if not setIfDoExist: return
        
        self.__inputEventsList['events'][name] = [function, 
                                         {'key': key, 'enabled': startAsEnabled, 'forcedSceneName': forcedSceneName, 'type': typeOfInputTypeEvent, 'name': name}]
        self.__inputEventsList[typeOfInputTypeEvent][name] = [function, 
                                                     {'key': key, 'enabled': startAsEnabled, 'forcedSceneName': forcedSceneName, 'type': typeOfInputTypeEvent, 'name': str}]
            
            # if forcedSceneName is not None:
                
    def removeInputEvent(self, name: str, dontRaiseAnyErrors: bool = False) -> None:
        if not self.doesInputEventNameDoExist(name):
            if not dontRaiseAnyErrors:
                raise invalidName(f"didn't find event of name '{name}'")
            return
            
        del self.__inputEventsList[self.__inputEventsList['events'][name][1]['type']][name]
        del self.__inputEventsList['events'][name]
        
    
    def getInputEvents(self, ofType:Optional[Union[str, InputType]] = None) -> list[tuple[str,list[callable, dict]]]:            
        if ofType == None:
            return self.__events['events'].items()
        else:
            if ofType != None and ofType != str:
                ofType = ofType.value
            return self.__inputEventsList[ofType].items()
            
        
    def clearInputEvents(self, ofType: Optional[Union[str, InputType]] = None) -> None:
        if ofType != None and ofType != str:
            ofType = ofType.value
        
        if ofType == None:
                self.__inputEventsList = {
                # "forcedScenes": {
                    
                # },
                "events": {
                },
                "rightClick": {
                    
                },
                "leftClick": {
                    
                }
            }
        else:
            # creating copy just because python can create errors about changing size of dictionary during iteration
            # that's just to avoid feature errors
            eventNamesToDelete = [eventName for eventName in self.__inputEventsList[ofType].keys()]
            self.__inputEventsList[ofType] = {}
            for name in eventNamesToDelete:
                del self.__inputEventsList['events'][name]
                
        
        
        
    
    # def addRightClick(self, name: str, function: callable, DontRaiseAnyErrors: bool = False, ForceSetting: bool = False) -> None:
    #     if name in self.__events or name in self.__events[''])and not DontRaiseAnyErrors:
    #         raise gameEngineError(f"{name} is already taken")
        
    def __init__(self, resolution: tuple[int,int]) -> None:
        # save data
        self.__resolution = resolution
        self.__isGameOn: bool = True
        self.__scenes: dict[str,Scene] = {}
        self.__currentScene: None | Scene = None
        self.__inputEventsList = {
            # "forcedScenes": {
                
            # },
            "events": {
            },
            "rightClick": {
                
            },
            "leftClick": {
                
            }
        }
        
        
        
        
        
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
        
        
        