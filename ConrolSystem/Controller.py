import threading
import keyboard
import socket
import time 

RUNTIME = 60
# thread.daemon = False, for running always!
REFRESH_INTERVAL = 0.1
server_ip = '192.168.0.94'

class KeyHandler(threading.Thread):
    def __init__(self,key,port):
        threading.Thread.__init__(self)
        self.daemon = True
        self.key = key
        self.tx = str(self.key)
        self.port = port
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.s.connect((server_ip,self.port))
    def run(self):
        self.pressed = False
        while (1):
            if(keyboard.is_pressed(self.key)):
                self.transmit(1)
                self.pressed = True
            elif(self.pressed == True):
                self.pressed = False               
                self.transmit(0)
            time.sleep(REFRESH_INTERVAL)
    def transmit(self,value):
        if value == 1:
            self.s.send(self.tx.encode())
        else:
            self.s.send('X'.encode())

    def stop(self):
        self.is_alive = False
    def __del__(self):
        self.s.close()
        self.stop()

W = KeyHandler('w',5550)
A = KeyHandler('a',5551)
S = KeyHandler('s',5552)
D = KeyHandler('d',5553)
A.start()
W.start()
S.start()
D.start()
time.sleep(RUNTIME)
