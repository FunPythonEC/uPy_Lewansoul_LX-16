import machine as m  # needed so that uart can be used
from time import sleep, sleep_ms, sleep_us  # in case any delay is needed
import utime

# every command available for the servo
SERVO_ID_ALL = 0xFE
SERVO_MOVE_TIME_WRITE = 1
SERVO_MOVE_TIME_READ = 2
SERVO_MOVE_TIME_WAIT_WRITE = 7
SERVO_MOVE_TIME_WAIT_READ = 8
SERVO_MOVE_START = 11
SERVO_MOVE_STOP = 12
SERVO_ID_WRITE = 13
SERVO_ID_READ = 14
SERVO_ANGLE_OFFSET_ADJUST = 17
SERVO_ANGLE_OFFSET_WRITE = 18
SERVO_ANGLE_OFFSET_READ = 19
SERVO_ANGLE_LIMIT_WRITE = 20
SERVO_ANGLE_LIMIT_READ = 21
SERVO_VIN_LIMIT_WRITE = 22
SERVO_VIN_LIMIT_READ = 23
SERVO_TEMP_MAX_LIMIT_WRITE = 24
SERVO_TEMP_MAX_LIMIT_READ = 25
SERVO_TEMP_READ = 26
SERVO_VIN_READ = 27
SERVO_POS_READ = 28
SERVO_OR_MOTOR_MODE_WRITE = 29
SERVO_OR_MOTOR_MODE_READ = 30
SERVO_LOAD_OR_UNLOAD_WRITE = 31
SERVO_LOAD_OR_UNLOAD_READ = 32
SERVO_LED_CTRL_WRITE = 33
SERVO_LED_CTRL_READ = 34
SERVO_LED_ERROR_WRITE = 35
SERVO_LED_ERROR_READ = 36

SERVO_ERROR_OVER_TEMPERATURE = 1
SERVO_ERROR_OVER_VOLTAGE = 2
SERVO_ERROR_LOCKED_ROTOR = 4


header = [0x55, 0x55]  # defined to be used later (initials of the packet)


class lx16(object):

    # constructor
    # default uart used in serialid, especified for esp32
    def __init__(self, dir_com, serialid=2):

        self.baudrate = 115200  # only baudrate avaiable for the servo
        self.serialid = serialid
        self.dir_com = m.Pin(dir_com, m.Pin.OUT)

        # uart defined
        try:
            self.uart = m.UART(self.serialid, self.baudrate)
            self.uart.init(self.baudrate, bits=8, parity=None, stop=1, txbuf=0)
        except Exception as e:
            print(e)

    # =======================WRITE METHODS===================
    # every writing method is here
    def goal_position(self, ID, angle, time, rxbuf=15, timeout=2500, rtime=850):
        sendPacket(
            bytearray(
                makePacket(
                    ID,
                    SERVO_MOVE_TIME_WRITE,
                    le(int(angle * 1000 / 240)) + le(int(time)),
                )
            ),
            self.uart,
            self.dir_com,
            rtime,
            rxbuf,
            timeout,
        )

    def start_goal_position(self, ID, angle, time, rxbuf=15, timeout=2500, rtime=850):
        sendPacket(
            bytearray(
                makePacket(
                    ID,
                    SERVO_MOVE_TIME_WAIT_WRITE,
                    le(int(angle * 1000 / 240)) + le(int(time)),
                )
            ),
            self.uart,
            self.dir_com,
            rtime,
            rxbuf,
            timeout,
        )

    def start(self, ID, rxbuf=15, timeout=5, rtime=850):
        sendPacket(
            bytearray(makePacket(ID, SERVO_MOVE_START)),
            self.uart,
            self.dir_com,
            rtime,
            rxbuf,
            timeout,
        )

    def stop(self, ID, rxbuf=15, timeout=5, rtime=850):
        sendPacket(
            bytearray(makePacket(ID, SERVO_MOVE_STOP)),
            self.uart,
            self.dir_com,
            rtime,
            rxbuf,
            timeout,
        )

    def set_id(self, ID, NID, rxbuf=15, timeout=5, rtime=850):
        sendPacket(
            bytearray(makePacket(ID, SERVO_ID_WRITE, [NID])),
            self.uart,
            self.dir_com,
            rtime,
            rxbuf,
            timeout,
        )

    def set_temp_offset_angle(self, ID, angle, rxbuf=15, timeout=5, rtime=850):
        sendPacket(
            bytearray(
                makePacket(ID, SERVO_ANGLE_OFFSET_ADJUST, [int(angle / 30 * 125)])
            ),
            self.uart,
            self.dir_com,
            rtime,
            rxbuf,
            timeout,
        )

    def set_offset_angle(self, ID, angle, rxbuf=15, timeout=5, rtime=850):
        sendPacket(
            bytearray(
                makePacket(ID, SERVO_ANGLE_OFFSET_WRITE, [int(angle / 30 * 125)])
            ),
            self.uart,
            self.dir_com,
            rtime,
            rxbuf,
            timeout,
        )

    def set_angle_limit(self, ID, minangle, maxangle, rxbuf=15, timeout=5, rtime=850):
        sendPacket(
            bytearray(
                makePacket(
                    ID,
                    SERVO_ANGLE_LIMIT_WRITE,
                    le(int(minangle / 240 * 1000)) + le(int(maxangle / 240 * 1000)),
                )
            ),
            self.uart,
            self.dir_com,
            rtime,
            rxbuf,
            timeout,
        )

    def set_vin_limit(self, ID, minvin, maxvin, rxbuf=15, timeout=5, rtime=850):
        sendPacket(
            bytearray(makePacket(ID, SERVO_VIN_LIMIT_WRITE, le(minvin) + le(maxvin))),
            self.uart,
            self.dir_com,
            rtime,
            rxbuf,
            timeout,
        )

    def set_max_temp_limit(self, ID, temp, rxbuf=15, timeout=5, rtime=850):
        sendPacket(
            bytearray(makePacket(ID, SERVO_TEMP_MAX_LIMIT_WRITE, [temp])),
            self.uart,
            self.dir_com,
            rtime,
            rxbuf,
            timeout,
        )

    def set_load_status(self, ID, status, rxbuf=15, timeout=5, rtime=850):
        sendPacket(
            bytearray(makePacket(ID, SERVO_LOAD_OR_UNLOAD_WRITE, [status])),
            self.uart,
            self.dir_com,
            rtime,
            rxbuf,
            timeout,
        )

    def set_led_ctrl(self, ID, mode, rxbuf=15, timeout=5, rtime=850):
        sendPacket(
            bytearray(makePacket(ID, SERVO_LED_CTRL_WRITE, [mode])),
            self.uart,
            self.dir_com,
            rtime,
            rxbuf,
            timeout,
        )

    def set_led_error(self, ID, fault, rxbuf=15, timeout=5, rtime=850):
        sendPacket(
            bytearray(makePacket(ID, SERVO_LED_ERROR_WRITE, [fault])),
            self.uart,
            self.dir_com,
            rtime,
            rxbuf,
            timeout,
        )

    def goal_speed(self, ID, speed, rxbuf=15, timeout=5, rtime=850):
        sendPacket(
            bytearray(makePacket(ID, SERVO_OR_MOTOR_MODE_WRITE, le(1) + le(speed))),
            self.uart,
            self.dir_com,
            rtime,
            rxbuf,
            timeout,
        )

    def joint_mode(self, ID, rxbuf=15, timeout=5, rtime=850):
        sendPacket(
            bytearray(makePacket(ID, SERVO_OR_MOTOR_MODE_WRITE, le(0) + le(0))),
            self.uart,
            self.dir_com,
            rtime,
            rxbuf,
            timeout,
        )

    # =======================READ METHODS===================
    # every reading method is here

    def read_goal_position(self, ID, rxbuf=15, timeout=5, rtime=500):
        resp = sendPacket(
            bytearray(makePacket(ID, SERVO_MOVE_TIME_READ)),
            self.uart,
            self.dir_com,
            rtime,
            rxbuf,
            timeout,
        )
        return resp

    def read_wait_goal_position(self, ID, rxbuf=15, timeout=5, rtime=500):
        resp = sendPacket(
            bytearray(makePacket(ID, SERVO_MOVE_TIME_WAIT_READ)),
            self.uart,
            self.dir_com,
            rtime,
            rxbuf,
            timeout,
        )
        return resp

    def read_id(self, ID, rxbuf=15, timeout=5, rtime=500):
        resp = sendPacket(
            bytearray(makePacket(ID, SERVO_ID_READ)),
            self.uart,
            self.dir_com,
            rtime,
            rxbuf,
            timeout,
        )
        return resp

    def read_angle_offset(self, ID, rxbuf=15, timeout=5, rtime=500):
        resp = sendPacket(
            bytearray(makePacket(ID, SERVO_ANGLE_OFFSET_READ)),
            self.uart,
            self.dir_com,
            rtime,
            rxbuf,
            timeout,
        )
        return resp

    def read_angle_limit(self, ID, rxbuf=15, timeout=5, rtime=500):
        resp = sendPacket(
            bytearray(makePacket(ID, SERVO_ANGLE_LIMIT_READ)),
            self.uart,
            self.dir_com,
            rtime,
            rxbuf,
            timeout,
        )
        return resp

    def read_vin_limit(self, ID, rxbuf=15, timeout=5, rtime=500):
        resp = sendPacket(
            bytearray(makePacket(ID, SERVO_VIN_LIMIT_READ)),
            self.uart,
            self.dir_com,
            rtime,
            rxbuf,
            timeout,
        )
        return resp

    def read_temp_max_limit(self, ID, rxbuf=15, timeout=5, rtime=500):
        resp = sendPacket(
            bytearray(makePacket(ID, SERVO_TEMP_MAX_LIMIT_READ)),
            self.uart,
            self.dir_com,
            rtime,
            rxbuf,
            timeout,
        )
        return resp

    def read_temp(self, ID, rxbuf=15, timeout=5, rtime=500):
        resp = sendPacket(
            bytearray(makePacket(ID, SERVO_TEMP_READ)),
            self.uart,
            self.dir_com,
            rtime,
            rxbuf,
            timeout,
        )
        return resp

    def read_vin(self, ID, rxbuf=15, timeout=5, rtime=500):
        resp = sendPacket(
            bytearray(makePacket(ID, SERVO_VIN_READ)),
            self.uart,
            self.dir_com,
            rtime,
            rxbuf,
            timeout,
        )
        return resp

    def read_pos(self, ID, rxbuf=15, timeout=5, rtime=500):
        resp = sendPacket(
            bytearray(makePacket(ID, SERVO_POS_READ)),
            self.uart,
            self.dir_com,
            rtime,
            rxbuf,
            timeout,
        )
        return resp

    def read_servo_mode(self, ID, rxbuf=15, timeout=5, rtime=500):
        resp = sendPacket(
            bytearray(makePacket(ID, SERVO_OR_MOTOR_MODE_READ)),
            self.uart,
            self.dir_com,
            rtime,
            rxbuf,
            timeout,
        )
        return resp

    def read_load_status(self, ID, rxbuf=15, timeout=5, rtime=500):
        resp = sendPacket(
            bytearray(makePacket(ID, SERVO_LOAD_OR_UNLOAD_READ)),
            self.uart,
            self.dir_com,
            rtime,
            rxbuf,
            timeout,
        )
        return resp

    def read_led_ctrl(self, ID, rxbuf=15, timeout=5, rtime=500):
        resp = sendPacket(
            bytearray(makePacket(ID, SERVO_LED_CTRL_READ)),
            self.uart,
            self.dir_com,
            rtime,
            rxbuf,
            timeout,
        )
        return resp

    def read_led_error(self, ID, rxbuf=15, timeout=5, rtime=500):
        resp = sendPacket(
            bytearray(makePacket(ID, SERVO_LED_ERROR_READ)),
            self.uart,
            self.dir_com,
            rtime,
            rxbuf,
            timeout,
        )
        return resp


def sendPacket(packet, uart, dir_com, rtime, rxbuf, timeout):
    dir_com.on()  # turn on so packet is sent
    uart.write(packet)

    # time is traced in order to know when to listen
    tinit = utime.ticks_us()
    while (utime.ticks_us() - tinit) < rtime:
        pass

    dir_com.off()  # off to receive packet

    tinit = utime.ticks_ms()
    while (utime.ticks_ms() - tinit) < timeout:  # timeout of 1600us
        resp = uart.read(rxbuf)
        if resp is not None:
            return list(resp)
    return None


def makePacket(ID, cmd, params=None):
    if params:
        length = 3 + len(params)
        packet = [ID, length, cmd] + params
    else:
        length = 3
        packet = [ID, length, cmd]
    packet = header + packet + [checksum(packet)]
    return packet


def le(h):
    """
	Little-endian, takes a 16b number and returns an array arrange in little
	endian or [low_byte, high_byte].
	"""
    h &= 0xFFFF  # make sure it is 16 bits
    return [h & 0xFF, h >> 8]


def word(l, h):
    """
	Given a low and high bit, converts the number back into a word.
	"""
    return (h << 8) + l


def checksum(packet):
    return 255 - (sum(packet) % 256)
