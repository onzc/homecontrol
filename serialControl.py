import serial
import time


class SerialControl:
    baud = 9600
    port = 8
    open_delay = 1

    def send_single_message(self, msg):
        ser = serial.Serial(self.port, self.baud)  # open serial port
        time.sleep(1)
        s = ''
        while 'READY' not in s:
            s = ser.readline()
            print s

        print "sending"
        ser.write(msg)  # write a string
        print "sent"
        while "end" not in s:
            s = ser.readline()

        ser.close()  # close port

    def __init__(self):
        pass