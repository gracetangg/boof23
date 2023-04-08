import math
import time 
import serial

import tkinter as tk
from tkinter import ttk


LEADERBOARD = [] 
LARGEFONT = ("Verdana", 35)
  
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
        container.pack(side = "top", fill = "both", expand = True)
  
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
        self.canvas = tk.Canvas(self)
        self.canvas.configure()
        self.canvas.pack(fill="both", expand=True)

        # create a canvas for clock
        self.clock = tk.Canvas(self, width=self.clock_size + 50, height=self.clock_size + 50)
        self.clock.configure()
        self.clock.place(x=self.clock_position[0], y=self.clock_position[1])
        self.clock.place_forget()

        # create a canvas for points
        self.points = tk.Canvas(self, width=self.point_size[0], height=self.point_size[1])
        self.points.configure(bg="Blue")
        self.points.place(x=self.point_position[0], y=self.point_position[1])
        self.points.place_forget()
        self.parent.update()

        button_pos = (350, 240)
        ## button to show frame 2 with text layout2
        self.play_button = ttk.Button(self, text ="START",
            command = lambda : self.start_game())
        self.play_button.place(x=button_pos[0], y=button_pos[1])

        self.time_left = 0      # amount of time left in seconds

    def update_clock(self):
        """
        update the clock every second
        """
        angle_per_second = 2 * math.pi / 45
        clock_radius = self.clock_size / 2
        clock_center = (self.clock_position[0] + self.clock_size / 2, 
                        self.clock_position[1] + self.clock_size / 2)
        
        angle = (self.time_left * angle_per_second) + 3 * math.pi/2
        x = clock_center[0] + clock_radius * math.cos(angle)
        y = clock_center[1] + clock_radius * math.sin(angle)
        self.time_left -= 1

        self.clock.delete("all")
        self.clock.create_oval(self.clock_position, 
                              (self.clock_position[0] + self.clock_size, self.clock_position[1] + self.clock_size), 
                              outline='white', width=2)    
        self.clock.create_line(clock_center, (x, y), fill="white", width=2)
        self.clock.place(x=self.clock_position[0], y=self.clock_position[1])
        self.parent.update()

    def get_ready(self):
        """
        Countdown animation
        """
        text_center = (400, 240)
        # hide the button, show it again with place later
        self.play_button.place_forget()

        # self.canvas.config
        self.canvas.delete("all")
        self.canvas.create_text(text_center, text="3", fill="White", font=('Helvetica 15 bold', 200))
        self.canvas.pack(fill="both", expand=True)
        self.parent.update()
        time.sleep(1)

        self.canvas.delete("all")
        self.canvas.create_text(text_center, text="2", fill="White", font=('Helvetica 15 bold', 200))
        self.canvas.pack(fill="both", expand=True)
        self.parent.update()
        time.sleep(1)

        self.canvas.delete("all")
        self.canvas.create_text(text_center, text="1", fill="White", font=('Helvetica 15 bold', 200))
        self.canvas.pack(fill="both", expand=True)
        self.parent.update()
        time.sleep(1)
        
        self.canvas.delete("all")
        self.canvas.create_text(text_center, text="GO", fill="White", font=('Helvetica 15 bold', 200))
        self.canvas.pack(fill="both", expand=True)
        self.parent.update()
        time.sleep(1)

        self.canvas.delete("all")
        self.parent.update()
        self.start_game()

    def start_game(self):
        self.time_left = 45
        while self.time_left > 0: 
            self.update_clock()
            time.sleep(1)

        
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