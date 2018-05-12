import time
from RPiInterrupts import attachInterrupt,detatchAllInterrupts

def invoke():
     # Do Something !
    print(" Software Timer -> Interrupt Occoured! ")


attachInterrupt(0,invoke,"RISING",2)
time.sleep(5)
detatchAllInterrupts()