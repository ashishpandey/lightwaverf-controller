import json


class Data:
    data = {'schedules': {'global_enabled': False, 'timers': []}, 'dimmer': 0}

    def __init__(self, filename):
        try:
            self.filename = filename
            f = open(filename, 'r')
            self.data = json.loads(f.read());
            f.close()
        except IOError:
            self.write(self.data)

    def get_schedules(self):
        return self.data['schedules'];

    def set_schedules(self, schedules):
        self.data['schedules'] = schedules;
        self.write()

    def get_dimmer(self):
        return self.data['dimmer']

    def set_dimmer(self, value):
        self.data['dimmer'] = value
        self.write();

    def write(self):
        f = open(self.filename, 'w')
        f.write(json.dumps(self.data))
        f.close();