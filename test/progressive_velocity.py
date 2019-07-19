from lx16 import lx16
import time
motor=lx16(22)
i=0

while i<=1000:
    motor.goal_speed(2,i)
    i+=50
    time.sleep(1)
    
    