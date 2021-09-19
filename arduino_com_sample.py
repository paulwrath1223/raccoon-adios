# Importing Libraries
import serial
import time
arduino = serial.Serial(port='COM4', baudrate=115200, timeout=.1)


def write_read(message):
    arduino.write(bytes(message, 'utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    return data


def set_pos(x, y):
    value = write_read(x)
    if value == "x":
        value = write_read(y)
        if value != "y":
            raise Exception("arduino did not acknowledge y target")
    else:
        raise Exception("arduino did not acknowledge x target")
