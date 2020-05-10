import tornado

class DimmerHandler(tornado.web.RequestHandler):
    """ Handle setting instant values for the dimmer """

    def initialize(self, util):
        self.util = util

    def get(self, dimmer_id):
        self.write(str(self.util.get_dimmer_value(dimmer_id)))

    def post(self, dimmer_id):
        value = int(self.request.body)
        self.util.set_dimmer_value(dimmer_id, value)
        self.write("set dimmer " + dimmer_id + " to " + str(value))


