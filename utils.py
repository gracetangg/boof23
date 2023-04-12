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


# keys = ['QWERTYUIOP', 'ASDFGHJKL!', 'ZXCVBNM@']
# for r in range(len(keys)):
#     for c in range(len(keys[r])):
#         key = keys[r][c]
#         c += 1
#         if key == '!':
#             print(f"\t\tttk.Button(self.keyboard_canvas, text='back', width=3, command=(lambda:self.press('back'))).grid(row={r}, column={c}, ipadx=3, ipady=7)")
#         elif key == '@':
#             print(f"\t\tttk.Button(self.keyboard_canvas, text='enter', width=3, command=(lambda:self.update_leaderboard())).grid(row={r}, column={c if r < 2 else c + 1}, ipadx=3, ipady=7)")
#         else:
#             print(f"\t\tttk.Button(self.keyboard_canvas, text='{key}', width=3, command=(lambda:self.press('{key}'))).grid(row={r}, column={c if r < 2 else c + 1}, ipadx=3, ipady=7)")
#         # c = c if r < 2 else c + 1
#         # button.grid(row=r, column=c, ipadx=3, ipady=7)