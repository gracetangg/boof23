import os
import math
import time 
import serial

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw, ImageOps

from rounded import RoundedButton

LARGEFONT = ("Verdana", 35)
BUTTONFONT = ('Quicksand Medium', 14, "bold")
SCOREFONT = ('Quicksand Medium', 14, "bold")

GAME_TIME = 1
LEADERBOARD = [] 

GIF_FRAMES = 52
GIF_DELAY = 150 / 1000

PORTNAME = '/dev/cu.usbmodem144201'
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
        self.show_frame(MenuPage)
  
    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
  
# first window frame MenuPage
class MenuPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller

        self.canvas = tk.Canvas(self, width=800, height=480)
        self.canvas.pack(fill="both", expand=True)

        self.alice_flower = ImageTk.PhotoImage(Image.open("alice_flower.png"))
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.alice_flower, tag="flower")

        self.canvas.create_text((400, 120), text=f"PAINT", fill="white", font=('Trattatello', 90))
        self.canvas.create_text((400, 190), text=f"the", fill="white", font=('Trattatello', 40))
        self.canvas.create_text((400, 265), text=f"ROSES", fill="white", font=('Trattatello', 90))

        # setting positions
        button_pos = (75, 340)

        # putting the button in its place by
        self.instructions_button = RoundedButton(button_pos[0], button_pos[1], self.canvas, text="Instructions", font=BUTTONFONT, fg="#9c171a",
            command=(lambda : controller.show_frame(Instructions)))
  
        self.play_button = RoundedButton((button_pos[0]+225), button_pos[1], self.canvas, text ="Play", font=BUTTONFONT, fg="#9c171a",
            command=self.start_game)

        self.leaderboard_button = RoundedButton((button_pos[0]+450), button_pos[1], self.canvas, text ="Leaderboard", font=BUTTONFONT, fg="#9c171a",
            command=self.show_leader)

        self.parent.update()

    def start_game(self):
        self.controller.show_frame(GamePage)
        gp = self.controller.frames[GamePage]
        gp.get_ready()

    def show_leader(self):
        self.controller.show_frame(Leaderboard)
        leader = self.controller.frames[Leaderboard]
        leader.view_leaderboard()
  
# second window frame Instructions
class Instructions(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        title_label = tk.Label(self, text="How to Paint the Roses?", font=('Trattatello', 50), fg="#9c171a")
        title_label.place(x=200, y=5)

        button_pos = (350, 440)

        back_button = tk.Button(self, text ="Back", font=('Trattatello', 20),
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
        self.finish_img = ImageTk.PhotoImage(Image.open("sad_card.jpeg"))

        self.gif = Image.open(r"paint_roses.gif")
        self.gif_frames = self.gif.n_frames
        self.gif_label = tk.Label(self.canvas)
        self.animation = []
        self.load_gif()
    
        self.button_pos = (300, 390)

        self.continue_button = RoundedButton(325, 240, self.canvas, text="Continue", font=BUTTONFONT,
                                                command=self.to_leaderboard)
        self.canvas.delete("Continue")

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
                                             fill="#9c171a", 
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
        # send first 'y' to the arduino to prep for start: 
        # arduino.write(bytes('y', 'utf-8'))

        text_center = (400, 240)
        
        soldier_image = ImageTk.PhotoImage(Image.open("card_soldiers.png"))
        soldier_image_flipped = ImageTk.PhotoImage(ImageOps.mirror(Image.open("card_soldiers.png")))    

        self.canvas.delete(self.continue_button)    

        self.canvas.create_image(25, 150, anchor=tk.NW, image=soldier_image, tag="soldL")
        self.canvas.create_image(775, 150, anchor=tk.NE, image=soldier_image_flipped, tag="soldR")
        self.parent.update()

        self.canvas.create_text(text_center, text="3", fill="#9c171a", font=('Trattatello', 200), tag='countdown')
        self.canvas.pack(fill="both", expand=True)
        self.parent.update()
        time.sleep(1)

        self.canvas.delete("countdown")
        self.canvas.create_text(text_center, text="2", fill="#9c171a", font=('Trattatello', 200), tag='countdown')
        self.canvas.pack(fill="both", expand=True)
        self.parent.update()
        time.sleep(1)

        self.canvas.delete("countdown")
        self.canvas.create_text(text_center, text="1", fill="#9c171a", font=('Trattatello', 200), tag='countdown')
        self.canvas.pack(fill="both", expand=True)
        self.parent.update()
        time.sleep(1)
        
        self.canvas.delete("countdown")
        self.canvas.create_text(text_center, text="GO!", fill="#9c171a", font=('Trattatello', 200), tag='countdown')
        self.canvas.pack(fill="both", expand=True)
        self.parent.update()
        time.sleep(1)

        self.canvas.delete("countdown")
        self.canvas.delete("soldL")
        self.canvas.delete("soldR")
        self.parent.update()
        self.start_game()

        # write 'y' second time to actually start game
        # arduino.write(bytes('y', 'utf-8'))

    def reset(self):
        self.canvas.delete("all")
        self.canvas.delete(self.continue_button)    
        # self.continue_button.place_forget()

        self.start_time = 0
        self.elapsed_time = 0       
        self.current_score = 0 

        self.gif_index = 0
        self.gif_time = 0

    def to_leaderboard(self):
        self.controller.show_frame(Leaderboard)
        leaderboard = self.controller.frames[Leaderboard]
        leaderboard.show_score(self.current_score)
        self.reset()

    def game_over(self):
        self.canvas.delete("watch")
        self.canvas.delete("score")
        self.canvas.delete("points")
        self.canvas.delete(self.img)

        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.finish_img, tag="finish_img")
        self.canvas.create_text((400, 75), text="GAME OVER", font=('Trattatello', 100), tag='countdown', fill="white")
        self.canvas.create_text((400, 350), text=f"Score: {self.current_score}", font=('Quicksand Medium', 30, "bold"), tag='countdown', fill="white")
        self.continue_button = RoundedButton(self.button_pos[0], self.button_pos[1], self.canvas, text="Continue", font=BUTTONFONT,
                                                command=self.to_leaderboard)
        
        self.parent.update()

    def start_game(self):
        """
        Actually runs the game for GAME_TIME:
        """
        SCORE_STRING = "new score: "
        self.setup_game()
        while self.elapsed_time <= GAME_TIME:
            self.play_gif()

            # serial read to find the score/game over
            # data = arduino.readline().decode('utf-8').rstrip()
            # if data == "":
            #     continue
            # # if there is a score update:
            # if SCORE_STRING in data: 
            #     new_score = int(data[len(SCORE_STRING):])
            #     self.current_score += new_score
            #     self.update_score()

            # if data == 'game over!!!':
            #     data = arduino.readline().decode('utf-8').rstrip()
            #     score = int(data[20:])
            #     assert(score == self.current_score)
            self.current_score += 3
            self.update_score()
            self.update_clock()
        self.game_over()

# foruth window frame Leaderboard
class Leaderboard(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller

        self.leaderboard = []
        with open('leaderboard.txt', 'r') as f:
            for i in range(5):
                line = f.readline().strip().split(',')
                self.leaderboard += [(int(line[0]), line[1])]

        self.canvas = tk.Canvas(self, width=800, height=480, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.leader_labels = []
        self.score_header = tk.Label(self.canvas, text=f"Score:", font=('Quicksand Medium', 20, "bold"), fg="#9c171a")
        self.player_header = tk.Label(self.canvas, text=f"Player:", font=('Quicksand Medium', 20, "bold"), fg="#9c171a")
        self.title_label = tk.Label(self.canvas, text="", font=('Trattatello', 50), fg="#9c171a")

        self.good_img = ImageTk.PhotoImage(Image.open("good.png"))
        self.bad_img = ImageTk.PhotoImage(Image.open("bad.png"))
        self.background = self.canvas.create_image(0, 0, anchor=tk.NW, image=None, tag="background")

        self.keyboard_canvas = tk.Canvas(self, width=600, height=300)
        self.keyboard_canvas.place_forget()
        self.create_keyboard()

        self.typing_label = tk.Label(self.canvas, text="type your name", font=('Trattatello', 50), fg="#9c171a")
        self.typing_pos = (50, 50)
        self.current_score = 0
        self.current_name = ""

        self.back_button = None
        self.add_button = None
        self.view_button = None

    def show_score(self, score):
        self.current_name = ""
        self.current_score = score
        self.title_label.destroy()

        if score > min(self.leaderboard)[0]: 
            button_pos = (75, 350)
            
            self.background = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.good_img, tag="background")

            self.title_label = self.canvas.create_text((400, 250), text="TOP 5!", font=('Trattatello', 100), fill="white", tag="title")
            
            self.back_button = RoundedButton(button_pos[0], button_pos[1], self.canvas, text ="Back to Menu", font=BUTTONFONT,
                                             command = lambda : self.leave_leaderboard())
            self.add_button = RoundedButton(button_pos[0]+225, button_pos[1], self.canvas, text ="Add to Leaderboard", font=BUTTONFONT,
                                             command = lambda : self.add_leaderboard())
            self.view_button = RoundedButton(button_pos[0]+450, button_pos[1], self.canvas, text ="View Leaderboard", font=BUTTONFONT,
                            command = lambda : self.view_leaderboard())
        
        else: 
            self.background = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bad_img, tag="background")
            
            self.title_label = self.canvas.create_text((400, 300), text="Who Painted My Roses Red?", font=('Trattatello', 50), fill="white", tag="title")
            
            self.back_button = RoundedButton(150, 300, self.canvas, text ="Back to Menu", font=BUTTONFONT,
                                             command = lambda : self.leave_leaderboard())
            self.view_button = RoundedButton(450, 300, self.canvas, text ="View Leaderboard", font=BUTTONFONT,
                                             command = lambda : self.view_leaderboard())

    def press(self, key):
        if key == 'back':
            self.current_name = self.current_name[:-1]
        else: 
            self.current_name = self.current_name + key

        self.typing_label['text'] = self.current_name
        self.typing_label.place(x=self.typing_pos[0], y=self.typing_pos[1])

    def create_keyboard(self):
        ttk.Button(self.keyboard_canvas, text='Q', width=4, command=(lambda:self.press('Q'))).grid(row=0, column=1, ipadx=3, ipady=7)
        ttk.Button(self.keyboard_canvas, text='W', width=4, command=(lambda:self.press('W'))).grid(row=0, column=2, ipadx=3, ipady=7)
        ttk.Button(self.keyboard_canvas, text='E', width=4, command=(lambda:self.press('E'))).grid(row=0, column=3, ipadx=3, ipady=7)
        ttk.Button(self.keyboard_canvas, text='R', width=4, command=(lambda:self.press('R'))).grid(row=0, column=4, ipadx=3, ipady=7)
        ttk.Button(self.keyboard_canvas, text='T', width=4, command=(lambda:self.press('T'))).grid(row=0, column=5, ipadx=3, ipady=7)
        ttk.Button(self.keyboard_canvas, text='Y', width=4, command=(lambda:self.press('Y'))).grid(row=0, column=6, ipadx=3, ipady=7)
        ttk.Button(self.keyboard_canvas, text='U', width=4, command=(lambda:self.press('U'))).grid(row=0, column=7, ipadx=3, ipady=7)
        ttk.Button(self.keyboard_canvas, text='I', width=4, command=(lambda:self.press('I'))).grid(row=0, column=8, ipadx=3, ipady=7)
        ttk.Button(self.keyboard_canvas, text='O', width=4, command=(lambda:self.press('O'))).grid(row=0, column=9, ipadx=3, ipady=7)
        ttk.Button(self.keyboard_canvas, text='P', width=4, command=(lambda:self.press('P'))).grid(row=0, column=10, ipadx=3, ipady=7)
        ttk.Button(self.keyboard_canvas, text='A', width=4, command=(lambda:self.press('A'))).grid(row=1, column=1, ipadx=3, ipady=7)
        ttk.Button(self.keyboard_canvas, text='S', width=4, command=(lambda:self.press('S'))).grid(row=1, column=2, ipadx=3, ipady=7)
        ttk.Button(self.keyboard_canvas, text='D', width=4, command=(lambda:self.press('D'))).grid(row=1, column=3, ipadx=3, ipady=7)
        ttk.Button(self.keyboard_canvas, text='F', width=4, command=(lambda:self.press('F'))).grid(row=1, column=4, ipadx=3, ipady=7)
        ttk.Button(self.keyboard_canvas, text='G', width=4, command=(lambda:self.press('G'))).grid(row=1, column=5, ipadx=3, ipady=7)
        ttk.Button(self.keyboard_canvas, text='H', width=4, command=(lambda:self.press('H'))).grid(row=1, column=6, ipadx=3, ipady=7)
        ttk.Button(self.keyboard_canvas, text='J', width=4, command=(lambda:self.press('J'))).grid(row=1, column=7, ipadx=3, ipady=7)
        ttk.Button(self.keyboard_canvas, text='K', width=4, command=(lambda:self.press('K'))).grid(row=1, column=8, ipadx=3, ipady=7)
        ttk.Button(self.keyboard_canvas, text='L', width=4, command=(lambda:self.press('L'))).grid(row=1, column=9, ipadx=3, ipady=7)
        ttk.Button(self.keyboard_canvas, text='back', width=4, command=(lambda:self.press('back'))).grid(row=1, column=10, ipadx=3, ipady=7)
        ttk.Button(self.keyboard_canvas, text='Z', width=4, command=(lambda:self.press('Z'))).grid(row=2, column=2, ipadx=3, ipady=7)
        ttk.Button(self.keyboard_canvas, text='X', width=4, command=(lambda:self.press('X'))).grid(row=2, column=3, ipadx=3, ipady=7)
        ttk.Button(self.keyboard_canvas, text='C', width=4, command=(lambda:self.press('C'))).grid(row=2, column=4, ipadx=3, ipady=7)
        ttk.Button(self.keyboard_canvas, text='V', width=4, command=(lambda:self.press('V'))).grid(row=2, column=5, ipadx=3, ipady=7)
        ttk.Button(self.keyboard_canvas, text='B', width=4, command=(lambda:self.press('B'))).grid(row=2, column=6, ipadx=3, ipady=7)
        ttk.Button(self.keyboard_canvas, text='N', width=4, command=(lambda:self.press('N'))).grid(row=2, column=7, ipadx=3, ipady=7)
        ttk.Button(self.keyboard_canvas, text='M', width=4, command=(lambda:self.press('M'))).grid(row=2, column=8, ipadx=3, ipady=7)
        ttk.Button(self.keyboard_canvas, text='enter', width=4, command=(lambda:self.update_leaderboard())).grid(row=2, column=9, ipadx=3, ipady=7)

    def show_keyboard(self):
        self.canvas.delete("title")
        self.canvas.delete("BacktoMenu")
        self.canvas.delete("AddtoLeaderboard")
        self.canvas.delete("ViewLeaderboard")
        self.canvas.delete("background")

        self.typing_label['text'] = "type your name"
        self.typing_label.place(x=self.typing_pos[0], y=self.typing_pos[1])

        keyboard_pos = (25, 200)
        self.keyboard_canvas.place(x=keyboard_pos[0], y=keyboard_pos[1])
        self.parent.update()
    
    def hide_keyboard(self):
        if self.typing_label: self.typing_label.place_forget()
        self.keyboard_canvas.place_forget()
        self.parent.update()

    def save_leaderboard(self):
        with open('leaderboard.txt', 'w') as f:
            for score, player in self.leaderboard:
                f.write(f"{score},{player}\n")

    def update_leaderboard(self):
        self.leaderboard = self.leaderboard[:-1] + [(self.current_score, self.current_name)]
        self.leaderboard.sort(reverse=True, key=lambda x: x[0])
        self.save_leaderboard()

        self.hide_keyboard()
        self.title_label.destroy()
        self.title_label = tk.Label(self.canvas, text="your score has been saved!", font=('Trattatello', 50), fg="#9c171a")

        self.back_button = RoundedButton(150, 300, self.canvas, text ="Back to Menu", font=BUTTONFONT,
                                             command = lambda : self.leave_leaderboard())
        self.view_button = RoundedButton(450, 300, self.canvas, text ="View Leaderboard", font=BUTTONFONT,
                                             command = lambda : self.view_leaderboard())

        self.title_label.place(x=175, y=200)

    def add_leaderboard(self):
        self.show_keyboard()

    def view_leaderboard(self):
        self.title_label.destroy()
        self.canvas.delete("BacktoMenu")
        self.canvas.delete("AddtoLeaderboard")
        self.canvas.delete("ViewLeaderboard")
        self.canvas.delete("background")
        self.hide_keyboard()

        self.back_button = RoundedButton(300, 400, self.canvas, text ="Back to Menu", font=BUTTONFONT,
                                             command=lambda:self.leave_leaderboard())
        print(self.back_button)

        score_pos = (200, 50)
        player_pos = (550, 50)

        self.score_header.place(x=score_pos[0], y=score_pos[1])
        self.player_header.place(x=player_pos[0], y=player_pos[1])

        self.leader_labels = []
        for i, (score, leader) in enumerate(self.leaderboard): 
            score_lbl = tk.Label(self.canvas, text=f"{score}", font=SCOREFONT, fg="#9c171a")
            player_lbl = tk.Label(self.canvas, text=f"{leader}", font=SCOREFONT, fg="#9c171a")
            self.leader_labels += [(score_lbl, player_lbl)]

            score_lbl.place(x=score_pos[0], y=score_pos[1] + 50 * (i + 1))
            player_lbl.place(x=player_pos[0], y=player_pos[1] + 50 * (i + 1))
        
    def leave_leaderboard(self):
        self.controller.show_frame(MenuPage)
        self.title_label.destroy()
        self.canvas.delete("BacktoMenu")
        self.canvas.delete("AddtoLeaderboard")
        self.canvas.delete("ViewLeaderboard")
        self.canvas.delete("background")
        self.hide_keyboard()

        # forget leaderboard stuff if its there:
        if self.score_header: self.score_header.place_forget()
        if self.player_header: self.player_header.place_forget()
        for score, player in self.leader_labels:
            score.destroy()
            player.destroy()

        self.title_label = tk.Label(self.canvas, text="Can YOU Make it to TOP 5?", font=('Trattatello', 50), fg="#9c171a")
        self.title_label.place(x=160, y=200)


if __name__ == "__main__":
    # Driver Code
    app = RosesGame()
    # app.overrideredirect(1) #Remove border
    app.mainloop()