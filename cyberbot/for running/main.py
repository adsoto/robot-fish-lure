#File used for flashing onto microbits. 
"""used to load programs onto the transmitter/reciever for microbit control. Make sure to open main.py
in a new window and copy/paste the program you want to flash (transmitter or reciever) into main.py.
Then flash main.py to the microbit - follow code documentation in the summer 2023 google drive"""

from microbit import *
import radio

radio.on()
radio.config(channel=7,length=64)

while True:

   packet = input()
   radio.send(packet)