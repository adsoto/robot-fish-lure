from microbit import *
import radio

radio.on()
radio.config(channel=7,length=64)

while True:

   packet = input()
   radio.send(packet)