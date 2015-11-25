import tornado
from lightwaverf.light import Light

class DimmerHandler(tornado.web.RequestHandler):
    """ Handle setting instant values for the dimmer """

    def initialize(self, id, data):
        self.id = id;
        self.data = data
        self.value = 0;

    def get(self):
        self.write(str(self.data.get_dimmer()))

    def post(self):
        value = int(self.request.body)
        self.data.set_dimmer(value)
        light = Light().write_value(self.id, value * 3)
        self.write("set " + str(self.id) + " to " + str(value))


