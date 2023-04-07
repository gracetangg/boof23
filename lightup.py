import board
import neopixel

PIN = board.D18              # digital 18 pin 
pixels = neopixel.NeoPixel(PIN, 10, auto_write=False)
pixels[0] = (10, 0, 0)
pixels[9] = (0, 10, 0)
pixels.show()

