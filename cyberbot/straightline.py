#File to flash onto reciever microbit. Paste into main.py as needed. Use summer 2023 code documentation

# hard coded straight line robot movement
from microbit import *
from cyberbot import *
from feedback360 import *
import radio

radio.on()
radio.config(channel=7,length=64)
drive.connect()

# arbitrarily chosen speeds and sleep times. 
x = 0
while x < 1:
    sleep(3000) # wait 3 secs after turning on
    drive.speed(20, 20) # drive forward at setting of 20 
    sleep(4000) # maintain speed for 4 seconds
    drive.speed(0,0) # stop wheels
    sleep(1000) # wait for 1 second
    x += 1


