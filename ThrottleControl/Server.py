import socket
import threading
from PWMHandler import PWMPin
import time
import os
os.system('sudo pigpiod')

REFRESH_INTERVAL = 0.001
HALT_ALL = False

class Emergerncy(threading.Thread):
    def __init__(self,port):
        threading.Thread.__init__(self)
        self.port = port
        self.daemon = False
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.s.bind(('0.0.0.0',self.port))
    def run(self):
        global HALT_ALL
        while 1:
            self.s.listen()
            conn , addr = self.s.accept()
            while(conn):
                self.string = conn.recv(8).decode('utf-8')
                if self.string.count('q') >= 1:
                    self.s.close()
                    HALT_ALL = True
X = Emergerncy(5520)
X.start()
class Throttle(threading.Thread):
    def __init__(self, pin, port, up_key, down_key):
        threading.Thread.__init__(self)
        self.pin = pin
        self.port = port
        self.up_key = up_key
        self.down_key = down_key
        self.Throttle_Value = 0
        self.PWMObj = PWMPin(self.pin, res=255, start_val=0)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(('0.0.0.0', self.port))

    def run(self):
        global HALT_ALL
        self.s.listen(1)
        self.conn , self.addr = self.s.accept()
        print('Incoming Connection From : ' + str(self.addr))
        self.PWMObj.start()
        while (self.conn):
            self.string = self.conn.recv(1).decode()
            print(self.Throttle_Value)
            self.Throttle_Value = self.Throttle_Value + self.string.count(self.up_key) - self.string.count(self.down_key)
            if self.Throttle_Value < 0:
                self.Throttle_Value = 0
            elif self.Throttle_Value > 255:
                self.Throttle_Value = 255
            if HALT_ALL == True:
                self.Halt()
                exit(-1)
            self.PWMObj.change_duty_cycle(self.Throttle_Value)
            time.sleep(REFRESH_INTERVAL)

    def Halt(self):
        self.PWMObj.change_duty_cycle(0)

    def __del__(self):
        self.PWMObj.change_duty_cycle(0)
        self.s.close()
        self.Halt()

a = Throttle(13,5585,'w','s')
a.start()
