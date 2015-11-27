import tornado

class DimmerHandler(tornado.web.RequestHandler):
    """ Handle setting instant values for the dimmer """

    def initialize(self, util):
        self.util = util

    def get(self):
        self.write(str(self.util.get_dimmer_value()))

    def post(self):
        value = int(self.request.body)
        self.util.set_dimmer_value(value)
        self.write("set dimmer to " + str(value))


