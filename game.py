import os
import math
import time 
import serial

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw, ImageOps

LARGEFONT = ("Verdana", 35)

GAME_TIME = 10
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

        title_label = ttk.Label(self, text="Can You Paint the Roses RED?", font=('Trattatello', 50))
        title_label.place(x=115, y=150)

        # setting positions
        button_pos = (190, 300)

        # putting the button in its place by
        instruction_button = tk.Button(self, text="INSTRUCTIONS", font=('Trattatello', 10)
            command = lambda : controller.show_frame(Instructions))
        instruction_button.place(x=button_pos[0], y=button_pos[1])
  
        ## button to show frame 2 with text layout2
        play_button = ttk.Button(self, text ="PLAY",
            command = lambda : self.start_game())
        play_button.place(x=(button_pos[0]+160), y=button_pos[1])

        ## button to show frame 2 with text layout2
        leaderboard_button = ttk.Button(self, text ="LEADERBOARD",
            command = lambda : self.show_leader())
        leaderboard_button.place(x=(button_pos[0]+300), y=button_pos[1])

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
        title_label = ttk.Label(self, text="How to Paint the Roses?", font=('Trattatello', 50))
        title_label.place(x=200, y=5)

        button_pos = (350, 440)

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
        # send first 'y' to the arduino to prep for start: 
        # arduino.write(bytes('y', 'utf-8'))

        text_center = (400, 240)
        
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

        # write 'y' second time to actually start game
        # arduino.write(bytes('y', 'utf-8'))

    def reset(self):
        self.canvas.delete("all")
        self.continue_button.place_forget()

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

        self.canvas.create_text((400, 240), text="GAME OVER", fill="White", font=('Trattatello', 100), tag='countdown')
        self.canvas.create_text((400, 300), text=f"your score: {self.current_score}", fill="White", font=('Trattatello', 50), tag='countdown')

        self.continue_button.place(x=self.button_pos[0], y=self.button_pos[1]+100)
        
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
        self.score_header = ttk.Label(self.canvas, text=f"Score:", font=('Trattatello', 20))
        self.player_header = ttk.Label(self.canvas, text=f"Player:", font=('Trattatello', 20))
        self.title_label = ttk.Label(self.canvas, text="", font=('Trattatello', 50))

        self.keyboard_canvas = tk.Canvas(self, width=600, height=300)
        self.keyboard_canvas.place_forget()
        self.create_keyboard()

        self.typing_label = ttk.Label(self.canvas, text="type your name", font=('Trattatello', 50))
        self.typing_pos = (50, 50)
        self.current_score = 0
        self.current_name = ""

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
        self.current_name = ""
        self.current_score = score
        self.title_label.destroy()

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

    def press(self, key):
        if key == 'back':
            self.current_name = self.current_name[:-1]
        else: 
            self.current_name = self.current_name + key

        self.typing_label['text'] = self.current_name
        # self.typing_label = ttk.Label(self.canvas, text=self.current_name, font=('Trattatello', 50))
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
        self.title_label.destroy()
        self.back_button.place_forget()
        self.add_button.place_forget()
        self.view_button.place_forget()

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
        self.title_label = ttk.Label(self.canvas, text="your score has been saved!", font=('Trattatello', 50))
        self.title_label.place(x=175, y=200)
        self.back_button.place(x=200, y=300)
        self.view_button.place(x=400, y=300)

    def add_leaderboard(self):
        self.show_keyboard()

    def view_leaderboard(self):
        self.title_label.destroy()
        self.back_button.place_forget()
        self.add_button.place_forget()
        self.view_button.place_forget()
        self.hide_keyboard()

        self.back_button.place(x=300, y=400)

        score_pos = (200, 50)
        player_pos = (550, 50)

        self.score_header.place(x=score_pos[0], y=score_pos[1])
        self.player_header.place(x=player_pos[0], y=player_pos[1])

        self.leader_labels = []
        for i, (score, leader) in enumerate(self.leaderboard): 
            score_lbl = ttk.Label(self.canvas, text=f"{score}", font=('Trattatello', 20))
            player_lbl = ttk.Label(self.canvas, text=f"{leader}", font=('Trattatello', 20))
            self.leader_labels += [(score_lbl, player_lbl)]

            score_lbl.place(x=score_pos[0], y=score_pos[1] + 50 * (i + 1))
            player_lbl.place(x=player_pos[0], y=player_pos[1] + 50 * (i + 1))
        
    def leave_leaderboard(self):
        self.controller.show_frame(MenuPage)
        self.title_label.destroy()
        self.back_button.place_forget()
        self.add_button.place_forget()
        self.view_button.place_forget()
        self.hide_keyboard()

        # forget leaderboard stuff if its there:
        if self.score_header: self.score_header.place_forget()
        if self.player_header: self.player_header.place_forget()
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