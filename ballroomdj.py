import time, backend, os
from tkinter import *
from tkinter import ttk
from pygame import mixer
from PIL import Image
from PIL import ImageTk
#https://tkdocs.com/

Mfont=["Comic sans MS", 20]

root = Tk()

#Sets the title and the icon
root.title("Ballroom DJ!")
ico = Image.open('media/imgs/logo.ico') #Your icon here
photo = ImageTk.PhotoImage(ico)
root.wm_iconphoto(False, photo)

root.grid()
frm = ttk.Frame(root,padding="20")
frm.grid(column=0,row=0)
statusVar = StringVar(frm)
std_round_label = ttk.Label(frm,text="Run a std round",padding='10').grid(column=0,row=0)
lat_round_label = ttk.Label(frm,text="Run a lat round",padding='10').grid(column=1,row=0)
smo_round_label = ttk.Label(frm,text="Run a smo round",padding='10').grid(column=2,row=0)
rhy_round_label = ttk.Label(frm,text="Run a rhy round",padding='10').grid(column=3,row=0)
all_round_label = ttk.Label(frm,text="Run all the rounds!",padding='10').grid(column=0,row=2)
status_label = ttk.Label(frm,textvariable=statusVar,padding='10').grid(column=1,row=2)
  

def playSong():
    filepath = ''
    mixer.init()
    mixer.music.load(filepath)
    mixer.music.play()

def waitDone():
    while mixer.music.get_busy() == True:
        pass

def playRound(style:str):
    if style == "all":
        for cat in backend.dances.keys():
            dances = backend.dances[cat]
            mixer.init()
            statusVar.set("Queuing music...")
            for dance in dances:
                song = os.listdir(f"music/{cat}/{dance}")
                mixer.music.load(f"music/{cat}/{dance}/{song[0]}")
                mixer.music.play()
                mixer.music.queue("media/clapping.mp3")
                statusVar.set(f"Playing {dance}\n{song[0][:-4]}")
                waitDone()
        statusVar.set("Nice Dancing!\nAwaiting input")
    else:       
        dances = backend.dances[style]
        mixer.init()
        statusVar.set("Queuing music...")
        for dance in dances:
            song = os.listdir(f"music/{style}/{dance}")
            mixer.music.load(f"music/{style}/{dance}/{song[0]}")
            mixer.music.play()
            mixer.music.queue("media/clapping.mp3")
            statusVar.set(f"Playing {dance}\n{song[0][:-4]}")
            waitDone()
        statusVar.set("Nice Dancing!\nAwaiting input")

std_round_but = ttk.Button(frm, text="Play!", command=lambda:playRound('std')).grid(column=0,row=1)
lat_round_but = ttk.Button(frm, text="Play!", command=lambda:playRound('lat')).grid(column=1,row=1)
smo_round_but = ttk.Button(frm, text="Play!", command=lambda:playRound('smo')).grid(column=2,row=1)
rhy_round_but = ttk.Button(frm, text="Play!", command=lambda:playRound('rhy')).grid(column=3,row=1)
all_round_but = ttk.Button(frm, text="not implemented", command=lambda:playRound('all')).grid(column=0,row=3)
#lab.pack()
#but.pack()

statusVar.set("Setting up...")
backend.setup()
statusVar.set("Awaiting input")
root.mainloop()
