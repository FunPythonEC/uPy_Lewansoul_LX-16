from lx16 import lx16
import time

motor = lx16(22)
motor.servo_mode(1)
motor.goal_position(1, 0, 1000)
s = motor.read_vin(1, timeout=5, rtime=500)
print("trama recibida: " + str(s))
