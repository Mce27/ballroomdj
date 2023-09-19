import time, backend, os
from tkinter import *
from tkinter import ttk
from pygame import mixer
from PIL import Image
from PIL import ImageTk
#https://tkdocs.com/
dances = {"Standard":["watlz","tango","vwaltz","foxtrot","quickstep"],
              "Latin":["chacha","rumba","samba","jive"],
              "Smooth":["waltz","tango","vwaltz","foxtrot"],
              "Rhythm":["chacha","rumba","swing","bolero","mambo"]
              }
api_link='http://ballroom.mce27.xyz/rest/stream?id=5a8524f33621b876715bb7160289917c&u=ballroom&t=ow130p2&s=ow130p2&v=1.12.0&c=myapp'

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
lab=ttk.Label(frm,text=textVar)

def setup():
    """
    builds media file structure and dls music from server
    """
    print("Setting up!\n")
    if not os.path.exists('music'):#means no fs is there
        os.mkdir('music')
        for cat in dances.keys():
            os.mkdir(f'music/{cat}')
            for dance in dances[cat]:
                os.mkdir(f'music/{cat}/{dance}')
    else:#check if rest of fs is there
        for cat in dances.keys():
            if not os.path.exists(f'music/{cat}'):
                os.mkdir(f'music/{cat}')
                for dance in dances[cat]:
                    os.mkdir(f'music/{cat}/{dance}')
            else:
                for dance in dances[cat]:#see if dir for each dance exists
                    if not os.path.exists(f'music/{cat}/{dance}'):
                        os.mkdir(f'music/{cat}/{dance}')
    #now that fs is in place, time to dl music
    

def playSong():
    start = time.time()
    filepath = backend.api_request(api_link)
    mixer.init()
    mixer.music.load(filepath)
    mixer.music.play()
    end = time.time()
    print('Recieved file in '+str(end-start)+' seconds')

but=ttk.Button(frm, text="Play!", command=playSong)
lab.pack()
but.pack()

root.mainloop()