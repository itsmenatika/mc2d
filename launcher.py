import tkinter as Tk
from tkinter import ttk


root = Tk.Tk()
root.title("mc2d Launcher")
root.geometry("854x480")
root.configure()

# TopFrame = Tk.Frame(master=root)


# TopFrame.pack(side='top')




# notebook

notebook = ttk.Notebook(master=root)

# updates
updates = Tk.Frame(master=notebook, bg="gray")
notebook.add(updates, text="Update Notes")

#  launcher logs
launcherLogs = ttk.Frame(master=notebook)
notebook.add(launcherLogs, text="Launcher logs")


#  game logs
gameLogs = ttk.Frame(master=notebook)
notebook.add(gameLogs, text="Recent game logs")

logs = Tk.Text(master=gameLogs, bg="lightgray", fg="black")
logs.pack(side="top", fill="both", expand=1)


with open("data/logs/latest.log", "r+") as f:
    content = f.read()
    logs.insert(0.0, content)
    # logs.add(Tk.END, f.readline())
# logs.insert(Tk.END, 'swawa')
# logs.set
logs.config(state="disabled")
# logs.configure(text=lines)
# controls = 

# ttk.Label(master=gameLogs, text="Recent game logs")


#  account
account = ttk.Frame(master=root)
notebook.add(account, text="Account and launcher Settings")


# final notebook
notebook.pack(side="top", expand=1, fill="both")




# bottom

bottom = ttk.Frame(master=root)


ProfileFrame = ttk.Frame(master=bottom)

SelectorFrame = ttk.Frame(master=ProfileFrame)
SelectorFrame.pack(side="top", pady=3)

ttk.Label(master=SelectorFrame,text="Profile:  ").pack(side="left")
selectedProfile = Tk.StringVar(master=root, value="PRE-INDEV 1")
selectorProfile = ttk.Combobox(master=SelectorFrame, textvariable=selectedProfile, width=20)
selectorProfile.pack(side="left")

editFrame = ttk.Frame(master=ProfileFrame)
editFrame.pack(side="top", fill="x", expand=1, pady=3)

newProfileBtn = ttk.Button(master=editFrame, text="New profile")
newProfileBtn.pack(side="left", fill="x", expand=1, padx=5)

editProfileBtn = ttk.Button(master=editFrame, text="Edit profile")
editProfileBtn.pack(side="left", fill="x", expand=1, padx=5)



# ProfileFrame.grid(column=0, row=0, sticky="E")
# ProfileFrame.grid_columnconfigure(0,weight=1)
ProfileFrame.pack(side="left", padx=8)


playButtonFrame = ttk.Frame(master=bottom)
playButtonFrame.grid_rowconfigure(0, weight=1)
playButtonFrame.grid_rowconfigure(1, weight=1)
playButtonFrame.grid_rowconfigure(2, weight=1)
playButton = Tk.Button(master=playButtonFrame, text="Play", width=30, height=3)
playButton.grid(column=0, row=1)
# playButton.grid(column=1, row=0)

accountFastInfo = ttk.Frame(master=bottom)

ttk.Label(master=accountFastInfo, text="Welcome back, SUS!").pack(side="top", pady=1)
ttk.Label(master=accountFastInfo, text="new version is out!").pack(side="top", pady=1)
ttk.Button(master=accountFastInfo, text="switch User").pack(side="top", pady=2)


# accountFastInfo.grid(column=2, row=0, sticky="W")
# accountFastInfo.grid_columnconfigure(0,weight=1)
accountFastInfo.pack(side="right", padx=8)


playButtonFrame.pack(side="bottom",fill="y", expand=1)


bottom.pack(side="bottom", fill="x", expand=0)


root.mainloop()