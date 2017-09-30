import struct
import numpy
import time
import argparse
import serial

default_device = '/dev/ttyUSB0'
number_of_bytes = 7

def main():
    parser = argparse.ArgumentParser(description='Test serial reading')
    parser.add_argument('--device', default=default_device, help='path to serial device')
    # parser.add_argument('--device', dest='device', action='store_const', const='sum', default=default_device, help='path to serial device')
    args = parser.parse_args()
    ser = serial.Serial(args.device)
    print('Serial open: ' + ser.name)
    try:
        old_bits = numpy.zeros((number_of_bytes * 8), dtype=numpy.int8);
        while True:
            data = ser.read(number_of_bytes);
            value = struct.unpack('B'*number_of_bytes, data)
            a = numpy.array([[value]], dtype=numpy.uint8)
            bits = numpy.unpackbits(a)
            bits = numpy.array(bits, dtype=numpy.int8)
            diff = old_bits - bits
            
            for i in xrange(1, bits.size):
                val = diff[i]
                if (val < 0):
                    print("Pressed button #" + str(i))
                if (val > 0):
                    print("Released button #" + str(i))

            old_bits = bits

    except KeyboardInterrupt:
        print "KeyboardInterrupt caught, closing..."

    ser.close()

if __name__ == "__main__":
    main()
