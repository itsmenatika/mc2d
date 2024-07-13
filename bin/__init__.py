import pygame
import sys
import traceback
import asyncio
from typing import Optional, Iterable, ItemsView, Union

from bin.map import Scene, Chunk, currentScene, Block
from bin.camera import Camera

from pygame.math import Vector2
from bin.namespace import resourceManager
from bin.worldgenerator import worldGeneratorNormal
from bin.abstractClasses import InputType, inputEventInfo
from bin.logger import Logger, Loggable, logType, ParentForLogs

class gameEngineError(Exception): pass
class invalidName(gameEngineError): pass


class Game(Loggable):
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
                    self.getLogger().log(logtype=logType.ERROR, message="game is being forcefully closed...")
                    self.getLogger().log(logtype=logType.ERROR, message="game engine has been forcefully closed by user!", parent=None)
                    self.__isGameOn = False
                case pygame.KEYUP:
                    # print(self.__inputEventsList["keyUp"].items())
                    for eventName, eventTwo in self.__inputEventsList["keyUp"].items():
                        if eventTwo[1]['key'] == event.key:
                            try:
                                if eventTwo[0](self, self.getCurrentScene(), InputType.keyUp, {
                                    "buttonClicked": event.key,
                                }, Loggable(game=self,logParent=ParentForLogs(name=f"inputevent_{eventName}", parent=self.getLogParent()))): break
                            except Exception as e:
                                # self.getLogger().log(logType.ERROR, f"An error has occured during trying to execute a function given to the event with the name of '{eventName}' (eventData: {eventTwo[1]}):\n")
                                # traceback.print_exception(e)
                                # print("")
                                self.getLogger().errorWithTraceBack("An error has occured during trying to execute a function given to the event with the name of '{eventName}' (eventData: {eventTwo[1]})", e)
                case pygame.KEYDOWN:
                    for eventName, eventTwo in self.__inputEventsList["keyDown"].items():
                        # print(event.key, event['key'])
                        # print(event[1])
                        try:
                            if eventTwo[1]['key'] == event.key:
                                if eventTwo[0](self, self.getCurrentScene(), InputType.keyDown, {
                                    "buttonClicked": event.key,
                                }, Loggable(game=self,logParent=ParentForLogs(name=f"inputevent_{eventName}", parent=self.getLogParent()))): break
                        except Exception as e:
                            # type, value, traceback = sys.exc_info()
                            # traceback.print_exception(e)
                            # print(type,value,traceback)
                            # self.getLogger().log(logType.ERROR, f"An error has occured during trying to execute a function given to the event with the name of '{eventName}' (eventData: {eventTwo[1]}):\n")
                            # traceback.print_exception(e)
                            # print("")
                            self.getLogger().errorWithTraceback("An error has occured during trying to execute a function given to the event with the name of '{eventName}' (eventData: {eventTwo[1]})", e)
                    
                    # if event.key == pygame.K_LEFT:
                    #     # self.camera.cords.x -= 200
                    #     self.camera.moveBy(Vector2(-200,0))
                    # elif event.key == pygame.K_RIGHT:
                    #     # self.camera.cords.x += 200
                    #     self.camera.moveBy(Vector2(200,0))
                    # elif event.key == pygame.K_UP:
                    #     # self.camera.cords.y -= 200
                    #     self.camera.moveBy(Vector2(0,-200))
                    # elif event.key == pygame.K_DOWN:
                    #     # self.camera.cords.y += 200
                    #     self.camera.moveBy(Vector2(0,200))
                case pygame.MOUSEBUTTONDOWN:
                    # callable[['Game', currentScene, InputType,inputEventInfo], bool]
                    buttonsClicked: tuple[bool, bool, bool] = pygame.mouse.get_pressed()
                    mousePos = pygame.mouse.get_pos()
                    
                    # print(self.__inputEventsList)
                    if buttonsClicked[0]:
                        for eventName, eventTwo in self.__inputEventsList["leftClick"].items():
                            if eventTwo[1]['enabled']:
                                try:
                                    if eventTwo[0](self, self.getCurrentScene(), InputType.leftClick, {
                                        "buttonClicked": buttonsClicked,
                                        "mousePos": mousePos
                                    }, Loggable(game=self, logParent=ParentForLogs(name=f"inputevent_{eventName}", parent=self.getLogParent()))): break
                                except Exception as e:
                                    self.getLogger().errorWithTraceback("An error has occured during trying to execute a function given to the event with the name of '{eventName}' (eventData: {eventTwo[1]})", e)
                                    # traceback.print_exception(e)
                                    # print("")
                    elif buttonsClicked[2]:
                        for eventName, eventTwo in self.__inputEventsList["rightClick"].items():
                            if eventTwo[1]['enabled']:
                                try:
                                    if eventTwo[0](self, self.getCurrentScene(), InputType.leftClick, {
                                        "buttonClicked": buttonsClicked,
                                        "mousePos": mousePos
                                    }, Loggable(game=self, logParent=ParentForLogs(name=f"inputevent_{eventName}", parent=self.getLogParent()))): break
                                except Exception as e:
                                    # self.getLogger().log(logType.ERROR, f"An error has occured during trying to execute a function given to the event with the name of '{eventName}' (eventData: {eventTwo[1]}):\n")
                                    # traceback.print_exception(e)
                                    # print("")
                                    self.getLogger().errorWithTraceback("An error has occured during trying to execute a function given to the event with the name of '{eventName}' (eventData: {eventTwo[1]})", e)
                
               
                    
            
    async def __onRun(self) -> None:
        t = Scene(self, name="test", worldGenerator=worldGeneratorNormal)
        self.setCurrentScene(t)
        self.camera = Camera(cords=Vector2(0,70), game=self)
        
        
        # events
        def destroyBlock(game, currentScene: Scene, typeEvent, info, loggable):
            blockLocation = Vector2((info['mousePos'][0] + self.camera.cords.x) // Block.SIZE.x,
                                    (info['mousePos'][1] + self.camera.cords.y) // Block.SIZE.y) 

            currentScene.setBlockByAbsolutePos(blockLocation, None, notRaiseErrors=True)
            
            
        def addBlock(game, currentScene: Scene, typeEvent, info, loggable):
            blockLocation = Vector2((info['mousePos'][0] + self.camera.cords.x) // Block.SIZE.x,
                                    (info['mousePos'][1] + self.camera.cords.y) // Block.SIZE.y) 


            currentScene.setBlockByAbsolutePos(blockLocation,self.storage['selectedBlockName'],notRaiseErrors=True)
        
        
        self.addInputEvent("test", InputType.leftClick, destroyBlock)
        self.addInputEvent("test2", InputType.rightClick, addBlock)
        self.addInputEvent("keyUp", InputType.keyDown, lambda *args, **kwargs: self.camera.moveBy(Vector2(0,-200)), key=pygame.K_UP)
        self.addInputEvent("keyDown", InputType.keyDown, lambda *args, **kwargs: self.camera.moveBy(Vector2(0,200)), key=pygame.K_DOWN)
        self.addInputEvent("keyRight", InputType.keyDown, lambda *args, **kwargs: self.camera.moveBy(Vector2(200,0)), key=pygame.K_RIGHT)
        self.addInputEvent("keyLeft", InputType.keyDown, lambda *args, **kwargs: self.camera.moveBy(Vector2(-200,-0)), key=pygame.K_LEFT)
        self.addInputEvent("keyOne", InputType.keyDown, lambda *args, **kwargs: 5 / 0, key=pygame.K_1)
        
    #  self.getCurrentScene().__   
        
        def handleBlockUp(game, currentScene: Scene, typeEvent, info, loggable: Loggable):
            idInts = game.getNameSpace()['IDInts']
            
            
            # loggable.log(logType.INFO, idInts)
            # loggable.info(type(game.storage['selectedBlock']))
            # loggable.info(idInts.keys())
            # loggable.info(list(filter(lambda thing: thing > game.storage['selectedBlock'], idInts.keys())))
            if len(list(filter(lambda thing: thing > game.storage['selectedBlock'], idInts.keys()))) > 0:
                game.storage['selectedBlock'] += 1
                while game.storage['selectedBlock'] not in idInts.keys():
                    game.storage['selectedBlock'] += 1
                game.storage['selectedBlockName'] = idInts[game.storage['selectedBlock']]

            else:
                game.storage['selectedBlock'] = 1
                game.storage['selectedBlockName'] = idInts[1]
                
            loggable.info(f"block editor got changed to {game.storage['selectedBlockName']} (intID: {game.storage['selectedBlock']})")
                
        def handleBlockDown(game, currentScene: Scene, typeEvent, info, loggable: Loggable):
            idInts = game.getNameSpace()['IDInts']
            maxint = max(idInts.keys())
            
            if len(list(filter(lambda thing: thing < game.storage['selectedBlock'], idInts.keys()))) > 0:
                game.storage['selectedBlock'] -= 1
                while game.storage['selectedBlock'] not in idInts.keys():
                    game.storage['selectedBlock'] -= 1
                game.storage['selectedBlockName'] = idInts[game.storage['selectedBlock']]

            else:
                game.storage['selectedBlock'] = maxint
                game.storage['selectedBlockName'] = idInts[maxint]
            
            loggable.info(f"block editor got changed to {game.storage['selectedBlockName']} (intID: {game.storage['selectedBlock']})")
        
        self.addInputEvent("blockUp", InputType.keyDown, handleBlockUp, key=pygame.K_z)
        self.addInputEvent("blockDown", InputType.keyDown, handleBlockDown, key=pygame.K_x)
        
    
    async def __gameLoop(self) -> None:
        self.__logger.log(logType.SUCCESS, "loading engine... COMPLETE ")
        self.__logger.log(logType.INIT, "invoking onrun functions...")               
        await self.__onRun()
        self.__logger.log(logType.SUCCESS, "invoking onrun functions... DONE")   
        def executeScene(scene: Scene) -> Scene:
            if not scene.idle:
                scene.tick()
            return scene
            
        self.__logger.log(logType.INIT, "starting final game loop...")          
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
        if name in self.__inputEventsList["keyUp"]:
            if forcedType is None: return True
            elif forcedType == "leftClick": return True
        if name in self.__inputEventsList["keyDown"]:
            if forcedType is None: return True
            elif forcedType == "leftClick": return True
            
        return False
        
    
    def addInputEvent(self, name: str, typeOfInputTypeEvent: Union[str, InputType], function: callable, key: Optional[int] = None, forcedSceneName: Optional[str] = None, dontRaiseAnyErrors: bool = True, setIfDoExist: bool = False, startAsEnabled: bool = True) -> None:            
        if typeOfInputTypeEvent != str:
                typeOfInputTypeEvent = typeOfInputTypeEvent.value
        # callable[['Game', currentScene, InputType,inputEventInfo, Loggable], bool]
        # name Checking
        if self.doesInputEventNameDoExist(name):
            self.getLogger().log(logType.ERROR, f"Trying to set input event of id '{name}' but name was already claimed!")
            if not dontRaiseAnyErrors:
                raise invalidName(f"name ''{name}'' is already claimed as name for an event!")
            if not setIfDoExist: return
            self.getLogger().log(logType.INFO, f"f'{name}' will be set anyways, because flag of ignoring that is set!")
        
        eventInfo = {'key': key, 'enabled': startAsEnabled, 'forcedSceneName': forcedSceneName, 'type': typeOfInputTypeEvent, 'name': name}
        
        self.__inputEventsList['events'][name] = [function, 
                                         eventInfo]
        self.__inputEventsList[typeOfInputTypeEvent][name] = [function, 
                                                     eventInfo]
        
        self.getLogger().log(logType.SUCCESS, f"New input event has been added with name of '{name}'. information about this event: {eventInfo}")
        
            # if forcedSceneName is not None:
                
    def removeInputEvent(self, name: str, dontRaiseAnyErrors: bool = True) -> None:
        if not self.doesInputEventNameDoExist(name):
            self.getLogger().log(logType.ERROR, f"Trying to remove input event of id '{name}' but name wasnt used!")
            if not dontRaiseAnyErrors:
                raise invalidName(f"didn't find event of name '{name}'")
            return
            
        eventInfo = self.__inputEventsList['events'][name][1]
            
        del self.__inputEventsList[self.__inputEventsList['events'][name][1]['type']][name]
        del self.__inputEventsList['events'][name]
        
        self.getLogger().log(logType.SUCCESS, f"Input event of id '{name}' has been deleted. The event info: {eventInfo}")
        
    
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
                "keyDown": {
                },
                "keyUp": {
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
        
    # logger
    
    def getGame(self): return self
        
    def getLogger(self) -> Logger:
        return self.__logger

    # already implemented in Loggable    
    # def log(self, logtype: logType, message: str) -> None:
    #     self.__logger.log(logtype, message, self.__logParent)
        
    def __init__(self, resolution: tuple[int,int]) -> None:
        self.__logger: Logger = Logger(self)
        
        self.__logger.log(logType.INIT, "loading engine...")
        
        
        super().__init__(logParent=ParentForLogs("game"))
        # save data
        self.__resolution = resolution
        self.__isGameOn: bool = True
        self.__scenes: dict[str,Scene] = {}
        self.__currentScene: None | Scene = None
        self.storage = {
            "selectedBlock": 1,
            "selectedBlockName": "dirt"
        }
        self.__inputEventsList = {
            # "forcedScenes": {
                
            # },
            "events": {
            },
            "keyDown": {
            },
            "keyUp": {
            },
            "rightClick": {
                
            },
            "leftClick": {
                
            }
        }
        
        
        
        
        self.__logger.log(logType.INIT, "loading engine... (loading pygame stuff)")
        # pygame issues
        pygame.init()
        pygame.font.init()
        self.__display = pygame.display.set_mode(self.__resolution)
        pygame.display.set_caption("Kantraft")
        self.clock = pygame.time.Clock()
        self.__logger.log(logType.SUCCESS, "loading engine... (loading pygame stuff - COMPLETE)")
        

        self.__resourceManager = resourceManager(self)
        
        # asyncio
        # self.__eventLoop = asyncio.new_event_loop()
        # asyncio.set_event_loop(self.__eventLoop)
        # asyncio.create_task(self.__gameLoop(), name="gameLoop")
        
        self.__logger.log(logType.INIT, "invoking asyncio main game loop... ")
        asyncio.run(self.__gameLoop())
        
        
        
        