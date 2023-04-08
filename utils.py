from tkinter import Tk, font, Label, Frame, Canvas, Scrollbar
root = Tk()

frame = Frame(root)
frame.pack(fill='both', expand=True)


rCanvas = Canvas(frame)

rCanvas.pack(side='left', fill='both', expand=True)


scrollBar = Scrollbar(frame,command=rCanvas.yview)
scrollBar.pack(side='right', fill='y')


rCanvas.configure(yscrollcommand=scrollBar.set)

sFrame = Frame(master=rCanvas)
sFrame.bind("<Configure>", lambda e: rCanvas.configure(scrollregion=rCanvas.bbox("all")))

rCanvas.create_window((0,0), window=sFrame,anchor="nw")


x = font.families()
for i in x:
    l = Label(sFrame, text=i, font=(i, 12))
    print(i)
    l.pack()
root.mainloop()
