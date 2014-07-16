#! /usr/bin/env python2.7
import serial
import sys
import threading
import argparse

def sending(seri):
    while True:
        blah = raw_input().strip()
        seri.write(blah)
        seri.flush()

def receiving(seri):
    while True:
        s = seri.read(1000000)
        sys.stdout.write(s)
        sys.stdout.flush()

parser = argparse.ArgumentParser(description="Simple Serial reader / writer")
parser.add_argument('-s', '--serial', dest='serial_port',
        default="/dev/cu.usbmodem1421", help='the serial communication port')
parser.add_argument('-b', '--baudrate', dest='baud_rate',
        default='9600', help='baud rate for the serial communication')
args = parser.parse_args()

try:
    # This is here because of an error in my laptop serial stack or whatever
    ser = serial.Serial(args.serial_port, 9600, timeout=0)
    ser.close()
    ser = serial.Serial(args.serial_port, 115200, timeout=0)
except:
    print("serial open failure")

t1 = threading.Thread(target=sending, args = (ser))
t1.daemon = True
t1.start()
try:
    receiving(ser)
except (KeyboardInterrupt, SystemExit):
    print("I Die")
    pass
finally:
    # raise
    ser.close()
