import serial
import time

# SENDING COMMANDS OVER SERIAL PORT

def go(ser):
    send_commands(ser, 64, 64)
    time.sleep(3)

def turn(ser):
    send_commands(ser, 64, -64)
    time.sleep(2.4)

def stop(ser):
    send_commands(ser, 0, 0)
    time.sleep(3)

def send_commands(ser, vL, vR):
    dict = {'vL': vL, 'vR' : vR}
    packet = str(dict) + "\r"
    ser.write(packet.encode())

# change to whatever serial port is connected to the transmitting robot
# find the port with: ls /dev/tty.* (or cu or usb instead of tty)
ser = serial.Serial('/dev/tty.usbmodem14202', baudrate=115200)

go(ser)
ser.close()