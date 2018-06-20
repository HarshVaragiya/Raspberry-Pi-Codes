import socket
import threading
import pigpio


class PWMPin(threading.Thread):

    def __init__(self, pin, res=255, start_val=0):
        threading.Thread.__init__(self)
        self.daemon = True
        self.pin = pin
        self.pi = pigpio.pi()
        self.pi.write(self.pin, 0)
        self.dutycycle = start_val
        self.min_val = 0
        self.max_val = res
        self.pi.set_PWM_range(self.pin,self.max_val)

    def run(self):

        while True:

            try:
                self.pi.set_PWM_dutycycle(self.pin, self.dutycycle)
            except:
                print("Error Occurred! ")

    def change_duty_cycle(self, D):
        if D > self.max_val:
            self.dutycycle = self.max_val
        elif D < self.min_val:
            self.dutycycle = self.min_val
        else:
            self.dutycycle = D

    def get_duty_cycle(self):
        return self.dutycycle

    def __del__(self):
        self.Halt()

    def Halt(self):
        self.is_alive = False
