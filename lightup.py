import os
import math
import time 
import pyglet
# import serial

import tkinter as tk
from tkinter import ttk
from tkextrafont import Font
from PIL import Image, ImageTk

LARGEFONT = ("Verdana", 35)

GAME_TIME = 45
LEADERBOARD = [] 

GIF_FRAMES = 52
GIF_DELAY = 150 / 1000

PORTNAME = '/dev/cu.usbmodem144201'

# pyglet.font.add_file('MiltonianTattoo-Regular.ttf')
# arduino = serial.Serial(port=PORTNAME, baudrate=9600, timeout=.1)
  
class RosesGame(tk.Tk):
    # __init__ function for class RosesGame
    def __init__(self, *args, **kwargs):
        # __init__ function for class Tk
        # set the size to fit screen
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("PAINT THE ROSES RED")
        self.geometry("800x480")
         
        # creating a container
        container = tk.Frame(self) 
        container.pack(side="top", fill="both", expand=True)
  
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
  
        # initializing frames to an empty array
        self.frames = {} 
  
        # iterating through a tuple consisting
        # of the different page layouts
        for F in (MenuPage, Instructions, GamePage, Leaderboard):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        # self.show_frame(MenuPage)
        self.show_frame(GamePage)
  
    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
  
# first window frame MenuPage
class MenuPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        title_label = ttk.Label(self, text="Can You Paint the Roses Red?")
        title_label.place(x=220, y=200)

        # setting positions
        button_pos = (190, 300)

        # putting the button in its place by
        instruction_button = ttk.Button(self, text="INSTRUCTIONS",
            command = lambda : controller.show_frame(Instructions))
        instruction_button.place(x=button_pos[0], y=button_pos[1])
  
        ## button to show frame 2 with text layout2
        play_button = ttk.Button(self, text ="PLAY",
            command = lambda : controller.show_frame(GamePage))
        play_button.place(x=(button_pos[0]+160), y=button_pos[1])

        ## button to show frame 2 with text layout2
        leaderboard_button = ttk.Button(self, text ="LEADERBOARD",
            command = lambda : controller.show_frame(Leaderboard))
        leaderboard_button.place(x=(button_pos[0]+300), y=button_pos[1])
  
# second window frame Instructions
class Instructions(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        title_label = ttk.Label(self, text="How to Paint the Roses Red?")
        title_label.place(x=220, y=200)

        button_pos = (350, 300)

        back_button = ttk.Button(self, text ="BACK",
                            command = lambda : controller.show_frame(MenuPage))
        back_button.place(x=button_pos[0], y=button_pos[1])


# third window frame GamePage
class GamePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.clock_position = (10, 10)
        self.clock_size = 150
        self.point_position = (540, 10)
        self.point_size = (250, 150)
        self.parent = parent

        # create a canvas for background animation/image with parent window
        self.canvas = tk.Canvas(self, width=800, height=480)
        self.canvas.pack()
        self.canvas.pack(fill="both", expand=True)

        self.gif = Image.open(r"paint_roses(low).gif")
        self.gif_frames = self.gif.n_frames
        self.gif_label = tk.Label(self.canvas)
        self.animation = []
        self.img = self.canvas.create_image(0, 0, anchor=tk.NW, image=None)
        self.load_gif()

        self.button_pos = (350, 240)
        self.play_button = ttk.Button(self, text ="START",
            command = lambda : self.get_ready())
        self.play_button.place(x=self.button_pos[0], y=self.button_pos[1])

        self.start_time = 0
        self.elapsed_time = 0       # amount of time left in seconds
        self.current_score = 0      # score of the current player

        self.gif_index = 0
        self.gif_time = 0

    def load_gif(self):
        for x in range(self.gif_frames):
            frame = ImageTk.PhotoImage(self.gif.copy())
            self.animation.append(frame)
            self.gif.seek(x)

    def update_clock(self):
        """
        update the clock every second
        """
        angle_per_second = 2 * math.pi / GAME_TIME
        clock_radius = self.clock_size / 2
        clock_center = (self.clock_position[0] + self.clock_size / 2, 
                        self.clock_position[1] + self.clock_size / 2)
        
        self.elapsed_time = time.time() - self.start_time
        time_left = GAME_TIME - self.elapsed_time

        angle = (time_left * angle_per_second) + 3 * math.pi/2
        x = clock_center[0] + clock_radius * math.cos(angle)
        y = clock_center[1] + clock_radius * math.sin(angle)

        self.canvas.create_oval(self.clock_position, 
                                        (self.clock_position[0] + self.clock_size, self.clock_position[1] + self.clock_size), 
                                        outline='white', width=2)    
        self.canvas.create_line(clock_center, (x, y), fill="white", width=2)

    def update_score(self):
        text_center = (650, 75)
        font = Font(file="MiltonianTattoo-Regular.ttf")
        self.canvas.delete('points')
        self.canvas.create_text(text_center, text=f"YOUR SCORE: {self.current_score}", 
                                             fill="White", 
                                            #  font=('Helvetica 15 bold', 30), 
                                             font=font,
                                             tag='points')

    def play_gif(self):
        if time.time() - self.gif_time > GIF_DELAY: 
            self.gif_time = time.time()
            self.gif_index = (self.gif_index + 1) % GIF_FRAMES
            self.canvas.itemconfig(self.img, image=self.animation[self.gif_index])
            self.parent.update()

    def get_ready(self):
        """
        Countdown animation
        """
        text_center = (400, 240)
        # hide the button, show it again with place later
        self.play_button.place_forget()

        self.canvas.create_text(text_center, text="3", fill="White", font=('Helvetica 15 bold', 200), tag='countdown')
        self.canvas.pack(fill="both", expand=True)
        self.parent.update()
        time.sleep(1)

        self.canvas.delete("countdown")
        self.canvas.create_text(text_center, text="2", fill="White", font=('Helvetica 15 bold', 200), tag='countdown')
        self.canvas.pack(fill="both", expand=True)
        self.parent.update()
        time.sleep(1)

        self.canvas.delete("countdown")
        self.canvas.create_text(text_center, text="1", fill="White", font=('Helvetica 15 bold', 200), tag='countdown')
        self.canvas.pack(fill="both", expand=True)
        self.parent.update()
        time.sleep(1)
        
        self.canvas.delete("countdown")
        self.canvas.create_text(text_center, text="GO", fill="White", font=('Helvetica 15 bold', 200), tag='countdown')
        self.canvas.pack(fill="both", expand=True)
        self.parent.update()
        time.sleep(1)

        self.canvas.delete("countdown")
        self.parent.update()
        self.start_game()

    def start_game(self):
        self.start_time = time.time()
        self.elapsed_time = 0
        self.current_score = 0
        # NOTE: at the beginning the serial prompt should be waiting for pi to 
        # output start
        # arduino.write(bytes('start', 'utf-8'))

        while True: 
            self.play_gif()
            self.current_score += 1
            self.update_score()
            self.update_clock()
            self.parent.update()
            # time.sleep(0.005)

        self.show_score()

# foruth window frame Leaderboard
class Leaderboard(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        title_label = ttk.Label(self, text="Did YOU Make it in the Top 5?")
        title_label.place(x=220, y=200)

        button_pos = (350, 300)
        back_button = ttk.Button(self, text ="BACK",
                            command = lambda : controller.show_frame(MenuPage))
        back_button.place(x=button_pos[0], y=button_pos[1])
  
  
# Driver Code
app = RosesGame()
app.mainloop()