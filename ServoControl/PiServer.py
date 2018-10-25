#!usr/bin/python3

# Server Code - Runs on Pi and it gets data and processes it. Basically.

import RPi.GPIO as GPIO
import time
import threading
import socket


GPIO.setmode(GPIO.BOARD)

class Servo(threading.Thread):
    def __init__(self, BOARD_PIN, INIT_POS=0, FREQ=50):
        threading.Thread.__init__(self)
        self.pin = BOARD_PIN
        self.freq = FREQ
        GPIO.setup(self.pin, GPIO.OUT)
        self.obj = GPIO.PWM(self.pin, self.freq)
        self.obj.start(INIT_POS)
        self.daemon = True
        self.CDC = INIT_POS

    def run(self):
        while (True):
            self.obj.ChangeDutyCycle(self.CDC)
            time.sleep(0.01)

    def write(self, signal):
        # Signal lies between 0 to 1000
        print("{}     ".format(signal) ,end = '\r')
        self.CDC = 2.5 + ((signal / 1000) * 10)

    def halt(self):
        self.obj.stop()

    def __del__(self):
        self.obj.stop()


sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.bind(('0.0.0.0', 5550 ))
sock.listen(2)
conn , addr = sock.accept()
print("Connection From : {}".format(addr))

x = Servo(12)
x.start()

while(1):
    try:
        data = conn.recv(1024).decode()
        x.write(int(data,16))
    except KeyboardInterrupt:
        x.halt()
        break
    except ValueError:
        pass

conn.close()
GPIO.cleanup()