import math

from tkinter import *
from PIL import Image, ImageTk
images = []

def create_line(x1, y1, x2, y2, canvas, **kwargs):
    # root = Tk()
    print("HERE")
    if 'alpha' in kwargs:
        alpha = int(kwargs.pop('alpha') * 255)
        fill = kwargs.pop('fill')
        fill = Tk().winfo_rgb(fill) + (alpha,)
        image = Image.new('RGBA', ((x2-x1), 2), fill)
        image = image.rotate(math.atan2((y2 - y1), (x2 - x1)) * 180 / math.pi, Image.NEAREST, expand=1)
        images.append(ImageTk.PhotoImage(image))
        canvas.create_image(x1, y1, image=images[-1], anchor='nw')
        # root.mainloop()
        # root.destroy()
        return ImageTk.PhotoImage(image)
    # canvas.create_rectangle(x1, y1, x2, y2, **kwargs)

# canvas = Canvas(width=300, height=200)
# canvas.pack()

# # create_rectangle(10, 10, 200, 100, fill='gray')
# # create_rectangle(50, 50, 250, 150, fill='green', alpha=.5)
# # create_rectangle(80, 80, 150, 120, fill='#800000', alpha=.8)

# create_line(10, 10, 200, 300, canvas, fill='red', alpha=0.5)

# root.mainloop()

from PIL import Image, ImageDraw

# Create a new empty 100x100 image for the sake of example.
# Use Image.open() to draw on your image instead, like this:
# img = Image.open('my_image.png')
img = Image.new('RGBA', (100, 100), color=(0,0,0,0))

radius = 25

# The circle position and size are specified by
# two points defining the bounding rectangle around the circle
topLeftPoint = (0, 0)
bottomRightPoint = (radius * 2, radius * 2)

draw = ImageDraw.Draw(img)

# Zero angle is at positive X axis, and it's going clockwise.
# start = 0, end = 180 would be bottom half circle.
# Adding 45 degrees, we get the diagonal half circle.
draw.pieslice((topLeftPoint, bottomRightPoint), start = 0, end = 270, fill=(255, 0, 0, 50))

img.save('moon.png')