import lwrf
import pigpio
import math


class Light:
    gpio_pin = 7
    repeat = 3

    def __init__(self):
       self.pi = pigpio.pi() # Connect to local Pi.
       self.tx = lwrf.tx(self.pi, self.gpio_pin) # Specify Pi, tx gpio, and baud.

    def write_value(self, id, value):
        # param1, param2, device, command
        if (value == 0):
            value = 64 # according to the LightwaveRF docs, when turning off, this should be 64.
            c = 0 # "command" setting i.e. on/off
        else:
            value += 128
            c = 1
        a = value >> 4  # first 4 bits
        b = value % 16  # last 4 bits
        data = [a, b, 0, c, 15, id, 5, 10, 12, 2]
        print(data)
        self.tx.put(data, 3)

