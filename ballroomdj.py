import time, backend, os, shutil
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
round_button_frm = ttk.Frame(frm,padding="20")
round_button_frm.grid(column=0,row=1)
style_button_frm = ttk.Frame(frm,padding="20")
style_button_frm.grid(column=1,row=1)
button_frm = ttk.Frame(frm,padding="20")
button_frm.grid(column=2,row=1)
statusVar = StringVar(frm)

rounds_label = ttk.Label(frm,text="Rounds:",padding='10').grid(column=0,row=0)
smo_round_but = ttk.Button(round_button_frm, text="Smooth!", command=lambda:playThreadedRound('smo')).grid(column=0,row=1)
std_round_but = ttk.Button(round_button_frm, text="Standard!", command=lambda:playThreadedRound('std')).grid(column=0,row=2)
rhy_round_but = ttk.Button(round_button_frm, text="Rhythm!", command=lambda:playThreadedRound('rhy')).grid(column=0,row=3)
lat_round_but = ttk.Button(round_button_frm, text="Latin!", command=lambda:playThreadedRound('lat')).grid(column=0,row=4)
all_round_but = ttk.Button(round_button_frm, text="All!", command=lambda:playThreadedRound('all')).grid(column=0,row=5)

shuffle_style_label = ttk.Label(frm,text="Shuffle Style:",padding='10').grid(column=1,row=0)
smo_shuffle_but = ttk.Button(style_button_frm, text="Smooth!", command=lambda:shuffleStyle('smo')).grid(column=1,row=1)
std_shuffle_but = ttk.Button(style_button_frm, text="Standard!", command=lambda:shuffleStyle('std')).grid(column=1,row=2)
rhy_shuffle_but = ttk.Button(style_button_frm, text="Rhythm!", command=lambda:shuffleStyle('rhy')).grid(column=1,row=3)
lat_shuffle_but = ttk.Button(style_button_frm, text="Latin!", command=lambda:shuffleStyle('lat')).grid(column=1,row=4)
all_shuffle_but = ttk.Button(style_button_frm, text="All!", command=lambda:shuffleStyle('all')).grid(column=1,row=5)

shuffle_dance_label = ttk.Label(frm,text="Shuffle Dance:",padding='10').grid(column=2,row=0)
smo_waltz_shuffle_but = ttk.Button(button_frm, text="Waltz!", command=lambda:shuffleDance('smo','waltz')).grid(column=2,row=1)
smo_tango_shuffle_but = ttk.Button(button_frm, text="Tango!", command=lambda:shuffleDance('smo','tango')).grid(column=2,row=2)
smo_vwaltz_shuffle_but = ttk.Button(button_frm, text="VWaltz!", command=lambda:shuffleDance('smo','vwaltz')).grid(column=2,row=3)
smo_foxtrot_shuffle_but = ttk.Button(button_frm, text="Foxtrot!", command=lambda:shuffleDance('smo','foxtrot')).grid(column=2,row=4)

std_waltz_shuffle_but = ttk.Button(button_frm, text="Waltz!", command=lambda:shuffleDance('std','waltz')).grid(column=3,row=1)
std_tango_shuffle_but = ttk.Button(button_frm, text="Tango!", command=lambda:shuffleDance('std','tango')).grid(column=3,row=2)
std_vwaltz_shuffle_but = ttk.Button(button_frm, text="VWaltz!", command=lambda:shuffleDance('std','vwaltz')).grid(column=3,row=3)
std_foxtrot_shuffle_but = ttk.Button(button_frm, text="Foxtrot!", command=lambda:shuffleDance('std','foxtrot')).grid(column=3,row=4)
std_quickstep_shuffle_but = ttk.Button(button_frm, text="Quickstep!", command=lambda:shuffleDance('std','quickstep')).grid(column=3,row=5)

rhy_chacha_shuffle_but = ttk.Button(button_frm, text="Chacha!", command=lambda:shuffleDance('rhy','chacha')).grid(column=4,row=1)
rhy_rumba_shuffle_but = ttk.Button(button_frm, text="Rumba!", command=lambda:shuffleDance('rhy','rumba')).grid(column=4,row=2)
rhy_swing_shuffle_but = ttk.Button(button_frm, text="Swing!", command=lambda:shuffleDance('rhy','swing')).grid(column=4,row=3)
rhy_bolero_shuffle_but = ttk.Button(button_frm, text="Bolero!", command=lambda:shuffleDance('rhy','bolero')).grid(column=4,row=4)
rhy_mambo_shuffle_but = ttk.Button(button_frm, text="Mambo!", command=lambda:shuffleDance('rhy','mambo')).grid(column=4,row=5)

lat_chacha_shuffle_but = ttk.Button(button_frm, text="Chacha!", command=lambda:shuffleDance('lat','chacha')).grid(column=5,row=1)
lat_rumba_shuffle_but = ttk.Button(button_frm, text="Rumba!", command=lambda:shuffleDance('lat','rumba')).grid(column=5,row=2)
lat_samba_shuffle_but = ttk.Button(button_frm, text="Samba!", command=lambda:shuffleDance('lat','samba')).grid(column=5,row=3)
lat_jive_shuffle_but = ttk.Button(button_frm, text="Jive!", command=lambda:shuffleDance('lat','jive')).grid(column=5,row=4)

"""
status_label = ttk.Label(frm,textvariable=statusVar,padding='10').grid(column=1,row=2)
pause_but = ttk.Button(frm, text="Pause", command=pauseSong).grid(column=0,row=4)
unpause_but = ttk.Button(frm, text="! Pause", command=resumeSong).grid(column=1,row=4)
skip_but = ttk.Button(frm, text="Skip", command=skipSong).grid(column=3,row=4)
"""

def playSong():
    filepath = ''
    mixer.init()
    mixer.music.load(filepath)
    mixer.music.play()


def waitDone():
    global PAUSED
    while mixer.music.get_busy() == True or PAUSED:
        #print(mixer.music.get_pos()/1000)
        if (mixer.music.get_pos()/1000) > 90:   #fades out song after 1.5 minutes
            mixer.music.fadeout(1000)
        time.sleep(1)
        pass

def playThreadedRound(style:str):
    threading.Thread(target=playRound,args=(style,)).start()

def playRound(style:str):
    global PAUSED
    if style == "all":
        for cat in backend.dances.keys():
            while PAUSED:
                time.sleep(1)
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
            pauseSong() #pause between styles requested by James
            statusVar.set("Press '! Pause' to continue!")
        statusVar.set("Nice Dancing!\nAwaiting input")
    else:       
        dances = backend.dances[style]
        mixer.init()
        statusVar.set("Queuing music...")
        for dance in dances:
            song = os.listdir(f"music/{style}/{dance}")
            title = song[0][:-4]
            if len(title) > 20:
                title = title[:20] + '-\n' + title[20:]
            statusVar.set(f"Playing {dance}:\n{title}")
            mixer.music.load(f"music/{style}/{dance}/{song[0]}")
            mixer.music.play()
            waitDone()
            mixer.music.load("media/clapping.mp3")
            mixer.music.play()
            waitDone()
        statusVar.set("Nice Dancing!\nAwaiting input")

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



statusVar.set("Setting up...")
#backend.setup()
statusVar.set("Awaiting input")
root.mainloop()
shutil.rmtree('music', ignore_errors=True)
