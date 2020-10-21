from lx16 import *
import time

motor = lx16(22)
motor.joint_mode(1)
i = 0
while i <= 240:
    motor.goal_position(1, i, 800)
    s = motor.read_pos(1)
    print("Posición pedida: ", str(i))
    print("Posición verdadera: ", str(word(s[5], s[6]) * 240 / 1000))
    i += 10
