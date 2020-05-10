from lightwaverf.light import Light
import json
import lightwaverf.lwrf
import pigpio
import math
import threading

class Util():
    """
    Manage setting and getting data, and updating the schedules and dimmer value
    """
    data = {'dimmer': { '1': 0, '2': 0 } }

    def __init__(self, filename, dimmer_id, gpio_pin, repeat):
        self.filename = filename
        self.gpio_pin = gpio_pin
        self.repeat = repeat
        self.lock = threading.Lock()

        try:
            f = open(filename, 'r')
            self.data = json.loads(f.read());
            f.close()
        except IOError:
            # File doesn't exist, so we write the initial data dict from this class.
            self._save_data()

        pi = pigpio.pi() # Connect to local Pi.
        self.lwrf_tx = lightwaverf.lwrf.tx(pi, self.gpio_pin) # Specify Pi, tx gpio, and baud.

    def get_dimmer_value(self, dimmer_id):
        """
        Returns an int with the value of the dimmer
        :return: int
        """
        return self.data['dimmer'][str(dimmer_id)]

    def set_dimmer_value(self, dimmer_id, value):
        """
        Sets the dimmer value
        :param value: int
        :return: None
        """
        self.data['dimmer'][str(dimmer_id)] = value
        self._update_dimmer(dimmer_id, value)
        self._save_data();

    def _save_data(self):
        """
        Saves the data to disk
        :return:
        """
        with self.lock:
            f = open(self.filename, 'w')
            f.write(json.dumps(self.data))
            f.close();

    def _update_dimmer(self, dimmer_id, brightness):
        """
        Transmits the brightness to the dimmer panel
        :param dimmer_id:
        :param brightness:
        :return:
        """
        print("Updating dimmer " + str(dimmer_id) + " to " + str(brightness))
        value = brightness * 3
        # param1, param2, device, command
        if (value == 0):
            value = 64 # according to the LightwaveRF docs, when turning off, this should be 64.
            c = 0 # "command" setting i.e. on/off
        else:
            value += 128
            c = 1
        a = value >> 4  # first 4 bits
        b = value % 16  # last 4 bits
        data = [a, b, 0, c, 15, dimmer_id, 0, 0, 0, 0]
        print(data)
        with self.lock:
            self.lwrf_tx.put(data, self.repeat)
