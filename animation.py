from tkinter import * 
from PIL import Image, ImageTk

root = Tk()
#root.geometry("1920x1080")

image1 = Image.open(r"paint_roses(low).gif")
framesTotal = image1.n_frames

play_back_delay = 150
animation = []

def loadGif():
    for x in range(framesTotal):
        frame = ImageTk.PhotoImage(image1.copy())
        animation.append(frame)
        image1.seek(x)


def update(ind):
    frame = animation[ind]
    label.configure(image=frame)
    
    ind += 1
    if ind == framesTotal:
        ind = 0

    root.after(play_back_delay, update, ind)

label = Label(root)
label.pack()
loadGif()
update(0)
root.mainloop()