# external imports
import tkinter as Tk
from tkinter import ttk
from tkinter import messagebox
# import asyncio
from multiprocessing import Process
import asyncio
import os

# internal imports
import bin


def startGame(): bin.Game((1280,720))

class Launcher:
    async def __logUpdater(self):
        while self.__launcherRunning:
            with open("data/logs/latest.log", "r") as f:
                content = f.read()
                if content != self.__Logs_previousContent:
                    self.__gameLogs.config(state="normal")
                    self.__gameLogs.delete(0.0, Tk.END)
                    self.__gameLogs.insert(0.0, content)
                    self.__gameLogs.config(state="disabled")
                    self.__gameLogs.see(Tk.END)
                    self.__Logs_previousContent = content
            await asyncio.sleep(0.1)
                
    async def __loopEvent(self):
        asyncio.create_task(self.__logUpdater(), name="logUpdater")  
        while self.__launcherRunning:
            self.__root.update()
            await asyncio.sleep(0.01)
            
    def stopLauncherEvent(self, event, forced: bool = False) -> None:
        if event.widget == self.__root or forced == True:
            self.__launcherRunning = False
                
    
    def setIsGameOpen(self, value: bool) -> None:
        with open("temp/isGameOpen", "w") as f:
            f.write("1" if value else "0")
            
    def getIsGameOpen(self) -> bool:
        with open("temp/isGameOpen", "r") as f:
            return True if f.read() == "1" else False
    
    def play(self, *args, **kwargs) -> None:
        gameStarted = self.getIsGameOpen()
        
        if gameStarted:
            odp = messagebox.askokcancel("Warning", "A game process is already running. We can't guarantee stability of a new game instance. Do you want to play anyway?") 
            if not odp: return
        
        self.setIsGameOpen(True)
            
        gameStarted = True
        p = Process(target=startGame)
        p.start()
        
    def ensuringThatEveryFileDoExist(self) -> None:
        if not os.path.exists("temp/isGameOpen"):
            self.setIsGameOpen(False)
        
    def __init__(self) -> None:
        # # is gameOpen
        # with open("data/isGameOpen", "w") as f:
        #     f.write("0")
            
        # setproctitle.setproctitle("mc2d Launchers")
        self.ensuringThatEveryFileDoExist()
            
        self.__launcherRunning: bool = True
        
        # basic tkinter stuff
        self.__root = Tk.Tk()
        self.__root.title("mc2d Launcher")
        self.__root.geometry("854x480")
        self.__root.configure()

        # ------
        # main menu
        # ---------
        self.__notebookMenu = ttk.Notebook(master=self.__root)

        # updates
        updates = Tk.Frame(master=self.__notebookMenu, bg="gray")
        self.__notebookMenu.add(updates, text="Update Notes")

        #  launcher logs
        launcherLogs = ttk.Frame(master=self.__notebookMenu)
        self.__notebookMenu.add(launcherLogs, text="Launcher logs")


        #  game logs
        self.__gameLogsFrame = ttk.Frame(master=self.__notebookMenu)
        self.__notebookMenu.add(self.__gameLogsFrame, text="Recent game logs")

        self.__gameLogs = Tk.Text(master=self.__gameLogsFrame, bg="lightgray", fg="black")
        self.__gameLogs.pack(side="top", fill="both", expand=1)

        #  account
        self.__accountFrame = ttk.Frame(master=self.__root)
        self.__notebookMenu.add(self.__accountFrame, text="Account and launcher Settings")


        # adding notebook to the area
        self.__notebookMenu.pack(side="top", expand=1, fill="both")



        # -------------
        # self.__bottomFrame things
        # --------------
        

        self.__bottomFrame = ttk.Frame(master=self.__root)
        
        # ----
        # profile frame (in bottom)
        # ----
        
        self.__profileFrame = ttk.Frame(master=self.__bottomFrame)

        # selector profile
        SelectorFrame = ttk.Frame(master=self.__profileFrame)
        SelectorFrame.pack(side="top", pady=3)

        ttk.Label(master=SelectorFrame,text="Profile:  ").pack(side="left")
        selectedProfile = Tk.StringVar(master=self.__root, value="PRE-INDEV 1")
        selectorProfile = ttk.Combobox(master=SelectorFrame, textvariable=selectedProfile, width=20)
        selectorProfile.pack(side="left")

        # edit profile
        editFrame = ttk.Frame(master=self.__profileFrame)
        editFrame.pack(side="top", fill="x", expand=1, pady=3)

        newProfileBtn = ttk.Button(master=editFrame, text="New profile")
        newProfileBtn.pack(side="left", fill="x", expand=1, padx=5)

        editProfileBtn = ttk.Button(master=editFrame, text="Edit profile")
        editProfileBtn.pack(side="left", fill="x", expand=1, padx=5)


        # packing profile frame
        self.__profileFrame.pack(side="left", padx=8)

        


        playButtonFrame = ttk.Frame(master=self.__bottomFrame)
        playButtonFrame.grid_rowconfigure(0, weight=1)
        playButtonFrame.grid_rowconfigure(1, weight=1)
        playButtonFrame.grid_rowconfigure(2, weight=1)
        playButton = Tk.Button(master=playButtonFrame, text="Play", width=30, height=3, command=self.play)
        playButton.grid(column=0, row=1)
        # playButton.grid(column=1, row=0)

        accountFastInfo = ttk.Frame(master=self.__bottomFrame)

        ttk.Label(master=accountFastInfo, text="Welcome back, SUS!").pack(side="top", pady=1)
        ttk.Label(master=accountFastInfo, text="new version is out!").pack(side="top", pady=1)
        ttk.Button(master=accountFastInfo, text="switch User").pack(side="top", pady=2)


        # accountFastInfo.grid(column=2, row=0, sticky="W")
        # accountFastInfo.grid_columnconfigure(0,weight=1)
        accountFastInfo.pack(side="right", padx=8)


        playButtonFrame.pack(side="top",fill="y", expand=1)


        self.__bottomFrame.pack(side="bottom", fill="x", expand=0)
        
        with open("data/logs/latest.log", "r") as f:
            content = f.read()
            self.__gameLogs.config(state="normal")
            self.__gameLogs.delete(0.0, Tk.END)
            self.__gameLogs.insert(0.0, content)
            self.__gameLogs.config(state="disabled")
            self.__gameLogs.see(Tk.END)
            self.__Logs_previousContent = content
        
        self.__root.bind("<Destroy>", self.stopLauncherEvent)

        asyncio.run(self.__loopEvent())      
        # self.__logUpdaterThread = Timer(0.1, self.__logUpdater)
        # self.__logUpdaterThread.daemon = True
        # self.__logUpdaterThread.start()
        
        # self.__loopEvent()



if __name__ == "__main__":
    Launcher()