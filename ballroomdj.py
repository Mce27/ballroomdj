import time, backend, shutil
from tkinter.font import Font
from tkinter import *
from tkinter import ttk
from pygame import mixer
from PIL import Image
from PIL import ImageTk
from queue import Queue
import threading
from pynput.keyboard import Key, Listener, Controller
#https://tkdocs.com/

Mfont=["Comic sans MS", 20]
PAUSED = False
STOP = False
LOL = False
CLAPS = True
END_PROGRAM = False
FONT = 'monocraft'
GREENHEX = '#006400'
GREYHEX = '#808080'
STATUS_LEN = 40
THREE_DANCE = False
FOUR_DANCE = False
three_dance_excludes = ['stdfoxtrot', 'smovwaltz', 'rhymambo', 'latsamba']
four_dance_excludes = ['latpaso', 'rhybolero','stdvwaltz']

root = Tk()
TKFONT = Font(root,font=(FONT,20))

s = ttk.Style()
s.configure('.', font=(FONT, 20))

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

    if not STOP:    #in case the user starts this thread without stopping the old one
        stopShuffle()
        time.sleep(2)

    STOP = False
    PAUSED = False

    song_dict = {}

    statusVar.set("Setting up...")
    if style == "all":
        backend.round_request(style,song_dict)
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
                    title,filepath = song_dict[cat + dance]
                    if THREE_DANCE and ((cat+dance) in three_dance_excludes or (cat+dance) in four_dance_excludes):
                        continue
                    if FOUR_DANCE and (cat+dance) in four_dance_excludes:
                        continue
                    if len(title) > STATUS_LEN:
                        title = title[:STATUS_LEN] + '-\n' + title[STATUS_LEN:]
                    statusVar.set(f"Playing {dance}\n{title}")
                    mixer.music.load(filepath)
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
        backend.round_request(style,song_dict) 
        dances = backend.dances[style]
        mixer.init()
        statusVar.set("Queuing music...")
        if LOL:
                mixer.music.load("media/MK Countdown.mp3")
                mixer.music.play()
                waitDone()
        for dance in dances:
            if not STOP:
                title,filepath = song_dict[style + dance]
                if THREE_DANCE and ((style+dance) in three_dance_excludes or (style+dance) in four_dance_excludes):
                    continue
                if FOUR_DANCE and (style+dance) in four_dance_excludes:
                    continue
                if len(title) > STATUS_LEN:
                    title = title[:STATUS_LEN] + '-\n' + title[STATUS_LEN:]
                statusVar.set(f"Playing {dance}:\n{title}")
                mixer.music.load(filepath)
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

    if not STOP:    #in case the user starts this thread without stopping the old one
        stopShuffle()
        time.sleep(2)

    STOP = False
    PAUSED = False
    statusVar.set("Queuing music...")
    threading.Thread(target=getShuffleStyleSongs,args=(que,style)).start()
    while not STOP:
        title,dance,filepath = que.get()
        if len(title) > STATUS_LEN:
            title = title[:STATUS_LEN] + '-\n' + title[STATUS_LEN:]
        statusVar.set(f"Playing {dance}:\n{title}")
        mixer.music.load(filepath)
        mixer.music.play()
        waitDone()
        if not STOP and CLAPS:
            mixer.music.load("media/clapping.mp3")
            mixer.music.play()
            waitDone()
    statusVar.set("Nice Dancing!\nAwaiting input")

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

    if not STOP:    #in case the user starts this thread without stopping the old one
        stopShuffle()
        time.sleep(2)
    
    STOP = False
    PAUSED = False
    statusVar.set("Queuing music...")
    threading.Thread(target=getShuffleDanceSongs,args=(que,style,dance)).start()
    
    while not STOP:
        title,filepath = que.get()
        if len(title) > STATUS_LEN:
            title = title[:STATUS_LEN] + '-\n' + title[STATUS_LEN:]
        statusVar.set(f"Playing {dance}:\n{title}")
        mixer.music.load(filepath)
        mixer.music.play()
        waitDone()
        if not STOP and CLAPS:
            mixer.music.load("media/clapping.mp3")
            mixer.music.play()
            waitDone()
        time.sleep(1)
    statusVar.set("Nice Dancing!\nAwaiting input")

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

def pause_or_unpause_song():
    if PAUSED:
        resumeSong()
    else:
        pauseSong()

def skipSong():
    global PAUSED #just in case the player is paused
    PAUSED = False
    mixer.music.fadeout(1000)

def toggleClaps():
    global CLAPS
    global claps_but
    if CLAPS == True:
        #set to red
        claps_but['bg'] = GREYHEX
        claps_but['activebackground'] = GREYHEX
    else:
        #set to green
        claps_but['bg'] = GREENHEX
        claps_but['activebackground'] = GREENHEX
    CLAPS = not CLAPS
    

def toggleLOL():
    global LOL
    global lol_button
    if LOL == True:
        #set to red
        lol_button['bg'] = GREYHEX
        lol_button['activebackground'] = GREYHEX
    else:
        #set to green
        lol_button['bg'] = GREENHEX
        lol_button['activebackground'] = GREENHEX
    LOL = not LOL

def toggleThreeDance():
    global THREE_DANCE
    global three_dance_but
    if FOUR_DANCE:
        toggleFourDance()
    if THREE_DANCE == True:
        #set to red
        three_dance_but['bg'] = GREYHEX
        three_dance_but['activebackground'] = GREYHEX
    else:
        #set to green
        three_dance_but['bg'] = GREENHEX
        three_dance_but['activebackground'] = GREENHEX
    THREE_DANCE = not THREE_DANCE

def toggleFourDance():
    global FOUR_DANCE
    global four_dance_but
    if THREE_DANCE:
        toggleThreeDance()
    if FOUR_DANCE == True:
        #set to red
        four_dance_but['bg'] = GREYHEX
        four_dance_but['activebackground'] = GREYHEX
    else:
        #set to green
        four_dance_but['bg'] = GREENHEX
        four_dance_but['activebackground'] = GREENHEX
    FOUR_DANCE = not FOUR_DANCE

### Keyboard stuff start
def on_key_press(key):
    global END_PROGRAM
    if not END_PROGRAM:
        try:
            #print(f'Key {key} pressed')
            match key.char:
                case 'p':
                    if PAUSED:
                        resumeSong()
                    else:
                        pauseSong()
                case 's':
                    stopShuffle()
            
        except AttributeError:
            # Some special keys, like 'Key.shift', do not have a string representation
            if key == Key.right:
                skipSong()
            #print(f'Special key {key} pressed')
    else:
        return False

def start_keylogger():
    with Listener(on_press=on_key_press) as listener: # type: ignore
        listener.join()
###Keyboard stuff end

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
smo_foxtrot_shuffle_but = ttk.Button(button_frm, text="Foxtrot!", command=lambda:threadedShuffleDance('smo','foxtrot')).grid(column=2,row=3)
smo_vwaltz_shuffle_but = ttk.Button(button_frm, text="VWaltz!", command=lambda:threadedShuffleDance('smo','vwaltz')).grid(column=2,row=4)

std_label=ttk.Label(button_frm,text="Standard:",padding='10',font=FONT).grid(column=3,row=0)
std_waltz_shuffle_but = ttk.Button(button_frm, text="Waltz!", command=lambda:threadedShuffleDance('std','waltz')).grid(column=3,row=1)
std_tango_shuffle_but = ttk.Button(button_frm, text="Tango!", command=lambda:threadedShuffleDance('std','tango')).grid(column=3,row=2)
std_vwaltz_shuffle_but = ttk.Button(button_frm, text="VWaltz!", command=lambda:threadedShuffleDance('std','vwaltz')).grid(column=3,row=3)
std_foxtrot_shuffle_but = ttk.Button(button_frm, text="Foxtrot!", command=lambda:threadedShuffleDance('std','foxtrot')).grid(column=3,row=4)
std_quickstep_shuffle_but = ttk.Button(button_frm, text="Quickstep!", command=lambda:threadedShuffleDance('std','quickstep')).grid(column=3,row=5)

rhy_label=ttk.Label(button_frm,text="Rhythm:",padding='10',font=FONT).grid(column=4,row=0)
rhy_chacha_shuffle_but = ttk.Button(button_frm, text="Cha Cha!", command=lambda:threadedShuffleDance('rhy','chacha')).grid(column=4,row=1)
rhy_rumba_shuffle_but = ttk.Button(button_frm, text="Rumba!", command=lambda:threadedShuffleDance('rhy','rumba')).grid(column=4,row=2)
rhy_swing_shuffle_but = ttk.Button(button_frm, text="Swing!", command=lambda:threadedShuffleDance('rhy','swing')).grid(column=4,row=3)
rhy_bolero_shuffle_but = ttk.Button(button_frm, text="Bolero!", command=lambda:threadedShuffleDance('rhy','bolero')).grid(column=4,row=4)
rhy_mambo_shuffle_but = ttk.Button(button_frm, text="Mambo!", command=lambda:threadedShuffleDance('rhy','mambo')).grid(column=4,row=5)

lat_label=ttk.Label(button_frm,text="Latin:",padding='10',font=FONT).grid(column=5,row=0)
lat_samba_shuffle_but = ttk.Button(button_frm, text="Samba!", command=lambda:threadedShuffleDance('lat','samba')).grid(column=5,row=1)
lat_chacha_shuffle_but = ttk.Button(button_frm, text="Cha Cha!", command=lambda:threadedShuffleDance('lat','chacha')).grid(column=5,row=2)
lat_rumba_shuffle_but = ttk.Button(button_frm, text="Rumba!", command=lambda:threadedShuffleDance('lat','rumba')).grid(column=5,row=3)
lat_paso_shuffle_but = ttk.Button(button_frm, text="Paso Doble!", command=lambda:threadedShuffleDance('lat','paso')).grid(column=5,row=4)
lat_jive_shuffle_but = ttk.Button(button_frm, text="Jive!", command=lambda:threadedShuffleDance('lat','jive')).grid(column=5,row=5)


status_label = ttk.Label(frm,textvariable=statusVar,padding='10',font=FONT).grid(column=2,row=6)

if THREE_DANCE:
    three_dance_but = Button(frm,bg=GREENHEX,activebackground=GREENHEX, text="3 Dance\nRounds",font=TKFONT, command=toggleThreeDance)
else:
    three_dance_but = Button(frm,bg=GREYHEX,activebackground=GREYHEX, text="3 Dance\nRounds",font=TKFONT, command=toggleThreeDance)
three_dance_but.grid(column=0,row=5)
if FOUR_DANCE:
    four_dance_but =Button(frm,bg=GREENHEX,activebackground=GREENHEX, text="4 Dance\nRounds",font=TKFONT, command=toggleFourDance)
else:
    four_dance_but =Button(frm,bg=GREYHEX,activebackground=GREYHEX, text="4 Dance\nRounds",font=TKFONT, command=toggleFourDance)
four_dance_but.grid(column=1,row=5)

pause_but = ttk.Button(frm, text="Pause", command=pause_or_unpause_song).grid(column=0,row=6)
#unpause_but = ttk.Button(frm, text="! Pause", command=resumeSong).grid(column=1,row=6)
skip_but = ttk.Button(frm, text="Skip", command=skipSong).grid(column=0,row=7)
stop_but = ttk.Button(frm, text="Stop", command=stopShuffle).grid(column=1,row=7)
if CLAPS:
    claps_but = Button(frm,bg=GREENHEX,activebackground=GREENHEX, text="Toggle\nClaps",font=TKFONT, command=toggleClaps)
else:
    claps_but = Button(frm,bg=GREYHEX,activebackground=GREYHEX, text="Toggle\nClaps",font=TKFONT, command=toggleClaps)
claps_but.grid(column=0,row=8)
if LOL:
    lol_button = Button(frm,bg=GREENHEX,activebackground=GREENHEX, text="Toggle\nCount",font=TKFONT, command=toggleLOL)
else:
    lol_button = Button(frm,bg='#808080',activebackground='white', text="Toggle\nCount",font=TKFONT, command=toggleLOL)
lol_button.grid(column=1,row=8)

statusVar.set("Setting up...")
backend.setup()
mixer.init()
statusVar.set("Awaiting input")

keylogger_thread = threading.Thread(target=start_keylogger, daemon=True)
keylogger_thread.start()

root.mainloop()
END_PROGRAM = True

# Press escape key to make the listener close
keyboard = Controller()
print("Wrapping up...")
keyboard.press(Key.esc)
time.sleep(0.5)
keyboard.release(Key.esc)
stopShuffle()
time.sleep(1)
shutil.rmtree('music', ignore_errors=True)
