import time
import uinput
import struct
import numpy
import time
import argparse
import serial

keys = (
    uinput.KEY_A,
    uinput.KEY_B,
    uinput.KEY_C,
    uinput.KEY_D,
    uinput.KEY_E,
    uinput.KEY_F,
    uinput.KEY_G,
    uinput.KEY_H,
    uinput.KEY_I,
    uinput.KEY_J,
    uinput.KEY_K,
    uinput.KEY_L,
    uinput.KEY_M,
    uinput.KEY_N,
    uinput.KEY_O,
    uinput.KEY_P,
    uinput.KEY_Q,
    uinput.KEY_R,
    uinput.KEY_S,
    uinput.KEY_T,
    uinput.KEY_U,
    uinput.KEY_V,
    uinput.KEY_W,
    uinput.KEY_X,
    uinput.KEY_Y,
    uinput.KEY_Z,
    uinput.KEY_1,
    uinput.KEY_2,
    uinput.KEY_3,
    uinput.KEY_4,
    uinput.KEY_5,
    uinput.KEY_6,
    uinput.KEY_7,
    uinput.KEY_8,
    uinput.KEY_9,
    uinput.KEY_0,
    uinput.KEY_F1,
    uinput.KEY_F2,
    uinput.KEY_F3,
    uinput.KEY_F4,
    uinput.KEY_F5,
    uinput.KEY_F6,
    uinput.KEY_F7,
    uinput.KEY_F8,
    uinput.KEY_F9,
    uinput.KEY_F10,
    uinput.KEY_F11,
    uinput.KEY_F12,
    uinput.KEY_HOME,
    uinput.KEY_UP,
    uinput.KEY_PAGEUP,
    uinput.KEY_LEFT,
    uinput.KEY_RIGHT,
    uinput.KEY_END,
    uinput.KEY_DOWN,
    uinput.KEY_PAGEDOWN,
    uinput.KEY_INSERT,
    uinput.KEY_DELETE
)

DEFAULT_DEVICE = '/dev/ttyUSB0'
NUMBER_OF_BYTES = 7

def main():
    parser = argparse.ArgumentParser(description='Test serial reading')
    parser.add_argument('--device', default=DEFAULT_DEVICE, help='path to serial device')
    # parser.add_argument('--device', dest='device', action='store_const', const='sum', default=DEFAULT_DEVICE, help='path to serial device')
    args = parser.parse_args()

    try:
        while True:
            try:
                ser = None
                ser = serial.Serial(args.device, 19200, timeout=5)
                print "Serial open: " + ser.name

                old_bits = numpy.zeros((NUMBER_OF_BYTES * 8), dtype=numpy.int8);
                with uinput.Device(events=keys, name="arduino-keyboard-translator") as device:
                    while True:
                        data = ""
                        while len(data) < NUMBER_OF_BYTES:
                            data += ser.read(NUMBER_OF_BYTES - len(data));

                        value = struct.unpack('B'*NUMBER_OF_BYTES, data)
                        a = numpy.array([[value]], dtype=numpy.uint8)
                        bits = numpy.unpackbits(a)
                        bits = numpy.array(bits, dtype=numpy.int8)
                        diff = old_bits - bits
                        
                        for i in xrange(1, bits.size):
                            val = diff[i]
                            if (val < 0):
                                # Button pressed
                                # print("Pressed button #" + str(i))
                                device.emit(keys[i], 1)
                            if (val > 0):
                                # Button released
                                # print("Released button #" + str(i))
                                device.emit(keys[i], 0)

                        old_bits = bits
            except serial.serialutil.SerialException:
                print "Something happened to the serial connection. Retrying in 1 sec..."
            time.sleep(1)

    except KeyboardInterrupt:
        print "KeyboardInterrupt caught, closing..."

    ser.close()

if __name__ == "__main__":
    main()
