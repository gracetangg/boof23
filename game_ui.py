import serial

"""
button_press -> start game, send signal to UI
    - UI listen to serial output: current_score
    - arduino handles game, on score change serial write new score (or just added score???)
        - near finish (some timer warning) send signal for evil queen display
        - on finish, arduino sends game over signal, python finishes score, does score board
"""
PORT_NAME = '/dev/cu.usbmodem101'
BAUD_RATE = 9600
TIMEOUT = 0.1

GAME_START = "start"
GAME_WARNING = "warning"
GAME_FINISH = "finish"

class RedQueen():
    def __init__(self):
        self.arduino = serial.Serial(PORT_NAME, BAUD_RATE, timeout=TIMEOUT)
        self.leaderboard = []
        self.game_active = False

    def listen(self):
        """
        Returns anything on the serial port as string
        """
        rawdata = self.arduino.readline()
        data = str(rawdata.decode('utf-8')).strip()
        return data

    def idle(self):
        """
        Listen for arduino to send game start from serial
        """
        while True: 
            data = self.listen()
            if data == GAME_START:
                self.start_game()

    def start_game(self):
        """
        Listens for new scores to update current score, return successful exit of game
        """
        current_score = 0
        while True:
            data = self.listen()
            if data == GAME_WARNING:
                # display red queen coming 
                print('5 SECONDS LEFT')
                pass 
            elif data == GAME_FINISH:
                print(f'FINISHED: your score was {current_score}')
                return True
            elif data:
                data = int(data)
                current_score += data 
                print(f'current score: {current_score}')
        return False


def main():
    game = RedQueen()
    game.idle()


if __name__ == "__main__":
    main()