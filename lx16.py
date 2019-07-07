
import machine as m
from time import sleep, sleep_ms, sleep_us

SERVO_ID_ALL = 0xfe

SERVO_MOVE_TIME_WRITE 			= 1
SERVO_MOVE_TIME_READ 			= 2
SERVO_MOVE_TIME_WAIT_WRITE 		= 7
SERVO_MOVE_TIME_WAIT_READ 		= 8
SERVO_MOVE_START 				= 11
SERVO_MOVE_STOP 				= 12
SERVO_ID_WRITE 					= 13
SERVO_ID_READ 					= 14
SERVO_ANGLE_OFFSET_ADJUST 		= 17
SERVO_ANGLE_OFFSET_WRITE 		= 18
SERVO_ANGLE_OFFSET_READ 		= 19
SERVO_ANGLE_LIMIT_WRITE 		= 20
SERVO_ANGLE_LIMIT_READ 			= 21
SERVO_VIN_LIMIT_WRITE 			= 22
SERVO_VIN_LIMIT_READ 			= 23
SERVO_TEMP_MAX_LIMIT_WRITE 		= 24
SERVO_TEMP_MAX_LIMIT_READ 		= 25
SERVO_TEMP_READ 				= 26
SERVO_VIN_READ 					= 27
SERVO_POS_READ 					= 28
SERVO_OR_MOTOR_MODE_WRITE 		= 29
SERVO_OR_MOTOR_MODE_READ 		= 30
SERVO_LOAD_OR_UNLOAD_WRITE 		= 31
SERVO_LOAD_OR_UNLOAD_READ 		= 32
SERVO_LED_CTRL_WRITE 			= 33
SERVO_LED_CTRL_READ 			= 34
SERVO_LED_ERROR_WRITE 			= 35
SERVO_LED_ERROR_READ 			= 36

SERVO_ERROR_OVER_TEMPERATURE 	= 1
SERVO_ERROR_OVER_VOLTAGE 		= 2
SERVO_ERROR_LOCKED_ROTOR 		= 4


header=[0x55,0x55]

class lx16(object):
	def __init__(self, dir_com, serialid=2):
		
		self.baudrate=115200
		self.serialid=serialid
		self.dir_com=m.Pin(dir_com,m.Pin.OUT)

		#definicion de objeto serial
		try:
			self.uart = m.UART(self.serialid,self.baudrate)
			self.uart.init(self.baudrate, bits=8, parity=None, stop=1)
		except Exception as e:
			print(e)


	def sendPacket(self, packet):
		self.dir_com.value(1)

		try:
			self.uart.write(bytearray(packet))
			a=utime.ticks_us()
		except Exception as e:
			print(e)

		time.sleep_us(325)
		self.dir_com.value(0)

		while True:
			msg=com.read()
			if msg is not None and (utime.ticks_us()-a)>=1450:
				print(list(msg))
				return list(msg)
			if (utime.ticks_us()-a)>=1450:
				break


#=======================WRITE METHODS===================
	def goal_position(self,ID,angle,time):
		packet=makePacket(ID,SERVO_MOVE_TIME_WRITE,le(angle*100/240)+le(time))
		self.uart.write(bytearray(packet))

	def start_goal_position(self,ID,angle,time):
		packet=makePacket(ID,SERVO_MOVE_TIME_WAIT_WRITE,le(angle*100/240)+le(time))
		self.uart.write(bytearray(packet))

	def start(self,ID):
		packet=makePacket(ID,SERVO_MOVE_START)
		self.uart.write(bytearray(packet))

	def stop(self,ID):
		packet=makePacket(ID,SERVO_MOVE_STOP)
		self.uart.write(bytearray(packet))

	def set_id(self,ID,NID):
		packet=makePacket(ID,SERVO_ID_WRITE,[NID])
		self.uart.write(bytearray(packet))

	def goal_speed(self,ID,speed):
		print(le(1)+le(speed))
		packet=makePacket(ID,SERVO_OR_MOTOR_MODE_WRITE,le(1)+le(speed))
		print(packet)
		self.uart.write(bytearray(packet))

	def servo_mode(self,ID):
		packet=makePacket(ID,SERVO_OR_MOTOR_MODE_WRITE,le(0)+le(0))
		self.uart.write(bytearray(packet))

def makePacket(ID, cmd, params=None):
	length=3+len(params)
	packet=[ID,length,cmd]+params
	print(packet)
	return header+packet+[checksum(packet)]

def le(h):
	"""
	Little-endian, takes a 16b number and returns an array arrange in little
	endian or [low_byte, high_byte].
	"""
	h &= 0xffff  # make sure it is 16 bits
	return [h & 0xff, h >> 8]

def word(l, h):
	"""
	Given a low and high bit, converts the number back into a word.
	"""
	return (h << 8) + l

def checksum(packet):
	return 255-(sum(packet) % 256)