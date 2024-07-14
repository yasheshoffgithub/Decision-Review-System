import tkinter
import PIL.Image, PIL.ImageTk
import cv2
from functools import partial
import threading
import time
import imutils

stream=cv2.VideoCapture("clip.mp4")
flag=True
def play(speed):
    global flag
    print(f"You clicked on play. Speed is {speed}")
    
    frame1=stream.get(cv2.CAP_PROP_POS_FRAMES)
    stream.set(cv2.CAP_PROP_POS_FRAMES,frame1+speed)
    grabbed,frame=stream.read()
    if not grabbed:
        exit()
    frame=imutils.resize(frame,width=SET_WIDTH,height=SET_HEIGHT)
    frame=PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    CANVAS.image=frame
    CANVAS.create_image(0,0,image=frame,anchor=tkinter.NW)
    if flag:
        CANVAS.create_text(130,30,fill="black",font="Times 25 bold",text="Decision Pending")
    else:
        flag=not flag
def pending(decision):
    # 1. Display decision pending image
    frame=cv2.cvtColor(cv2.imread("pending.png"),cv2.COLOR_BGR2RGB)
    frame=imutils.resize(frame,width=SET_WIDTH,height=SET_HEIGHT)
    frame=PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    CANVAS.image=frame
    CANVAS.create_image(0,0,image=frame,anchor=tkinter.NW)
    # 2. Wait for 1 sec
    time.sleep(1)
    # 3. Display sponsor image
    frame=cv2.cvtColor(cv2.imread("sponsor.png"),cv2.COLOR_BGR2RGB)
    frame=imutils.resize(frame,width=SET_WIDTH,height=SET_HEIGHT)
    frame=PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    CANVAS.image=frame
    CANVAS.create_image(0,0,image=frame,anchor=tkinter.NW)
    # 4. Wait for 1.5 sec
    time.sleep(1.5)
    # 5. Display out/notout image
    if decision=='out':
        decisionImg="out.png"
    else:
        decisionImg="Notout.png"   
    frame=cv2.cvtColor(cv2.imread(decisionImg),cv2.COLOR_BGR2RGB)
    frame=imutils.resize(frame,width=SET_WIDTH,height=SET_HEIGHT)
    frame=PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    CANVAS.image=frame
    CANVAS.create_image(0,0,image=frame,anchor=tkinter.NW)     
def out():
    thread=threading.Thread(target=pending,args=("out",))
    thread.daemon=1
    thread.start()
    print("Player is out")


def notout():
    thread=threading.Thread(target=pending,args=("not out",))
    thread.daemon=1
    thread.start()
    print("Player is Notout")

SET_WIDTH=650
SET_HEIGHT=368

window=tkinter.Tk()
window.title("DRS")
cv_img=cv2.cvtColor(cv2.imread("welcome.png"),cv2.COLOR_BGR2RGB)
cv_img=imutils.resize(cv_img,width=SET_WIDTH,height=SET_HEIGHT)
CANVAS=tkinter.Canvas(window,width=SET_WIDTH,height=SET_HEIGHT)
photo=PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))
image_on_canvas=CANVAS.create_image(0,0,anchor=tkinter.NW,image=photo)
CANVAS.pack()

#buttons to control playback
btn=tkinter.Button(window,text="<<Previous(fast)",width=50,command=partial
                   (play,-25))
btn.pack()

btn=tkinter.Button(window,text="<<Previous(slow)",width=50,command=partial
                   (play,-2))
btn.pack()

btn=tkinter.Button(window,text="Next(slow)>>",width=50,command=partial
                   (play,2))
btn.pack()

btn=tkinter.Button(window,text="Next(fast)>>",width=50,command=partial
                   (play,25))
btn.pack()

btn=tkinter.Button(window,text="Give Out",width=50,command=out)
btn.pack()

btn=tkinter.Button(window,text="Give Not Out",width=50,command=notout)
btn.pack()

window.mainloop()