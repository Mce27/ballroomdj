from tkinter import *
from tkinter import ttk
import backend
import playsound
api_link='http://navidrome.mce27.xyz/rest/download?id=8e59a33e095d62fcf3671477f8c760c6&u=mce27&t=e122d5bb2a94badb87dd8df90de1873f&s=d54g6h&v=1.12.0&c=myapp'

Mfont=["Comic sans MS", 20]

root = Tk()
root.grid()
frm = ttk.Frame(root,padding="20")
frm.grid(column=0,row=0)
textVar = 'Press the button!'
lab=ttk.Label(frm,text=textVar)


def playSong():
    filepath = backend.api_request(api_link)
    playsound.playsound(filepath)

but=ttk.Button(frm, text="Play!", command=playSong)
lab.pack()
but.pack()

root.mainloop()