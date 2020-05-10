import tornado

class DimmerHandler(tornado.web.RequestHandler):
    """ Handle setting instant values for the dimmer """

    def initialize(self, util):
        self.util = util

    def get(self, dimmer_id_str):
        dimmer_id = int(dimmer_id_str)
        self.write(str(self.util.get_dimmer_value(dimmer_id)))

    def post(self, dimmer_id_str):
        value = int(self.request.body)
        dimmer_id = int(dimmer_id_str)
        self.util.set_dimmer_value(dimmer_id, value)
        self.write("set dimmer " + dimmer_id + " to " + str(value))


