import time, backend, os, shutil
from tkinter import *
from tkinter import ttk
from pygame import mixer
from PIL import Image
from PIL import ImageTk
from queue import Queue
import threading
#https://tkdocs.com/

Mfont=["Comic sans MS", 20]
PAUSED = False
STOP = False
LOL = True
CLAPS = TRUE
FONT = 'monocraft'

root = Tk()

#Sets the title and the icon
root.title("Ballroom DJ!")
ico = Image.open('media/imgs/logo.ico') #Your icon here
photo = ImageTk.PhotoImage(ico)
root.wm_iconphoto(False, photo)

root.grid()
frm = ttk.Frame(root,padding="20")
frm.grid(column=0,row=0)
round_button_frm = ttk.Frame(frm,padding="20")
round_button_frm.grid(column=0,row=1)
style_button_frm = ttk.Frame(frm,padding="20")
style_button_frm.grid(column=1,row=1)
button_frm = ttk.Frame(frm,padding="20")
button_frm.grid(column=2,row=1)

statusVar = StringVar(frm)


def playSong():
    filepath = ''
    mixer.init()
    mixer.music.load(filepath)
    mixer.music.play()


def waitDone():
    global PAUSED
    global STOP
    while (mixer.music.get_busy() == True or PAUSED) and not STOP:
        #print(mixer.music.get_pos()/1000)
        if (mixer.music.get_pos()/1000) > 90:   #fades out song after 1.5 minutes
            mixer.music.fadeout(1000)
        time.sleep(1)
        pass

def playThreadedRound(style:str):
    threading.Thread(target=playRound,args=(style,)).start()

def playRound(style:str):
    global PAUSED
    global STOP
    global LOL
    global CLAPS
    STOP = False
    PAUSED = False
    statusVar.set("Setting up...")
    if style == "all":
        backend.round_request(style)
        for cat in backend.dances.keys():
            while PAUSED:
                time.sleep(1)
            dances = backend.dances[cat]
            mixer.init()
            statusVar.set("Queuing music...")
            if LOL:
                mixer.music.load("media/MK Countdown.mp3")
                mixer.music.play()
                waitDone()
            for dance in dances:
                if not STOP:
                    song = os.listdir(f"music/{cat}/{dance}")
                    statusVar.set(f"Playing {dance}\n{song[0][:-4]}")
                    mixer.music.load(f"music/{cat}/{dance}/{song[0]}")
                    mixer.music.play()
                    waitDone()
                    if not STOP and CLAPS:
                        mixer.music.load("media/clapping.mp3")
                        mixer.music.play()
                        waitDone()
            if not STOP:
                pauseSong() #pause between styles requested by James
                statusVar.set("Press '! Pause' to continue!")
        statusVar.set("Nice Dancing!\nAwaiting input")
    else:      
        backend.round_request(style) 
        dances = backend.dances[style]
        mixer.init()
        statusVar.set("Queuing music...")
        if LOL:
                mixer.music.load("media/MK Countdown.mp3")
                mixer.music.play()
                waitDone()
        for dance in dances:
            if not STOP:
                song = os.listdir(f"music/{style}/{dance}")
                title = song[0][:-4]
                if len(title) > 20:
                    title = title[:20] + '-\n' + title[20:]
                statusVar.set(f"Playing {dance}:\n{title}")
                mixer.music.load(f"music/{style}/{dance}/{song[0]}")
                mixer.music.play()
                waitDone()
                if not STOP and CLAPS:
                    mixer.music.load("media/clapping.mp3")
                    mixer.music.play()
                    waitDone()
        statusVar.set("Nice Dancing!\nAwaiting input")

def getShuffleStyleSongs(que:Queue,style:str):
    while not STOP:
        while not que.full():
            filepath,dance,title = backend.get_random_style_song(style)
            que.put((title,dance,filepath))

def shuffleStyle(style:str):
    """
    Plays a continuous stream of music of the specific style, in random order
    """
    global STOP
    global PAUSED
    que = Queue()
    que.maxsize = 3
    STOP = False
    PAUSED = False
    statusVar.set("Queuing music...")
    threading.Thread(target=getShuffleStyleSongs,args=(que,style)).start()
    while not STOP:
        title,dance,filepath = que.get()
        if len(title) > 20:
            title = title[:20] + '-\n' + title[20:]
        statusVar.set(f"Playing {dance}:\n{title}")
        mixer.music.load(filepath)
        mixer.music.play()
        waitDone()
        if not STOP and CLAPS:
            mixer.music.load("media/clapping.mp3")
            mixer.music.play()
            waitDone()

def threadedShuffleStyle(style:str):
    threading.Thread(target=shuffleStyle,args=(style,)).start()

def getShuffleDanceSongs(que:Queue,style:str,dance:str):
    while not STOP:
        while not que.full() :
            filepath,title = backend.get_random_dance_song(style,dance)
            que.put((title,filepath))

def shuffleDance(style:str,dance:str):  
    """
    Plays a continuous stream of music of the specific style and dance, in random order
    """ 
    global STOP
    global PAUSED
    que = Queue()
    que.maxsize = 3
    STOP = False
    PAUSED = False
    statusVar.set("Queuing music...")
    threading.Thread(target=getShuffleDanceSongs,args=(que,style,dance)).start()
    
    while not STOP:
        title,filepath = que.get()
        if len(title) > 20:
            title = title[:20] + '-\n' + title[20:]
        statusVar.set(f"Playing {dance}:\n{title}")
        mixer.music.load(filepath)
        mixer.music.play()
        waitDone()
        if not STOP and CLAPS:
            mixer.music.load("media/clapping.mp3")
            mixer.music.play()
            waitDone()
        time.sleep(1)

def threadedShuffleDance(style:str,dance:str):
    threading.Thread(target=shuffleDance,args=(style,dance)).start()

def stopShuffle():
    global STOP
    STOP = True
    pauseSong()
    mixer.music.unload()

def pauseSong():
    global PAUSED
    """if mixer.music.get_busy():"""
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

def toggleClaps():
    global CLAPS
    CLAPS = not CLAPS

def toggleLOL():
    global LOL
    LOL = not LOL

rounds_label = ttk.Label(frm,text="Rounds:",padding='10',font=FONT).grid(column=0,row=0)
smo_round_but = ttk.Button(round_button_frm, text="Smooth!", command=lambda:playThreadedRound('smo')).grid(column=0,row=1)
std_round_but = ttk.Button(round_button_frm, text="Standard!", command=lambda:playThreadedRound('std')).grid(column=0,row=2)
rhy_round_but = ttk.Button(round_button_frm, text="Rhythm!", command=lambda:playThreadedRound('rhy')).grid(column=0,row=3)
lat_round_but = ttk.Button(round_button_frm, text="Latin!", command=lambda:playThreadedRound('lat')).grid(column=0,row=4)
all_round_but = ttk.Button(round_button_frm, text="All!", command=lambda:playThreadedRound('all')).grid(column=0,row=5)

shuffle_style_label = ttk.Label(frm,text="Shuffle Style:",padding='10',font=FONT).grid(column=1,row=0)
smo_shuffle_but = ttk.Button(style_button_frm, text="Smooth!", command=lambda:threadedShuffleStyle('smo')).grid(column=1,row=1)
std_shuffle_but = ttk.Button(style_button_frm, text="Standard!", command=lambda:threadedShuffleStyle('std')).grid(column=1,row=2)
rhy_shuffle_but = ttk.Button(style_button_frm, text="Rhythm!", command=lambda:threadedShuffleStyle('rhy')).grid(column=1,row=3)
lat_shuffle_but = ttk.Button(style_button_frm, text="Latin!", command=lambda:threadedShuffleStyle('lat')).grid(column=1,row=4)
all_shuffle_but = ttk.Button(style_button_frm, text="All!", command=lambda:threadedShuffleStyle('all')).grid(column=1,row=5)

shuffle_dance_label = ttk.Label(frm,text="Shuffle Dance:",padding='10',font=FONT).grid(column=2,row=0)
smo_label=ttk.Label(button_frm,text="Smooth:",padding='10',font=FONT).grid(column=2,row=0)
smo_waltz_shuffle_but = ttk.Button(button_frm, text="Waltz!", command=lambda:threadedShuffleDance('smo','waltz')).grid(column=2,row=1)
smo_tango_shuffle_but = ttk.Button(button_frm, text="Tango!", command=lambda:threadedShuffleDance('smo','tango')).grid(column=2,row=2)
smo_vwaltz_shuffle_but = ttk.Button(button_frm, text="VWaltz!", command=lambda:threadedShuffleDance('smo','vwaltz')).grid(column=2,row=3)
smo_foxtrot_shuffle_but = ttk.Button(button_frm, text="Foxtrot!", command=lambda:threadedShuffleDance('smo','foxtrot')).grid(column=2,row=4)

std_label=ttk.Label(button_frm,text="Standard:",padding='10',font=FONT).grid(column=3,row=0)
std_waltz_shuffle_but = ttk.Button(button_frm, text="Waltz!", command=lambda:threadedShuffleDance('std','waltz')).grid(column=3,row=1)
std_tango_shuffle_but = ttk.Button(button_frm, text="Tango!", command=lambda:threadedShuffleDance('std','tango')).grid(column=3,row=2)
std_vwaltz_shuffle_but = ttk.Button(button_frm, text="VWaltz!", command=lambda:threadedShuffleDance('std','vwaltz')).grid(column=3,row=3)
std_foxtrot_shuffle_but = ttk.Button(button_frm, text="Foxtrot!", command=lambda:threadedShuffleDance('std','foxtrot')).grid(column=3,row=4)
std_quickstep_shuffle_but = ttk.Button(button_frm, text="Quickstep!", command=lambda:threadedShuffleDance('std','quickstep')).grid(column=3,row=5)

rhy_label=ttk.Label(button_frm,text="Rhythm:",padding='10',font=FONT).grid(column=4,row=0)
rhy_chacha_shuffle_but = ttk.Button(button_frm, text="Cha cha!", command=lambda:threadedShuffleDance('rhy','chacha')).grid(column=4,row=1)
rhy_rumba_shuffle_but = ttk.Button(button_frm, text="Rumba!", command=lambda:threadedShuffleDance('rhy','rumba')).grid(column=4,row=2)
rhy_swing_shuffle_but = ttk.Button(button_frm, text="Swing!", command=lambda:threadedShuffleDance('rhy','swing')).grid(column=4,row=3)
rhy_bolero_shuffle_but = ttk.Button(button_frm, text="Bolero!", command=lambda:threadedShuffleDance('rhy','bolero')).grid(column=4,row=4)
rhy_mambo_shuffle_but = ttk.Button(button_frm, text="Mambo!", command=lambda:threadedShuffleDance('rhy','mambo')).grid(column=4,row=5)

lat_label=ttk.Label(button_frm,text="Latin:",padding='10',font=FONT).grid(column=5,row=0)
lat_chacha_shuffle_but = ttk.Button(button_frm, text="Cha cha!", command=lambda:threadedShuffleDance('lat','chacha')).grid(column=5,row=1)
lat_rumba_shuffle_but = ttk.Button(button_frm, text="Rumba!", command=lambda:threadedShuffleDance('lat','rumba')).grid(column=5,row=2)
lat_samba_shuffle_but = ttk.Button(button_frm, text="Samba!", command=lambda:threadedShuffleDance('lat','samba')).grid(column=5,row=3)
lat_jive_shuffle_but = ttk.Button(button_frm, text="Jive!", command=lambda:threadedShuffleDance('lat','jive')).grid(column=5,row=4)
lat_paso_shuffle_but = ttk.Button(button_frm, text="Paso Doble!", command=lambda:threadedShuffleDance('lat','paso')).grid(column=5,row=5)


status_label = ttk.Label(frm,textvariable=statusVar,padding='10',font=FONT).grid(column=3,row=6)
pause_but = ttk.Button(frm, text="Pause", command=pauseSong).grid(column=0,row=6)
unpause_but = ttk.Button(frm, text="! Pause", command=resumeSong).grid(column=1,row=6)
skip_but = ttk.Button(frm, text="Skip", command=skipSong).grid(column=0,row=7)
stop_but = ttk.Button(frm, text="Stop", command=stopShuffle).grid(column=1,row=7)
claps_but = ttk.Button(frm, text="Toggle\nClaps", command=toggleClaps).grid(column=0,row=8)
lol_button = ttk.Button(frm, text="Toggle\nCount", command=toggleLOL).grid(column=1,row=8)

statusVar.set("Setting up...")
backend.setup()
mixer.init()
statusVar.set("Awaiting input")
root.mainloop()
stopShuffle()
shutil.rmtree('music', ignore_errors=True)
