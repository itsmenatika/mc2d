# external imports
import pygame
from pygame.math import Vector2
# import sys
# import traceback
import asyncio
import os
from typing import Optional, Iterable, ItemsView, Union
import time

# internal imports
from bin.map import Scene, Chunk, currentScene, Block
from bin.camera import Camera
from bin.namespace import resourceManager
# from bin.worldGenerator.overworld import worldGeneratorNormal
from bin.worldGenerator.flatWorld import flatWorldGenerator
from bin.abstractClasses import InputType, inputEventInfo, EventType
from bin.logger import Logger, Loggable, logType, ParentForLogs
# from bin.event import Event
from bin.entity import Entity, entityType

class gameEngineError(Exception): pass
class invalidName(gameEngineError): pass


GAMEVERSION: str = "PRE-INDEV 1"
GAMEVERSIONINT: int = 1

class Game(Loggable):
    '''main class'''
    
    
    async def __drawLoop(self) -> None:
        '''main draw loop'''
        # self.__currentScene.draw()
        self.__display.fill((0,0,0))
        self.camera.draw(self.getDisplayOrginal())
        pygame.display.flip()
        
    async def __eventHandler(self) -> None:
        '''a function that are used with handling with events'''
        
        # getting all events
        self.__events = pygame.event.get()
        
        # example of function that could be passed here: callable[['Game', currentScene, InputType,inputEventInfo], bool]
        
        
        # getting basic info
        self.__buttonsClicked: tuple[bool, bool, bool] = pygame.mouse.get_pressed()
        self.__mousePos = pygame.mouse.get_pos()
        self.__keysPressed = pygame.key.get_pressed()
        
        
        # mouse hold detecting
        if self.__buttonsClicked[0]:
            for eventName, eventTwo in self.__inputEventsList["leftClickHold"].items():
                if eventTwo[1]['enabled']:
                    try:
                        if eventTwo[0](self, self.getCurrentScene(), InputType.leftClickHold, {
                            "buttonClicked": self.__buttonsClicked,
                            "mousePos": self.__mousePos,
                            "allKeysPressed": self.__keysPressed,
                            "leftShift": self.__keysPressed[pygame.K_LSHIFT],
                            "rightShift": self.__keysPressed[pygame.K_RSHIFT],
                            "anyShift":  self.__keysPressed[pygame.K_LSHIFT] or self.__keysPressed[pygame.K_RSHIFT]
                        }, Loggable(game=self, logParent=ParentForLogs(name=f"inputevent_{eventName}", parent=self.getLogParent()))): break
                    except Exception as e:
                        self.getLogger().errorWithTraceback(f"An error has occured during trying to execute a function given to the event with the name of '{eventName}' (eventData: {eventTwo[1]})", e)
                        # traceback.print_exception(e)
                        # print("")
                        
        if self.__buttonsClicked[1]:
            for eventName, eventTwo in self.__inputEventsList["wheelClickHold"].items():
                if eventTwo[1]['enabled']:
                    try:
                        if eventTwo[0](self, self.getCurrentScene(), InputType.wheelClickHold, {
                            "buttonClicked": self.__buttonsClicked,
                            "mousePos": self.__mousePos,
                            "allKeysPressed": self.__keysPressed,
                            "leftShift": self.__keysPressed[pygame.K_LSHIFT],
                            "rightShift": self.__keysPressed[pygame.K_RSHIFT],
                            "anyShift":  self.__keysPressed[pygame.K_LSHIFT] or self.__keysPressed[pygame.K_RSHIFT]
                        }, Loggable(game=self, logParent=ParentForLogs(name=f"inputevent_{eventName}", parent=self.getLogParent()))): break
                    except Exception as e:
                        self.getLogger().errorWithTraceback(f"An error has occured during trying to execute a function given to the event with the name of '{eventName}' (eventData: {eventTwo[1]})", e)
                        # traceback.print_exception(e)
                        # print("")
                        
        if self.__buttonsClicked[2]:
            for eventName, eventTwo in self.__inputEventsList["rightClickHold"].items():
                if eventTwo[1]['enabled']:
                    try:
                        if eventTwo[0](self, self.getCurrentScene(), InputType.rightClickHold, {
                            "buttonClicked": self.__buttonsClicked,
                            "mousePos": self.__mousePos,
                            "allKeysPressed": self.__keysPressed,
                            "leftShift": self.__keysPressed[pygame.K_LSHIFT],
                            "rightShift": self.__keysPressed[pygame.K_RSHIFT],
                            "anyShift":  self.__keysPressed[pygame.K_LSHIFT] or self.__keysPressed[pygame.K_RSHIFT]
                        }, Loggable(game=self, logParent=ParentForLogs(name=f"inputevent_{eventName}", parent=self.getLogParent()))): break
                    except Exception as e:
                        # self.getLogger().log(logType.ERROR, f"An error has occured during trying to execute a function given to the event with the name of '{eventName}' (eventData: {eventTwo[1]}):\n")
                        # traceback.print_exception(e)
                        # print("")
                        self.getLogger().errorWithTraceback(f"An error has occured during trying to execute a function given to the event with the name of '{eventName}' (eventData: {eventTwo[1]})", e)
        
        # looping through them
        for event in self.__events:
            match event.type:
                case pygame.QUIT:
                    # handling when user want to force quit by pressing "X" on their window
                    self.getLogger().log(logtype=logType.ERROR, message="Game has been forcefully quitted by the engine!")
                    self.__writeInformationAboutClosedGame()
                    self.getLogger().log(logtype=logType.ERROR, message="Game has been forcefully quitted by the player!", parent=None)
                    self.__isGameOn = False
                case pygame.KEYUP:
                    # handling events when user stop pressing key
                    for eventName, eventTwo in self.__inputEventsList["keyUp"].items():
                        if eventTwo[1]['key'] == event.key:
                            try:
                                if eventTwo[0](self, self.getCurrentScene(), InputType.keyUp, {
                                    "buttonClicked": event.key,
                                    "window": event.window,
                                    "unicode": event.unicode,
                                    "mod": event.mod,
                                    "scancode": event.scancode,
                                    "allKeysPressed": self.__keysPressed,
                                    "leftShift": self.__keysPressed[pygame.K_LSHIFT],
                                    "rightShift": self.__keysPressed[pygame.K_RSHIFT],
                                    "anyShift":  self.__keysPressed[pygame.K_LSHIFT] or self.__keysPressed[pygame.K_RSHIFT]
                                    
                                }, Loggable(game=self,logParent=ParentForLogs(name=f"inputevent_{eventName}", parent=self.getLogParent()))): break
                            except Exception as e:
                                # self.getLogger().log(logType.ERROR, f"An error has occured during trying to execute a function given to the event with the name of '{eventName}' (eventData: {eventTwo[1]}):\n")
                                # traceback.print_exception(e)
                                # print("")
                                self.getLogger().errorWithTraceBack(f"An error has occured during trying to execute a function given to the event with the name of '{eventName}' (eventData: {eventTwo[1]})", e)
                case pygame.KEYDOWN:
                    # print(event)
                    # handling events when user start pressing key
                    for eventName, eventTwo in self.__inputEventsList["keyDown"].items():
                        # print(event.key, event['key'])
                        # print(event[1])
                        try:
                            if eventTwo[1]['key'] == event.key:
                                if eventTwo[0](self, self.getCurrentScene(), InputType.keyDown, {
                                    "buttonClicked": event.key,
                                    "window": event.window,
                                    "unicode": event.unicode,
                                    "mod": event.mod,
                                    "scancode": event.scancode,
                                    "allKeysPressed": self.__keysPressed,
                                    "leftShift": self.__keysPressed[pygame.K_LSHIFT],
                                    "rightShift": self.__keysPressed[pygame.K_RSHIFT],
                                    "anyShift":  self.__keysPressed[pygame.K_LSHIFT] or self.__keysPressed[pygame.K_RSHIFT]
                                }, Loggable(game=self,logParent=ParentForLogs(name=f"inputevent_{eventName}", parent=self.getLogParent()))): break
                        except Exception as e:
                            # type, value, traceback = sys.exc_info()
                            # traceback.print_exception(e)
                            # print(type,value,traceback)
                            # self.getLogger().log(logType.ERROR, f"An error has occured during trying to execute a function given to the event with the name of '{eventName}' (eventData: {eventTwo[1]}):\n")
                            # traceback.print_exception(e)
                            # print("")
                            self.getLogger().errorWithTraceback(f"An error has occured during trying to execute a function given to the event with the name of '{eventName}' (eventData: {eventTwo[1]})", e)
                    
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
                    # print(event, event.button == 1)
                    # handling events when user clicks something on their mouse
                    
                    
                    # print(self.__inputEventsList)
                    # print(Event)
                    if event.button == 1:
                        # print('sw')
                        for eventName, eventTwo in self.__inputEventsList["leftClick"].items():
                            if eventTwo[1]['enabled']:
                                try:
                                    if eventTwo[0](self, self.getCurrentScene(), InputType.leftClick, {
                                        "buttonClicked": event.button,
                                        "allButtonsClicked": self.__buttonsClicked,
                                        "window": event.window,
                                        "mousePos": self.__mousePos,
                                        "allKeysPressed": self.__keysPressed,
                                        "leftShift": self.__keysPressed[pygame.K_LSHIFT],
                                        "rightShift": self.__keysPressed[pygame.K_RSHIFT],
                                        "anyShift":  self.__keysPressed[pygame.K_LSHIFT] or self.__keysPressed[pygame.K_RSHIFT]  
                                    }, Loggable(game=self, logParent=ParentForLogs(name=f"inputevent_{eventName}", parent=self.getLogParent()))): break
                                except Exception as e:
                                    self.getLogger().errorWithTraceback(f"An error has occured during trying to execute a function given to the event with the name of '{eventName}' (eventData: {eventTwo[1]})", e)
                                    # traceback.print_exception(e)
                                    # print("")
                    if event.button == 2:
                        for eventName, eventTwo in self.__inputEventsList["wheelClick"].items():
                            if eventTwo[1]['enabled']:
                                try:
                                    if eventTwo[0](self, self.getCurrentScene(), InputType.leftClick, {
                                        "buttonClicked": event.button,
                                        "allButtonsClicked": self.__buttonsClicked,
                                        "window": event.window,
                                        "mousePos": self.__mousePos,
                                        "allKeysPressed": self.__keysPressed,
                                        "leftShift": self.__keysPressed[pygame.K_LSHIFT],
                                        "rightShift": self.__keysPressed[pygame.K_RSHIFT],
                                        "anyShift":  self.__keysPressed[pygame.K_LSHIFT] or self.__keysPressed[pygame.K_RSHIFT]  
                                    }, Loggable(game=self, logParent=ParentForLogs(name=f"inputevent_{eventName}", parent=self.getLogParent()))): break
                                except Exception as e:
                                    self.getLogger().errorWithTraceback(f"An error has occured during trying to execute a function given to the event with the name of '{eventName}' (eventData: {eventTwo[1]})", e)
                                    # traceback.print_exception(e)
                                    # print("")
                    if event.button == 3:
                        for eventName, eventTwo in self.__inputEventsList["rightClick"].items():
                            if eventTwo[1]['enabled']:
                                try:
                                    if eventTwo[0](self, self.getCurrentScene(), InputType.leftClick, {
                                        "buttonClicked": event.button,
                                        "allButtonsClicked": self.__buttonsClicked,
                                        "window": event.window,
                                        "mousePos": self.__mousePos,
                                        "allKeysPressed": self.__keysPressed,
                                        "leftShift": self.__keysPressed[pygame.K_LSHIFT],
                                        "rightShift": self.__keysPressed[pygame.K_RSHIFT],
                                        "anyShift":  self.__keysPressed[pygame.K_LSHIFT] or self.__keysPressed[pygame.K_RSHIFT]  
                                    }, Loggable(game=self, logParent=ParentForLogs(name=f"inputevent_{eventName}", parent=self.getLogParent()))): break
                                except Exception as e:
                                    # self.getLogger().log(logType.ERROR, f"An error has occured during trying to execute a function given to the event with the name of '{eventName}' (eventData: {eventTwo[1]}):\n")
                                    # traceback.print_exception(e)
                                    # print("")
                                    self.getLogger().errorWithTraceback(f"An error has occured during trying to execute a function given to the event with the name of '{eventName}' (eventData: {eventTwo[1]})", e)
                
               
                    
            
    async def __onRun(self) -> None:
        '''a function that will be run once at the beginning'''
        # be careful with everything here. that was written fastly on 3 am
        
        # basics
        t = Scene(self, name="test", worldGenerator=flatWorldGenerator)
        self.setCurrentScene(t)
        self.camera = Camera(cords=Vector2(0,70), game=self)
        
        # functions for adding and destroying blocks
        def destroyBlock(game, currentScene: Scene, typeEvent, info, loggable):
            block_loc_x = (info['mousePos'][0] + self.camera.cords.x) // Block.SIZE.x
            block_loc_y = (info['mousePos'][1] + self.camera.cords.y) // Block.SIZE.y

            blockLocation = (int(block_loc_x), int(block_loc_y))

            currentScene.setBlockByAbsolutePosWithEvent(blockLocation, None, dontRaiseErrors=True)
            
            
        def addBlock(game, currentScene: Scene, typeEvent, info, loggable):
            block_loc_x = (info['mousePos'][0] + self.camera.cords.x) // Block.SIZE.x
            block_loc_y = (info['mousePos'][1] + self.camera.cords.y) // Block.SIZE.y

            blockLocation = (int(block_loc_x), int(block_loc_y))


            currentScene.setBlockByAbsolutePosWithEvent(blockLocation, self.storage['selectedBlockName'], dontRaiseErrors=True)
        
        
        # functions for changing block
        def handleBlockUp(game, currentScene: Scene, typeEvent, info, loggable: Loggable):
            idInts = game.getNameSpace()['IDInts']

            list_of_blocks = []

            filtered_blocks = filter(lambda key: key > game.storage['selectedBlock'], idInts.keys())

            list_of_blocks = list(filtered_blocks)
            

            # loggable.log(logType.INFO, idInts)
            # loggable.info(type(game.storage['selectedBlock']))
            # loggable.info(idInts.keys())
            # loggable.info(list(filter(lambda thing: thing > game.storage['selectedBlock'], idInts.keys())))
            if len(list_of_blocks) > 0:
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
        
        
        def getBlock(game, currentScene: Scene, typeEvent, info, loggable: Loggable):
            pos = Vector2(info['mousePos'][0]+self.camera.cords.x, info['mousePos'][1]+self.camera.cords.y)
            block = self.getCurrentScene().getBlock(pos)
            if block != None:
                game.storage['selectedBlock'] = block.IDInt
                game.storage['selectedBlockName'] = block.ID
                loggable.info(f"block editor got changed to {game.storage['selectedBlockName']} (intID: {game.storage['selectedBlock']})")
                
        # binding events
        self.addInputEvent("test", InputType.rightClickHold, destroyBlock)
        # self.addInputEvent("test2", InputType.leftClickHold, addBlock)
        self.addInputEvent("keyUp", InputType.keyDown, lambda *args, **kwargs: self.camera.moveBy(Vector2(0,-200)), key=pygame.K_UP)
        self.addInputEvent("keyDown", InputType.keyDown, lambda *args, **kwargs: self.camera.moveBy(Vector2(0,200)), key=pygame.K_DOWN)
        self.addInputEvent("keyRight", InputType.keyDown, lambda *args, **kwargs: self.camera.moveBy(Vector2(200,0)), key=pygame.K_RIGHT)
        self.addInputEvent("keyLeft", InputType.keyDown, lambda *args, **kwargs: self.camera.moveBy(Vector2(-200,-0)), key=pygame.K_LEFT)
        
        self.addInputEvent("keyOne", InputType.keyDown, lambda *args, **kwargs: 5 / 0, key=pygame.K_1)
        
        self.addInputEvent("blockUp", InputType.keyDown, handleBlockUp, key=pygame.K_z)
        self.addInputEvent("blockDown", InputType.keyDown, handleBlockDown, key=pygame.K_x)  
        self.addInputEvent("blockGet", InputType.wheelClick, getBlock)
        self.addInputEvent("saveMap", InputType.keyDown, key=pygame.K_s, function=lambda *args, **kwargs: self.getCurrentScene().saveWorld())
        
    
        def recompileLight(game, currentScene: Scene, typeEvent, info, loggable: Loggable):
            currentScene.getLightingManager().recompileBlocks()
            
        self.addInputEvent("t", InputType.keyDown, key=pygame.K_l, function=recompileLight)
        
        
        def spawnEntity(game, currentScene: Scene, typeEvent, info, loggable: Loggable):
            mousePos = Vector2(info['mousePos'])
            currentScene.addEntity(Entity(pygame.image.load("resources/tiles/allium.png"), currentScene.getChunk(currentScene.getChunkPosFromCords(mousePos)), mousePos+self.camera.cords, entityType.falling_block))
            
        self.addInputEvent("test2", InputType.leftClick, spawnEntity)
            
            
        

    async def __tick(self):
        while self.__isGameOn:
            # 20 per second (used for physics etc, NOT USE IT FOR RENDER PURPOSES)
            # spread ticks accross scenes
            for scene in self.__scenes.values():
                # main ticks
                if not scene.idle: await scene.tick()
                
            self.__tickPerSecondTime.append(time.time())
            # print(self.getTicksPerSecond())
            await asyncio.sleep(0.05)
            
    async def __resertTickNumber(self):
        while self.__isGameOn:
            self.__tickPerSecond = len(self.__tickPerSecondTime)
            self.__tickPerSecondTime.clear()
            await asyncio.sleep(1)
            
    def getTicksPerSecond(self) -> int:
        return self.__tickPerSecond

    async def __gameLoop(self) -> None:
        '''a main loop that is run once every frame'''
        
        # info for logger
        self.__logger.log(logType.SUCCESS, "Succesfully initi1alized engine!")  
        
        # await onrun function 
        self.__logger.log(logType.INIT, "Invoking function of [onrun] type...")            
        await self.__onRun()
        self.__logger.log(logType.SUCCESS, "Succesfully invoked functions of [onrun]!")   
        
        self.__logger.log(logType.INIT, "intializing ticks...")
        self.__tickPerSecond = 20
        self.__tickPerSecondTime = []
        asyncio.create_task(coro=self.__tick(), name="ticker")
        # print(asyncio.all_tasks())
        self.__logger.log(logType.SUCCESS, "intialized ticks.")
        
        # # giving tick time for every scene for scene specific events
        # def executeScene(scene: Scene) -> Scene:
        #     if not scene.idle:
        #         scene.tick()
        #     return scene
            
        # final main loop
        self.__logger.log(logType.INIT, "Starting the final game loop.")          
        while self.__isGameOn:
            await self.__eventHandler()
            
            # for scene in self.__scenes.values():
            #     if not scene.idle: await scene.tick()
            
            await asyncio.sleep(0.000000001)
            await self.__drawLoop()
            self.clock.tick(1000)
            # self.clock.get_rawtime()
            # print(self.clock.get_fps())
            
            
            
        
    
    async def __functionToGetAnotherMoreSpace(self) -> None:
        '''function that does nothing but is just to give time another async functions, because i need to await something.\n
            You can use just await asyncio.sleep(0.01) if you really want.'''
        await asyncio.sleep(0.01)
    
    
    
    # SCENE MANAGING
    
    def addScene(self, scene: Scene, name: str = "scene") -> None:
        '''adding scene\n
            Args:\n
                * scene: Scene -> that scene
                * name: str -> name of the scene (recommended, default name: 'scene')
            Returns:\n
                None'''
        if name in self.__scenes:
            raise gameEngineError(f"scene of name ${name} already do exist!")
          
        self.__scenes[name] = scene
            
        
    def removeScene(self, name: str) -> None:
        '''removing scene\n
            Args:\n
                * name: str -> name of the scene (recommended, default name: 'scene')
            Returns:\n
                None'''
        if name not in self.__scenes:
            raise gameEngineError(f"scene of name ${name} doesnt exist!")
        
        if self.__currentScene == self.__scenes[name]:
            self.__currentScene = None
            del self.__scenes[name]
            
        
    def findNameOfScene(self, scene: Scene) -> str | None:
        '''find scene by object\n
            Args:\n
                * scene: Scene -> that scene
            Returns:\n
                str: name of the scene'''
        for name, sceneT in self.__scenes:
            if scene == sceneT:
                return name
        return None
    
    
    def isSceneAdded(self, scene: Scene) -> bool:
        '''checking if scene has been added (by object)\n
            Args:\n
                * scene: Scene -> that scene
            Returns:\n
                bool: result'''
        return scene in self.__scenes.values()

    
    def isSceneAddedByName(self, name: str) -> bool:
        '''checking if scene has been added (by name)\n
            Args:\n
                * name: str -> name of the scene
            Returns:\n
                bool: result'''
        return name in self.__scenes.keys()
    
    def getScene(self, name: str) -> Optional[Scene]:
        '''returns scene object using a name of this scene. returns none if there's no scene with that name\n
            Args:\n
                * name: str -> name of the scene
            Returns:\n
                bool | None: result'''
        return self.__scenes.get(name, default=None)
    
            
        
            
    def setCurrentScene(self, scene: Scene) -> None:
        '''setting current scene\n
            Args:\n
                * scene: Scene -> that scene
            Returns:\n
                None'''
        self.__currentScene = scene
        
    def getCurrentScene(self) -> Scene:
        '''get you current scene'''
        return self.__currentScene
    
    # resource managing stuff
        
    def getResourceManager(self) -> resourceManager:
        '''allows you to get resource manager'''
        return self.__resourceManager

    def getNameSpace(self) -> dict:
        '''allows you to extract namespace from resource manager'''
        return self.__resourceManager.getNameSpace()
    
    # ------
    # input events management
    # ------
    
    def doesInputEventNameDoExist(self, name: str, forcedType: Optional[Union[InputType, str]] = None) -> bool:
        '''check if input event does exist\n
            Args:\n
                * name: str -> Name
                * forcedType: Optional[InputType|str] -> only count if this was of specified type
            Returns:\n
                bool: result'''

        def is_in(target: str, key: str, in_dict: dict) -> bool:
            if not target in in_dict:
                return False
            
            return forcedType is None or forcedType == key
                
        # get value from enum      
        if forcedType != None and forcedType != str:
            forcedType = forcedType.value
        
        key_bindings: list[str] = ["rightClick", "leftClick", "keyUp", "keyDown"]

        for key in key_bindings:
            input_key_events = self.__inputEventsList[key]

            return is_in(name, key, input_key_events)

        # just checking
        # i need to optimize this someday...
        # if name in self.__inputEventsList["rightClick"]:
        #     if forcedType is None: return True
        #     elif forcedType == "rightClick": return True
        # if name in self.__inputEventsList["leftClick"]:
        #     if forcedType is None: return True
        #     elif forcedType == "leftClick": return True
        # if name in self.__inputEventsList["keyUp"]:
        #     if forcedType is None: return True
        #     elif forcedType == "leftClick": return True
        # if name in self.__inputEventsList["keyDown"]:
        #     if forcedType is None: return True
        #     elif forcedType == "leftClick": return True
            
        return False
        
    
    def addInputEvent(self, name: str, typeOfInputTypeEvent: Union[str, InputType], function: callable, key: Optional[int] = None, forcedSceneName: Optional[str] = None, dontRaiseAnyErrors: bool = True, setIfDoExist: bool = False, startAsEnabled: bool = True) -> None:            
        '''adding new input event\n
        Args:\n
            * name: str -> unique identificator of this new input event
            * typeOfInputTypeEvent: str | InputType -> type of this event
            * function: callable: function that will be called when this event occures, function must returns bool (bool will indicate if game engine have to still look for another functions for the same event). Game engine will provide to functions this type of data:
                - game: Game -> main object of the game
                - currentScene: Scene -> current scene of the game
                - inputtype: inputType -> type of the input that has been triggered
                - inputEventInfo: dict -> detail information about event
            * key: Optional[int] -> key. (for example like pygame.K_0)
            * forcedSceneName: Optional[str] -> force this to only works if current name scene has specified name (doesnt work)
            * dontRaiseAnyErrors: bool = True -> dont raise any errors if name is claimed
            * setIfDoExist: bool = False -> set even if exists
            * startAsEnabled: bool = True -> start as enabled event
        Returns:\n
            None'''
            
        # i couldn't put that type into working, idk why
        #callable[['Game', currentScene, InputType,inputEventInfo], bool]
            
            
        # get value from enum
        if typeOfInputTypeEvent != str:
            typeOfInputTypeEvent = typeOfInputTypeEvent.value
                
        # callable[['Game', currentScene, InputType,inputEventInfo, Loggable], bool]
        # name Checking
        
        # handling situation if there was already event with that name
        if self.doesInputEventNameDoExist(name):
            self.getLogger().log(logType.ERROR, f"Tried to initialize an input event for already existing input event \'{name}\'!")
            if not dontRaiseAnyErrors:
                raise invalidName(f"Name of the input event (\'{name}\') is not available.")
            if not setIfDoExist: return
            # Tu nie wiedziałem jak to by inaczej opisać (nie czaje do końca xd)
            self.getLogger().log(logType.INFO, f"f'{name}' will be set anyways, because a flag of ignoring that is set!")
        
        # setting event
        eventInfo = {'key': key, 'enabled': startAsEnabled, 'forcedSceneName': forcedSceneName, 'type': typeOfInputTypeEvent, 'name': name}
        
        self.__inputEventsList['events'][name] = [function, eventInfo]
        self.__inputEventsList[typeOfInputTypeEvent][name] = [function, eventInfo]
        
        # logs
        self.getLogger().log(logType.SUCCESS, f"Initialized a new input event \'{name}\'! Event info: {eventInfo}.")
        
            # if forcedSceneName is not None:
                
    def removeInputEvent(self, name: str, dontRaiseAnyErrors: bool = True) -> None:
        '''removes input event\n
            Args:\n
                * name: str -> Name
                * dontRaiseAnyErrors: bool = True -> dont raise any errors if name is not claimed
            Returns:\n
                None''' 
                
        # check if name exist
        if not self.doesInputEventNameDoExist(name):
            self.getLogger().log(logType.ERROR, f"Attempted to uninitialize not existing event key \'{name}\'!")
            if not dontRaiseAnyErrors:
                raise invalidName(f"Failed to find an event input for '{name}'!")
            return
            
        # deleting event
        eventInfo = self.__inputEventsList['events'][name][1]
            
        del self.__inputEventsList[eventInfo['type']][name]
        del self.__inputEventsList['events'][name]
        
        # logs
        self.getLogger().log(logType.SUCCESS, f"Succesfully uninitialized event key for '{name}'! Event info: {eventInfo}.")
        
    
    def getInputEvents(self, ofType:Optional[Union[str, InputType]] = None) -> list[tuple[str,list[callable, dict]]]:   
        '''get all input events\n
            Args:\n
                * ofType: Optional[Union[str|InputType]] -> only of specified type. That is optional
            Returns:\n
                list[tuple[str,list[callable, dict]]]'''   
                       
        if ofType == None:
            return self.__events['events'].items()
        
        if ofType != None and ofType != str:
            ofType = ofType.value
            
        return self.__inputEventsList[ofType].items()
            
        
    def clearInputEvents(self, ofType: Optional[Union[str, InputType]] = None) -> None:
        '''removes all input events\n
            Args:\n
                * ofType: Optional[Union[str|InputType]] -> only of specified type. That is optional
            Returns:\n
                None'''   
        if ofType != None and ofType != str:
            ofType = ofType.value
        
        if ofType == None:
                self.__inputEventsList = {
                # "forcedScenes": {
                    
                # },
                "events": {},
                "keyDown": {},
                "keyUp": {},
                "rightClick": {},
                "leftClick": {},
                "wheelClick": {},
                "rightClickHold": {},
                "leftClickHold": {},
                "wheelClickHold": {}
            }
                
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
    
    def getLogger(self) -> Logger:
        return self.__logger
    
    def clearLogger(self) -> None:
        self.__logger.clear()
    
    
    # anothet getting
    
    @staticmethod
    def getVersion() -> str: return GAMEVERSION
    
    @staticmethod
    def getVersionInt() -> int: return GAMEVERSIONINT
    
    @staticmethod
    def getVersionFull() -> tuple[str, int]: return (GAMEVERSION, GAMEVERSIONINT)
    
    
    def getGame(self): return self
        

    def getDisplayOrginal(self) -> pygame.surface.Surface:
        '''allows you to get orginal display that is used with handling with pygame'''
        return self.__display
    
    def getEvents(self) -> list[pygame.event.Event]:
        '''Get events from pygame'''
        return self.__events

    # already implemented in Loggable    
    # def log(self, logtype: logType, message: str) -> None:
    #     self.__logger.log(logtype, message, self.__logParent)
    
    
    def __writeInformationAboutClosedGame(self) -> None:
        with open("temp/isGameOpen", "w") as f:
            f.write("0")
        
    def __init__(self, resolution: tuple[int,int]) -> None:
        super().__init__(logParent=ParentForLogs("game"))
        # logger
        self.__logger: Logger = Logger(self)
        
        self.__logger.log(logType.INIT, "Initializing engine...")
        
        
        if not os.path.exists("bin"):
            self.__logger.log(logType.ERROR, "Unable to run the game! Failed to access the directory \'bin\'.")
            self.__logger.log(logType.CRASHREPORT, "Switched state for game by this engine (Running -> False).")
            self.__writeInformationAboutClosedGame()
            exit()
            
        if not os.path.exists("data"):
            self.__logger.log(logType.ERROR, "Unable to run the game! Failed to access the directory \'data\'.")
            self.__logger.log(logType.CRASHREPORT, "Switched state for game by this engine (Running -> False).")
            self.__writeInformationAboutClosedGame()
            exit()
            
        if not os.path.exists("resources"):
            self.__logger.log(logType.ERROR, "Unable to run the game! Failed to access the directory \'resources\'.")
            self.__logger.log(logType.CRASHREPORT, "Switched state for game by this engine (Running -> False).")
            self.__writeInformationAboutClosedGame()
            exit()
        
        # basics
        self.__resolution = resolution
        self.__isGameOn: bool = True
        self.__scenes: dict[str,Scene] = {}
        self.__currentScene: Optional[Scene] = None
        self.storage = {
            "selectedBlock": 1,
            "selectedBlockName": "dirt"
        }
        self.__inputEventsList = {
            # "forcedScenes": {
                
            # },
            "events": {},
            "keyDown": {},
            "keyUp": {},
            "rightClick": {},
            "leftClick": {},
            "wheelClick": {},
            "rightClickHold": {},
            "leftClickHold": {},
            "wheelClickHold": {}
        }
        
        
        
        
        self.__logger.log(logType.INIT, "Gathering pygame resources...")
        
        
        # pygame issues
        pygame.init()
        pygame.font.init()
        self.__display = pygame.display.set_mode(self.__resolution)
        pygame.display.set_caption("Kantraft")
        self.clock = pygame.time.Clock()
        self.__logger.log(logType.SUCCESS, "Succesfully gathered pygame resources!")
        

        self.__resourceManager = resourceManager(self)
        
        # asyncio
        # self.__eventLoop = asyncio.new_event_loop()
        # asyncio.set_event_loop(self.__eventLoop)
        # asyncio.create_task(self.__gameLoop(), name="gameLoop")
        
        
        # main loop
        
        self.__logger.log(logType.INIT, "Invoking engine\'s asynchronous main-loop...")
        asyncio.run(self.__gameLoop())
        
        
        
        