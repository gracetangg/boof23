import serial

port_name = '/dev/cu.usbmodem101'
baud_rate = 9600
arduino = serial.Serial(port_name, 9600, timeout=0.1) 

def main():
    start = input("start? ")
    if start == 'y': 
        print("YES")
        arduino.write(bytes(start, 'utf-8'))
    while True: 
        rawdata = arduino.readline()
        data = str(rawdata.decode('utf-8'))
        if data:
            print(data)

if __name__ == "__main__":
    main()