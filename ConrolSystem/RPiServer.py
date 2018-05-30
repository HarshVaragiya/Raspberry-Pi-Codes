import RPi.GPIO as GPIO 
GPIO.setmode(GPIO.BOARD)
import socket    
import time
import threading

RUNTIME = 60 
# run for 60 seconds . change thread.daemon = False to run infinitely 
REFRESH_INTERVAL = 0.1

class Handler(threading.Thread):
    def __init__(self,pin,port,key):
        threading.Thread.__init__(self)
        self.daemon = True
        self.key_binded = key
        self.port = port
        self.pin = pin
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.s.bind(('0.0.0.0',self.port))
        GPIO.setup(self.pin,GPIO.OUT)
        GPIO.output(self.pin,False)
    def run(self):
        self.s.listen(5)
        self.conn,addr = self.s.accept()
        while(self.conn):
            self.string = self.conn.recv(1024).decode()
            print("-> "+str(self.string))
            if(self.string.count(self.key_binded)==len(self.string)):
                GPIO.output(self.pin,True)
                time.sleep(REFRESH_INTERVAL)                
            else:
                GPIO.output(self.pin,False)
    def __del__(self):
        GPIO.output(self.pin,False)
        self.s.close()
        self.is_alive =  False

w = Handler(11,5550,'w')
a = Handler(12,5551,'a')
s = Handler(13,5552,'s')
d = Handler(15,5553,'d')

w.start()
a.start()
s.start()
d.start()
time.sleep(RUNTIME)
