
#Servo x16 v1.0p test code

######################
#Notes
#Servos min=650 max=2300
servo_max = 650
servo_min = 2300

from machine import Pin, I2C
from pyb import CAN
import utime
import servo
#import pca9685

print("starting Servo x16 v1.1p test code")
print("v1.0")
print("initializing")
can = CAN(1, CAN.NORMAL)
can.setfilter(0, CAN.LIST16, 0, (123, 124, 125, 126))

#sleep to let pca9685 wake up
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
OE.value(0)

#Setup hbt timer
hbt_state = 0
hbt_interval = 500
start = utime.ticks_ms()
next_hbt = utime.ticks_add(start, hbt_interval)
HBT_LED.value(hbt_state)

#Setup pca9685
#pca = pca9685.PCA9685(i2c)
servos = servo.Servos(i2c)


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
    can.send('servoX16', 123)   # send a message with id 123
    
def get():
    mess = can.recv(0)
    print(mess)
    simple_test()    

def simple_test():
    move_all(servo_max)
    move_all(servo_min)
    
def move_all(us_delay):
    print("moving all servos to " + str(us_delay))
    for i in range(16):
        servos.position(i, us=us_delay)
        utime.sleep_ms(100)
    print("done")
        
while True:
    chk_hbt()
    if not (FUNC_BUTTON.value()):
        print("function button")
        send()
        simple_test()
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
        move_all(servo_min)
        utime.sleep_ms(200)    

    if not (RIGHT.value()):
        print("RIGHT button")
        move_all(servo_max)
        utime.sleep_ms(200)    

    if not (DPAD_PUSH.value()):
        print("DPAD_PUSH button")        
        utime.sleep_ms(200)    

    if(can.any(0)):
        get()
