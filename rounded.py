import tkinter as tk

class RoundedButton():
    def __init__(self, x, y, canvas=None, text:str="", radius=25, fg="#000000", bg="#ffffff", command=None, font=("Times", 30), *args, **kwargs):
        self.canvas = canvas
        self.bg = bg
        self.command = command

        self.radius = radius        
        
        temp = self.canvas.create_text(0, 0, text=text, tags="button", fill=fg, font=font, justify="center")
        
        text_rect = self.canvas.bbox(temp)
        width = 200 # (text_rect[2]-text_rect[0]) + 15
        height = (text_rect[3]-text_rect[1]) + 15

        # self.canvas.delete(self.text)
        self.rect = self.round_rectangle(x, y, x + width, y + height, tags="button", radius=radius, fill=bg)
        self.text = self.canvas.create_text(x + width/2, y + height/2, text=text, tags="button", fill=fg, font=font, justify="center")

        self.canvas.tag_bind("button", "<ButtonPress>", self.border)
        self.canvas.tag_bind("button", "<ButtonRelease>", self.border)
          
    def round_rectangle(self, x1, y1, x2, y2, radius=25, update=False, **kwargs): # if update is False a new rounded rectangle's id will be returned else updates existing rounded rect.
        # source: https://stackoverflow.com/a/44100075/15993687
        points = [x1+radius, y1,
                x1+radius, y1,
                x2-radius, y1,
                x2-radius, y1,
                x2, y1,
                x2, y1+radius,
                x2, y1+radius,
                x2, y2-radius,
                x2, y2-radius,
                x2, y2,
                x2-radius, y2,
                x2-radius, y2,
                x1+radius, y2,
                x1+radius, y2,
                x1, y2,
                x1, y2-radius,
                x1, y2-radius,
                x1, y1+radius,
                x1, y1+radius,
                x1, y1]

        if not update:
            return self.canvas.create_polygon(points, **kwargs, smooth=True)
        
        else:
            self.coords(self.rect, points)

    def border(self, event):
        if event.type == "4":
            self.canvas.itemconfig(self.rect, fill="#d2d6d3")
            if self.command is not None:
                self.command()

        else:
            self.canvas.itemconfig(self.rect, fill=self.bg)

def func():
    print("Button pressed")

if __name__ == "__main__":
    root = tk.Tk()
    btn = RoundedButton(text="This is a \n rounded button", radius=100, bg="#0078ff", fg="#ffffff", command=func)
    btn.pack(expand=True, fill="both")
    root.mainloop()