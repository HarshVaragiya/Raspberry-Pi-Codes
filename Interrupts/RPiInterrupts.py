import RPi.GPIO as GPIO
import threading
import time

# Change for different Pin Config
GPIO.setmode(GPIO.BCM)

def process_pin_data(PIN):
    # basically the pin check function for the deamon thread
    # change for different checking condition
    return GPIO.input(4)

interrupt_thread_count = 0 
threads = []

class NewThread(threading.Thread):
    def __init__(self,id,PIN,FUNC,SIGNAL_DEF,time_delay=0):
        threading.Thread.__init__(self)
        self.threadID = id
        self.Target_Pin = PIN
        self.action = FUNC
        if SIGNAL_DEF == "RISING":
            self.trigger = True
        elif SIGNAL_DEF == "FALLING":
            self.trigger = False
        else:                                                                   # custom definition 
            pass
        self.time_delay = time_delay
        GPIO.setup(self.Target_Pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)        #pull_up or pull_down change...
        print("Attached Software Timer Interrupt!")

    def run(self):
        while(True):
            if(process_pin_data(self.Target_Pin) == self.trigger):
                self.action()
            time.sleep(self.time_delay)
              
    def return_thread_id(self):
        return self.threadID

    def stop(self):
        self.is_alive = False

def attachInterrupt(Pin,Function,Signal,frequency=-1):
    global interrupt_thread_count
    global threads
    time_delay_calculated = 0
    if(frequency != -1):
        time_delay_calculated = float(1/frequency)
    try:
        SpawnedThread = NewThread(interrupt_thread_count,Pin,Function,Signal,time_delay_calculated)
        SpawnedThread.daemon = True
        SpawnedThread.start()
        threads.append(SpawnedThread)
        interrupt_thread_count +=1
        return SpawnedThread.return_thread_id()
    except:
        print("Unable to Attach Software Interrupt!")
        return -1
        
def detatchInterrupt(threadId):
    for thread in threads:
        if (threadId == thread.return_thread_id()):
            thread.stop()
            threads.remove(thread)
            return 1    # if thread is stopped
    return -1           # if thread ID is not found .

def detatchAllInterrupts():
    for thread in threads:
        thread.stop()
    return 1

# attachInterrupt(Pin, Function ,Signal)  #optional a frequency argument to specify the scanning frequency 
# just like in arduino :p but on each pin :p 
