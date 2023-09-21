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
ico = Image.open('imgs/logo.ico')
photo = ImageTk.PhotoImage(ico)
root.wm_iconphoto(False, photo)

root.grid()
frm = ttk.Frame(root,padding="20")
frm.grid(column=0,row=0)
textVar = 'Press the button!'
std_round_label = ttk.Label(frm,text="Run a std round",padding='10').grid(column=0,row=0)
lat_round_label = ttk.Label(frm,text="Run a lat round",padding='10').grid(column=1,row=0)
smo_round_label = ttk.Label(frm,text="Run a smo round",padding='10').grid(column=2,row=0)
rhy_round_label = ttk.Label(frm,text="Run a rhy round",padding='10').grid(column=3,row=0)
all_round_label = ttk.Label(frm,text="Run all the rounds!",padding='10').grid(column=0,row=2)
  

def playSong():
    start = time.time()
    filepath = ''
    mixer.init()
    mixer.music.load(filepath)
    mixer.music.play()
    end = time.time()
    print('Recieved file in '+str(end-start)+' seconds')

std_round_but = ttk.Button(frm, text="Play!", command=playSong).grid(column=0,row=1)
lat_round_but = ttk.Button(frm, text="Play!", command=playSong).grid(column=1,row=1)
smo_round_but = ttk.Button(frm, text="Play!", command=playSong).grid(column=2,row=1)
rhy_round_but = ttk.Button(frm, text="Play!", command=playSong).grid(column=3,row=1)
all_round_but = ttk.Button(frm, text="Play!", command=playSong).grid(column=0,row=3)
#lab.pack()
#but.pack()

root.mainloop()