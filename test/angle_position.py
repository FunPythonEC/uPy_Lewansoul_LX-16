import lx16
import time
motor=lx16.lx16(22)
i=0
while i<=240:
    motor.goal_position(1,i,100)
    time.sleep(2)   
    i+=10