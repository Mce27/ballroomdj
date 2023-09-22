import time, backend, os
from tkinter import *
from tkinter import ttk
from pygame import mixer
from PIL import Image
from PIL import ImageTk
import threading
#https://tkdocs.com/

Mfont=["Comic sans MS", 20]
PAUSED = False

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
    global PAUSED
    while mixer.music.get_busy() == True or PAUSED:
        time.sleep(1)
        pass

def playThreadedRound(style:str):
    threading.Thread(target=playRound,args=(style,)).start()

def playRound(style:str):
    if style == "all":
        for cat in backend.dances.keys():
            dances = backend.dances[cat]
            mixer.init()
            statusVar.set("Queuing music...")
            for dance in dances:
                song = os.listdir(f"music/{cat}/{dance}")
                statusVar.set(f"Playing {dance}\n{song[0][:-4]}")
                mixer.music.load(f"music/{cat}/{dance}/{song[0]}")
                mixer.music.play()
                waitDone()
                mixer.music.load("media/clapping.mp3")
                mixer.music.play()
                waitDone()
        statusVar.set("Nice Dancing!\nAwaiting input")
    else:       
        dances = backend.dances[style]
        mixer.init()
        statusVar.set("Queuing music...")
        for dance in dances:
            song = os.listdir(f"music/{style}/{dance}")
            statusVar.set(f"Playing {dance}\n{song[0][:-4]}")
            mixer.music.load(f"music/{style}/{dance}/{song[0]}")
            mixer.music.play()
            waitDone()
            mixer.music.load("media/clapping.mp3")
            mixer.music.play()
            waitDone()
        statusVar.set("Nice Dancing!\nAwaiting input")

def pauseSong():
    global PAUSED
    if mixer.music.get_busy():
        PAUSED = True
        mixer.music.pause()

def resumeSong():
    global PAUSED
    if PAUSED:
        mixer.music.unpause()
        PAUSED = False

def skipSong():
    global PAUSED #just in case the player is paused
    PAUSED = False
    mixer.music.fadeout(1000)

std_round_but = ttk.Button(frm, text="Play!", command=lambda:playThreadedRound('std')).grid(column=0,row=1)
lat_round_but = ttk.Button(frm, text="Play!", command=lambda:playThreadedRound('lat')).grid(column=1,row=1)
smo_round_but = ttk.Button(frm, text="Play!", command=lambda:playThreadedRound('smo')).grid(column=2,row=1)
rhy_round_but = ttk.Button(frm, text="Play!", command=lambda:playThreadedRound('rhy')).grid(column=3,row=1)
all_round_but = ttk.Button(frm, text="Play!", command=lambda:playThreadedRound('all')).grid(column=0,row=3)
pause_but = ttk.Button(frm, text="Pause", command=pauseSong).grid(column=0,row=4)
unpause_but = ttk.Button(frm, text="! Pause", command=resumeSong).grid(column=1,row=4)
skip_but = ttk.Button(frm, text="Skip", command=skipSong).grid(column=3,row=4)

statusVar.set("Setting up...")
backend.setup()
statusVar.set("Awaiting input")
root.mainloop()
