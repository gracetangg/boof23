import os
import math
import time 
# import pyglet.font as font
# import serial

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw, ImageOps

LARGEFONT = ("Verdana", 35)

GAME_TIME = 2
LEADERBOARD = [] 

GIF_FRAMES = 52
GIF_DELAY = 150 / 1000

PORTNAME = '/dev/cu.usbmodem144201'

# font.add_file('MiltonianTattoo-Regular.ttf')
# arduino = serial.Serial(port=PORTNAME, baudrate=9600, timeout=.1)
  
class RosesGame(tk.Tk):
    # __init__ function for class RosesGame
    def __init__(self, *args, **kwargs):
        # __init__ function for class Tk
        # set the size to fit screen
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("PAINT THE ROSES RED")
        self.geometry("800x480")
        self.config(bg="#383434")
         
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
        self.parent = parent
        self.controller = controller

        self.clock_position = (33, 75)
        self.clock_size = 106 # 150
        self.point_position = (540, 10)
        self.point_size = (250, 150)

        # create a canvas for background animation/image with parent window
        self.canvas = tk.Canvas(self, width=800, height=480)
        self.canvas.pack(fill="both", expand=True)

        self.img = None
        self.watch_img = ImageTk.PhotoImage(Image.open("stop_watch.png"))
        self.score_img = ImageTk.PhotoImage(Image.open("score_card.png"))

        self.gif = Image.open(r"paint_roses.gif")
        self.gif_frames = self.gif.n_frames
        self.gif_label = tk.Label(self.canvas)
        self.animation = []
        self.load_gif()
    
        self.button_pos = (350, 240)
        self.play_button = ttk.Button(self, text="START",
                                            command=(lambda:self.get_ready()))
        self.play_button.place(x=self.button_pos[0], y=self.button_pos[1])

        self.continue_button = ttk.Button(self, text="CONTINUE", 
                                                command=self.to_leaderboard)
        self.continue_button.place(x=self.button_pos[0], y=self.button_pos[1])
        self.continue_button.place_forget()

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
        time_left = (GAME_TIME - self.elapsed_time)

        angle = ((time_left * angle_per_second) + 3 * math.pi/2)  * 180 / math.pi

        overlay = Image.new('RGBA', (self.clock_size, self.clock_size), color=(0,0,0,0))
        draw = ImageDraw.Draw(overlay)
        draw.pieslice(((0, 0), (self.clock_size, self.clock_size)), start=angle, end=270, fill=(255, 0, 0, 200))
        overlay = ImageTk.PhotoImage(overlay.copy())

        self.canvas.itemconfig('watch', image=self.watch_img)
        self.canvas.create_image(clock_center, anchor=tk.CENTER, image=overlay)
        self.parent.update()

    def update_score(self):
        text_center = (700, 110)
        self.canvas.delete('points')
        self.canvas.itemconfig('watch', image=self.watch_img)
        self.canvas.create_text(text_center, text=f"{self.current_score}", 
                                             fill="Red", 
                                             font=('Trattatello', 50), 
                                             tag='points')

    def play_gif(self):
        if time.time() - self.gif_time > GIF_DELAY: 
            self.gif_time = time.time()
            self.gif_index = (self.gif_index + 1) % GIF_FRAMES
            self.canvas.itemconfig(self.img, image=self.animation[self.gif_index])

    def setup_game(self):
        self.start_time = time.time()
        self.elapsed_time = 0
        self.current_score = 0

        self.img = self.canvas.create_image(0, 0, anchor=tk.NW, image=None)
        self.canvas.create_image(10, 10, anchor=tk.NW, image=self.watch_img, tag="watch")
        self.canvas.create_image(625, 25, anchor=tk.NW, image=self.score_img, tag="score")

        self.play_gif()
        self.parent.update()

    def get_ready(self):
        """
        Countdown animation
        """
        text_center = (400, 240)
        # hide the button, show it again with place later
        self.play_button.place_forget()
        
        soldier_image = ImageTk.PhotoImage(Image.open("card_soldiers.png"))
        soldier_image_flipped = ImageTk.PhotoImage(ImageOps.mirror(Image.open("card_soldiers.png")))
        

        self.canvas.create_image(25, 200, anchor=tk.NW, image=soldier_image, tag="soldL")
        self.canvas.create_image(775, 200, anchor=tk.NE, image=soldier_image_flipped, tag="soldR")
        self.parent.update()

        self.canvas.create_text(text_center, text="3", fill="White", font=('Trattatello', 200), tag='countdown')
        self.canvas.pack(fill="both", expand=True)
        self.parent.update()
        time.sleep(1)

        self.canvas.delete("countdown")
        self.canvas.create_text(text_center, text="2", fill="White", font=('Trattatello', 200), tag='countdown')
        self.canvas.pack(fill="both", expand=True)
        self.parent.update()
        time.sleep(1)

        self.canvas.delete("countdown")
        self.canvas.create_text(text_center, text="1", fill="White", font=('Trattatello', 200), tag='countdown')
        self.canvas.pack(fill="both", expand=True)
        self.parent.update()
        time.sleep(1)
        
        self.canvas.delete("countdown")
        self.canvas.create_text(text_center, text="GO!", fill="White", font=('Trattatello', 200), tag='countdown')
        self.canvas.pack(fill="both", expand=True)
        self.parent.update()
        time.sleep(1)

        self.canvas.delete("countdown")
        self.canvas.delete("soldL")
        self.canvas.delete("soldR")
        self.parent.update()
        self.start_game()

    def reset(self):
        self.canvas.delete("all")
        self.play_button.place(x=self.button_pos[0], y=self.button_pos[1])
        self.continue_button.place_forget()

        self.start_time = 0
        self.elapsed_time = 0       
        self.current_score = 0 

        self.gif_index = 0
        self.gif_time = 0

    def to_leaderboard(self):
        self.controller.show_frame(Leaderboard)
        leaderboard = self.controller.frames[Leaderboard]
        leaderboard.show_score(200)
        self.reset()

    def game_over(self):
        self.canvas.delete("watch")
        self.canvas.delete("score")
        self.canvas.delete("points")
        self.canvas.delete(self.img)

        self.canvas.create_text((400, 240), text="GAME OVER", fill="White", font=('Trattatello', 100), tag='countdown')
        self.canvas.create_text((400, 300), text=f"your score: {self.current_score}", fill="White", font=('Trattatello', 50), tag='countdown')

        self.continue_button.place(x=self.button_pos[0], y=self.button_pos[1]+100)
        
        self.parent.update()

    def start_game(self):
        # NOTE: at the beginning the serial prompt should be waiting for pi to 
        # output start
        # arduino.write(bytes('start', 'utf-8'))
        self.setup_game()

        while self.elapsed_time <= GAME_TIME:
            self.play_gif()
            self.current_score += 1
            self.update_score()
            self.update_clock()
            time.sleep(0.01)

        self.game_over()

# foruth window frame Leaderboard
class Leaderboard(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller

        self.leaderboard = [(0, "p1"),
                            (0, "p1"),
                            (0, "p1"),
                            (0, "p1"),
                            (0, "p1"),]

        self.canvas = tk.Canvas(self, width=800, height=480)
        self.canvas.pack(fill="both", expand=True)

        self.title_label = None
        self.score_header = None
        self.player_header = None
        self.leader_labels = []

        self.back_button = ttk.Button(self, text ="BACK TO MENU",
                            command = lambda : self.leave_leaderboard())
        self.back_button.place_forget()

        self.add_button = ttk.Button(self, text ="ADD TO LEADERBOARD",
                            command = lambda : self.add_leaderboard())
        self.add_button.place_forget()

        self.view_button = ttk.Button(self, text ="SEE LEADERBOARD",
                            command = lambda : self.view_leaderboard())
        self.add_button.place_forget()
        

    def show_score(self, score):
        print(score)
        if score > min(self.leaderboard)[0]: 
            self.title_label = ttk.Label(self.canvas, text="YOU MADE IT in TOP 5!", font=('Trattatello', 50))
            self.title_label.place(x=150, y=200)

            self.back_button.place(x=150, y=300)
            self.add_button.place(x=300, y=300)
            self.view_button.place(x=500, y=300)
        else: 
            self.title_label = ttk.Label(self.canvas, text="Better Luck Next Time <3", font=('Trattatello', 50))
            self.title_label.place(x=175, y=200)

            self.back_button.place(x=200, y=300)
            self.view_button.place(x=400, y=300)



    def view_leaderboard(self):
        self.title_label.destroy()
        self.back_button.place_forget()
        self.add_button.place_forget()
        self.view_button.place_forget()

        self.back_button.place(x=300, y=400)

        score_pos = (200, 50)
        player_pos = (550, 50)

        self.score_header = ttk.Label(self.canvas, text=f"Score:", font=('Trattatello', 20))
        self.player_header = ttk.Label(self.canvas, text=f"Player:", font=('Trattatello', 20))
        self.score_header.place(x=score_pos[0], y=score_pos[1])
        self.player_header.place(x=player_pos[0], y=player_pos[1])

        self.leader_labels = []
        for i, (score, leader) in enumerate(self.leaderboard): 
            score_lbl = ttk.Label(self.canvas, text=f"{score}", font=('Trattatello', 20))
            player_lbl = ttk.Label(self.canvas, text=f"{leader}", font=('Trattatello', 20))
            self.leader_labels += [(score_lbl, player_lbl)]

            score_lbl.place(x=score_pos[0], y=score_pos[1] + 50 * i)
            player_lbl.place(x=player_pos[0], y=player_pos[1] + 50 * i)
        
    def leave_leaderboard(self):
        self.controller.show_frame(MenuPage)
        self.title_label.destroy()
        self.back_button.place_forget()
        self.add_button.place_forget()
        self.view_button.place_forget()

        # forget leaderboard stuff if its there:
        if self.score_header: self.score_header.destroy()
        if self.player_header: self.player_header.destroy()
        for score, player in self.leader_labels:
            score.destroy()
            player.destroy()

        self.title_label = ttk.Label(self.canvas, text="Can YOU Make it to TOP 5?", font=('Trattatello', 50))
        self.title_label.place(x=160, y=200)

        self.back_button.place(x=225, y=300)
        self.view_button.place(x=410, y=300)


if __name__ == "__main__":
    # Driver Code
    app = RosesGame()
    app.mainloop()