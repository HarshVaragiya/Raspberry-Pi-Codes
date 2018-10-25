#!usr/bin/python3

# Client Code that Runs on PC and gives servo position control to the user over Keyboard

import keyboard
import socket
import time

PORT = 5550
INTERVAL = 2
MAX = 830
MIN = 0x00

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.connect(('192.168.0.94',PORT))

pos = 0

print("KeyMap :")
print("W - Increase Slowly ")
print("S - Decrease Slowly ")
print("A - Max Position    ")
print("D - Min Position    ")
print("T - Position ++     ")
print("G - Position --     ")

while(1):
    try:
        if keyboard.is_pressed('t'):
            pos += 100
        if keyboard.is_pressed('g'):
            pos -= 100

        if keyboard.is_pressed('w'):
            pos += INTERVAL
        if keyboard.is_pressed('s'):
            pos -= INTERVAL
        if keyboard.is_pressed('a'):
            pos = MAX
        if keyboard.is_pressed('d'):
            pos = MIN

        if(pos > MAX):
            pos = MAX
        if(pos < MIN):
            pos = MIN

        sock.send(hex(pos).encode())
        print(" POS : {}     ".format(pos),end='\r')
        time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nEnding!")
        sock.send(str('000').encode())
        break

sock.close()