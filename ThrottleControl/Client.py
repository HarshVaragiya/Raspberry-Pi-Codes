import socket
import threading
import keyboard
import time 

HOST_IP = '192.168.0.94'
REFRESH_INTERVAL = 0.0015
class EMHandler(threading.Thread):
    def __init__(self,port,quit_key):
        threading.Thread.__init__(self)
        self.quit_key = quit_key
        self.port = port
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.s.connect((HOST_IP,self.port))
    def run(self):
        while 1:
            if(keyboard.is_pressed(self.quit_key)):
                self.s.send(self.quit_key.encode('utf-8'))
    def __del__(self):
        self.s.close()
        self.is_alive = False
X = EMHandler(5520,'q')
X.start()
class MotorControl(threading.Thread):
    def __init__(self,port,up_key,down_key):
        threading.Thread.__init__(self)
        global HOST_IP
        self.port = port
        self.up_key= up_key
        self.down_key = down_key
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.s.connect((HOST_IP,self.port))
    def run(self):
        while True:
            if keyboard.is_pressed(self.up_key):
                self.s.send(self.up_key.encode('utf-8'))
            if keyboard.is_pressed(self.down_key):
                self.s.send(self.down_key.encode('utf-8'))
            time.sleep(REFRESH_INTERVAL)

    def Halt(self):
        self.is_alive = False

    def __del__(self):
        self.s.close()
        self.Halt()

a = MotorControl(5585,'w','s')
a.start()
