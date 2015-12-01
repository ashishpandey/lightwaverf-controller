from lightwaverf.light import Light
from apscheduler.schedulers.tornado import TornadoScheduler
import json
import lightwaverf.lwrf
import pigpio
import math

class Util():
    """
    Manage setting and getting data, and updating the schedules and dimmer value
    """
    data = {'schedules': {'global_enabled': False, 'timers': []}, 'dimmer': 0}

    def __init__(self, filename, dimmer_id, gpio_pin, repeat):
        self.filename = filename
        self.dimmer_id = dimmer_id
        self.gpio_pin = gpio_pin
        self.repeat = repeat

        try:
            f = open(filename, 'r')
            self.data = json.loads(f.read());
            f.close()
        except IOError:
            # File doesn't exist, so we write the initial data dict from this class.
            self._save_data()

        self.scheduler = TornadoScheduler()
        self.scheduler.start()
        self._update_schedules()

        pi = pigpio.pi() # Connect to local Pi.
        self.lwrf_tx = lightwaverf.lwrf.tx(pi, self.gpio_pin) # Specify Pi, tx gpio, and baud.


    def get_schedules(self):
        """
        Returns a dict containing schedules
        :return: dict of schedules
        """
        return self.data['schedules'];

    def set_schedules(self, schedules):
        """
        Updates the schedules
        :param schedules:
        :return:
        """
        self.data['schedules'] = schedules;
        self._update_schedules()
        self._save_data()

    def get_dimmer_value(self):
        """
        Returns an int with the value of the dimmer
        :return: int
        """
        return self.data['dimmer']

    def set_dimmer_value(self, value):
        """
        Sets the dimmer value
        :param value: int
        :return: None
        """
        self.data['dimmer'] = value
        self._update_dimmer(value)
        self._save_data();

    def _save_data(self):
        """
        Saves the data to disk
        :return:
        """
        f = open(self.filename, 'w')
        f.write(json.dumps(self.data))
        f.close();


    def _update_schedules(self):
        """
        Updates the TornadoScheduler with the schedules in the class
        :return:
        """
        for job in self.scheduler.get_jobs():
            self.scheduler.remove_job(job.id)
        for schedule in self.data['schedules']["timers"]:
            self.scheduler.add_job(
                self._update_dimmer,
                'cron',
                day_of_week=",".join(schedule["days"]),
                hour=schedule["hour"],
                minute=schedule["min"],
                kwargs={"brightness":int(schedule["brightness"])}
            )
            print "Added job for " + schedule["hour"] + ":" + schedule["min"] + " on days " + ",".join(schedule["days"])

    def _update_dimmer(self, brightness):
        """
        Transmits the brightness to the dimmer panel
        :param brightness:
        :return:
        """
        print("Updating light to " + str(brightness))
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
        data = [a, b, 0, c, 15, self.dimmer_id, 0, 0, 0, 0]
        print(data)
        self.lwrf_tx.put(data, self.repeat)