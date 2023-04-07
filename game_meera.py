import serial
import time
from serial import Serial
arduino = serial.Serial(port='/dev/cu.usbmodem144201', baudrate=9600, timeout=.1)

leaderboard = []
score = 0

while True:
    data = arduino.readline().decode('utf-8').rstrip()
    if data != '':
        print(data)

    if data == "restart?" or data == "start?":
        val = input()
        if val == 'y':
            arduino.write(bytes(val, 'utf-8'))
    # TODO graphics create restart button and send byte when clicked
    
    elif data == "game over!!!":
        data = arduino.readline().decode('utf-8').rstrip()
        print(data)
        score = int(data[20:])
        print(f"score = {score}")
        if len(leaderboard) < 5:
            print("Enter your name:")
            name = input()
            leaderboard.append((name, score))
        else:
            leaderboard.sort(key=lambda a: a[1], reverse=True)
            min_score = leaderboard[4][1]
            if score > min_score:
                print("Enter your name:")
                name = input()
                if len(leaderboard) >= 5:
                    del leaderboard[4]
                leaderboard.append((name, score))
                leaderboard.sort(key=lambda a: a[1], reverse=True)
        print(leaderboard)
        # TODO graphics create keyboard on touchscreen to type name, 
        # display leaderboard


    elif data == "got it!":
        old_score = score
        data = arduino.readline().decode('utf-8').rstrip()
        print(data)
        score = int(data[11:])
        change = score - old_score
        sign = '+'
        print(f"{sign}{abs(change)} -----> new score = {score}")
        # TODO graphics display value change next to score

    elif data == "wrong rose :(":
        old_score = score
        data = arduino.readline().decode('utf-8').rstrip()
        print(data)
        score = int(data[11:])
        change = score - old_score
        sign = '-'
        print(f"{sign}{abs(change)} -----> new score = {score}")
        # TODO graphics display value change next to score

    elif data.isnumeric():
        elapsed_time = int(data)
        # TODO graphics use elapsed time to display timer 
        # game is 45 seconds but actually ends around 47 seconds? 