
#Servo x16 v1.0p test code

from machine import Pin, I2C
from pyb import CAN
import utime
import pca9685

print("starting Servo x16 v1.0p test code")
print("v1.0")
print("initializing")
utime.sleep_ms(500)

i2c = I2C(2, freq=1000000)


#Setup Pins
HBT_LED = Pin("E8", Pin.OUT)
FUNC_BUTTON = Pin("SD_DETECT", Pin.IN, Pin.PULL_UP) 
NEO_STATUS = Pin("E7", Pin.OUT)

BUTTON_A = Pin("E4", Pin.IN, Pin.PULL_UP)
BUTTON_B = Pin("E5", Pin.IN, Pin.PULL_UP)

UP = Pin("E12", Pin.IN, Pin.PULL_UP)
DOWN = Pin("E10", Pin.IN, Pin.PULL_UP)
LEFT = Pin("E17", Pin.IN, Pin.PULL_UP)
RIGHT = Pin("E11", Pin.IN, Pin.PULL_UP)
DPAD_PUSH = Pin("E13", Pin.IN, Pin.PULL_UP)



#OE pin is the 'enable' pin for the outputs. ACTIVE LOW!
OE = Pin("E2", Pin.OUT)
OE.value(1)

#Setup hbt timer
hbt_state = 0
hbt_interval = 500
start = utime.ticks_ms()
next_hbt = utime.ticks_add(start, hbt_interval)
HBT_LED.value(hbt_state)

#Setup pca9685
pca = pca9685.PCA9685(i2c)



print("setup complete")


def chk_hbt():
    global next_hbt
    global hbt_state
    now = utime.ticks_ms()
    if utime.ticks_diff(next_hbt, now) <= 0:
        if hbt_state == 1:
            hbt_state = 0
            HBT_LED.value(hbt_state)
            #print("hbt")
        else:
            hbt_state = 1
            HBT_LED.value(hbt_state)  
        
        next_hbt = utime.ticks_add(next_hbt, hbt_interval)

def send():
    can.send('lowPrFET', 123)   # send a message with id 123
    
def get():
    mess = can.recv(0)
    print(mess)
    simple_test()        
        

while True:
    chk_hbt()
    if not (FUNC_BUTTON.value()):
        print("function button")        
        utime.sleep_ms(200)
        
    if not (BUTTON_A.value()):
        print("A button")        
        utime.sleep_ms(200)    

    if not (BUTTON_B.value()):
        print("B button")        
        utime.sleep_ms(200)    

    if not (UP.value()):
        print("UP button")        
        utime.sleep_ms(200)    

    if not (DOWN.value()):
        print("DOWN button")        
        utime.sleep_ms(200)    

    if not (LEFT.value()):
        print("LEFT button")        
        utime.sleep_ms(200)    

    if not (RIGHT.value()):
        print("RIGHT button")        
        utime.sleep_ms(200)    

    if not (DPAD_PUSH.value()):
        print("DPAD_PUSH button")        
        utime.sleep_ms(200)    

