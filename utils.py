import math

from tkinter import *
from PIL import Image, ImageTk

root = Tk()
images = []

def create_line(x1, y1, x2, y2, **kwargs):
    if 'alpha' in kwargs:
        alpha = int(kwargs.pop('alpha') * 255)
        fill = kwargs.pop('fill')
        fill = root.winfo_rgb(fill) + (alpha,)
        image = Image.new('RGBA', (x2-x1, 2), fill)
        image = image.rotate(math.atan2((y2 - y1), (x2 - x1)) * 180 / math.pi, Image.NEAREST, expand=1)
        images.append(ImageTk.PhotoImage(image))
        # canvas.create_image(x1, y1, image=images[-1], anchor='nw')
        return image
    # canvas.create_rectangle(x1, y1, x2, y2, **kwargs)

# canvas = Canvas(width=300, height=200)
# canvas.pack()

# # create_rectangle(10, 10, 200, 100, fill='gray')
# # create_rectangle(50, 50, 250, 150, fill='green', alpha=.5)
# # create_rectangle(80, 80, 150, 120, fill='#800000', alpha=.8)

# create_line(10, 10, 200, 300, fill='red', alpha=0.5)

# root.mainloop()