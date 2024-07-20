# external imports
import tkinter as Tk
from tkinter import ttk
from tkinter import messagebox
# import asyncio
from multiprocessing import Process
import asyncio
import os
import json
from datetime import datetime

# internal imports
import bin


def startGame(): bin.Game((1280,720))

class Launcher:
    def log(self, message: str):
        timenow = datetime.now().time().strftime("%X:%f")
        with open("data/launcherData/launcherLogsRecent.log", "a") as f:
            f.write(f"[{timenow}] -> {message}\n")
    
    async def __logUpdater(self):
        while self.__launcherRunning:
            # self.log("updating logs...")
            with open("data/logs/latest.log", "r") as f:
                content = f.read()
                if content != self.__Logs_previousContent:
                    self.__gameLogs.config(state="normal")
                    self.__gameLogs.delete(0.0, Tk.END)
                    self.__gameLogs.insert(0.0, content)
                    self.__gameLogs.config(state="disabled")
                    self.__gameLogs.see(Tk.END)
                    self.__Logs_previousContent = content
                
            with open("data/launcherData/launcherLogsRecent.log", "r") as f:
                content = f.read()
                if content != self.__LogsLauncher_previousContent:
                    self.__launcherLogs.config(state="normal")
                    self.__launcherLogs.delete(0.0, Tk.END)
                    self.__launcherLogs.insert(0.0, content)
                    self.__launcherLogs.config(state="disabled")
                    self.__launcherLogs.see(Tk.END)
                    self.__LogsLauncher_previousContent = content
            # self.log("logs has been updated!")
            await asyncio.sleep(0.1)
                
    async def __loopEvent(self):
        asyncio.create_task(self.__logUpdater(), name="logUpdater")  
        while self.__launcherRunning:
            self.__root.update()
            await asyncio.sleep(0.01)
            
    def stopLauncherEvent(self, event, forced: bool = False) -> None:
        self.log("closing tkinter environment and launcher by user...")
        if event.widget == self.__root or forced == True:
            self.__launcherRunning = False
        self.log("launcher has been closed by user")
                
    
    def setIsGameOpen(self, value: bool) -> None:
        self.log("setting selecedProfile to file...")
        with open("data/isGameOpen", "w") as f:
            f.write("1" if value else "0")
            
    def getIsGameOpen(self) -> bool:
        self.log("reading selecedProfile from file...")
        with open("data/isGameOpen", "r") as f:
            return True if f.read() == "1" else False
        
    
    def setSelectedProfileFile(self, value: str, setAlsoToselected: bool = True) -> None:
        self.log("setting selecedProfile to file...")
        with open("data/launcherData/selectedProfile", "w") as f:
            f.write(value)
            
    def getSelectedProfileFile(self) -> str:
        self.log("reading selecedProfile from file...")
        with open("data/launcherData/selectedProfile", "r") as f:
            return f.read()

    
    def play(self, *args, **kwargs) -> None:
        self.log("trying to launch game...")
        gameStarted = self.getIsGameOpen()
        
        if gameStarted:
            self.log("game has been already launched before!")
            odp = messagebox.askokcancel("Warning", "A game process is already running. We can't guarantee stability of a new game instance. Do you want to play anyway?") 
            if not odp: return
        
        self.setIsGameOpen(True)
            
        self.log("game has been launched!")
        gameStarted = True
        p = Process(target=startGame)
        p.start()
        
    def updateProfileSelector(self) -> None:
        self.log("updating existing profiles to combobox (reading from file)...")
        with open("data/launcherData/profiles.json", 'r') as f:
            profileData = json.load(f)
        
        # self.__selectorProfile.option_clear()
        # print(profileData)
        
        self.__selectorProfile['values'] = [profileName for profileName, profile in profileData.items()]
        selected = self.getSelectedProfileFile()
        if selected in self.__selectorProfile['values']:  
            self.__selectorProfile.set(selected)
        else:
            self.__selectorProfile.set(list(profileData.keys())[0])
        
        self.log("updating existing profiles to combobox (reading from file)... DONE")
        # for profileName, profile in profileData.items():
        #     self.__selectorProfile['values'] = [profileName]
        # # values = list(self.__selectorProfile['values'])
        # print(values)
        
    def __selectedProfileComboChanged(self, *args, **kwargs) -> None:
        newProfile = self.__selectedProfile.get()
        
        self.log(f"profile has been changed to {newProfile}")
        self.setSelectedProfileFile(newProfile)
        
    def addProfileWindow(self, *args, **kwargs) -> None:
        self.log("creating add profile window...")
        self.__addProfileWindow = Tk.Toplevel(master=self.__root)
        self.__addProfileWindow.geometry("300x300")
        self.log("creating add profile window... DONE")
        
        
    def ensuringThatEveryFileDoExist(self) -> None:

        if not os.path.isdir("data/logs"):
            os.makedirs("data/logs")

        if not os.path.exists("data/logs/latest.log"):
            with open("data/logs/latest.log", "w") as f:
                f.write("")
                self.log("Couldn't a find file 'data/logs/latest.log'. created one.")
        
        
        if not os.path.exists("data/isGameOpen"):
            self.log("Couldn't a find file 'data/isGameOpen'. created one.")
            self.setIsGameOpen(False)
            
        if not os.path.exists("data/launcherData/profiles.json"):
            prof = {
                "vanilia": {
                    "gameVersion": "INDEV-1",
                    "gameVersionINT": 0
                },
                "debug": {
                    "gameVersion": "INDEV-1",
                    "gameVersionINT": 0
                }
            }
            with open("data/launcherData/profiles.json", "w") as f:
                json.dump(prof, f, indent=4)
            self.log("Couldn't find a file 'data/launcherData/profiles.json'. created one.")
        
        if not os.path.exists("data/launcherData/selectedProfile"):
            self.log("Couldn't find a file 'data/launcherData/selectedProfile'. created one.")
            with open("data/launcherData/selectedProfile", "w") as f:
                f.write("vanilia")
                
                
                
        
    def __init__(self) -> None:
        # # is gameOpen
        # with open("data/isGameOpen", "w") as f:
        #     f.write("0")
            
        # setproctitle.setproctitle("mc2d Launchers")

        if not os.path.isdir("data/launcherData"):
            os.makedirs("data/launcherData")
        
        with open("data/launcherData/launcherLogsRecent.log", "w") as f:
            f.write("")
        
        self.log("ensuring that every file is intact...")
        self.ensuringThatEveryFileDoExist()
        self.log("Launcher has ensured that every file that is needed to running this launcher is intact!")
        

        
        self.log("creating tkinter environment...")    
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
        self.__launcherLogsFrame = ttk.Frame(master=self.__notebookMenu)
        self.__notebookMenu.add(self.__launcherLogsFrame, text="launcher Logs")

        self.__launcherLogs = Tk.Text(master=self.__launcherLogsFrame, bg="lightgray", fg="black")
        self.__launcherLogs.pack(side="top", fill="both", expand=1)

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
        self.__selectedProfile = Tk.StringVar(master=self.__root, value="PRE-INDEV 1")
        self.__selectedProfile.trace_add("write", self.__selectedProfileComboChanged)
        self.__selectorProfile = ttk.Combobox(master=SelectorFrame, textvariable=self.__selectedProfile, width=20, state="readonly")
        self.__selectorProfile.pack(side="left")

        # edit profile
        editFrame = ttk.Frame(master=self.__profileFrame)
        editFrame.pack(side="top", fill="x", expand=1, pady=3)

        newProfileBtn = ttk.Button(master=editFrame, text="New profile", command=self.addProfileWindow)
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
        
        # first read of game recent logs
        self.log("reading latest game logs...")
        with open("data/logs/latest.log", "r") as f:
            content = f.read()
            self.__gameLogs.config(state="normal")
            self.__gameLogs.delete(0.0, Tk.END)
            self.__gameLogs.insert(0.0, content)
            self.__gameLogs.config(state="disabled")
            self.__gameLogs.see(Tk.END)
            self.__Logs_previousContent = content
        self.log("reading latest game logs... DONE")
            
        # first read of game recent logs
        self.log("reading latest launcher logs...")
        with open("data/launcherData/launcherLogsRecent.log", "r") as f:
            content = f.read()
            self.__launcherLogs.config(state="normal")
            self.__launcherLogs.delete(0.0, Tk.END)
            self.__launcherLogs.insert(0.0, content)
            self.__launcherLogs.config(state="disabled")
            self.__launcherLogs.see(Tk.END)
            self.__LogsLauncher_previousContent = content
        self.log("reading latest launcher logs... DONE")
        
        # events
        self.__root.bind("<Destroy>", self.stopLauncherEvent)
        self.log("creating tkinter environment... DONE")    
        
        # updating things from files
        self.updateProfileSelector()

        # final run
        self.log("running main event loop...")
        asyncio.run(self.__loopEvent())      
        # self.__logUpdaterThread = Timer(0.1, self.__logUpdater)
        # self.__logUpdaterThread.daemon = True
        # self.__logUpdaterThread.start()
        
        # self.__loopEvent()



if __name__ == "__main__":
    Launcher()