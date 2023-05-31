#File to flash onto transmitter microbit. Paste into main.py as needed. Use summer 2023 code documentation

from microbit import *
import radio

radio.on()
radio.config(channel=7,length=64)

while True:

   packet = input()
   radio.send(packet)