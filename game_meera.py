import serial
import time
from serial import Serial
arduino = serial.Serial(port='/dev/cu.usbmodem1413301', baudrate=9600, timeout=.1)


# def write_read(x):
#     arduino.write(bytes(x, 'utf-8'))
#     time.sleep(0.05)
#     data = arduino.readline()
#     return data


# while True:
#     num = input("Enter a number: ")
#     value = write_read(num)
#     print(value)

leaderboard = []

while True:
    data = arduino.readline().decode('utf-8').rstrip()
    if data != '':
        print(data)

    if data == "restart?":
        val = input()
        if val == 'r':
            arduino.write(bytes(val, 'utf-8'))
    
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
            # leaderboard = dict(sorted(leaderboard, reverse = True))
        print(leaderboard)