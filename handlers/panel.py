import tornado
from lightwaverf.light import Light

panels = {"bedroom" : {"id": 1, "value": 0}}

class PanelHandler(tornado.web.RequestHandler):

    def get(self, panal):
        self.write("panel " + panal  + " is:" + str(panels[panal]))

    def post(self, panel):
        value = int(self.request.body)
        panels[panel]["value"] = value
        light = Light()
        light.write_value(panels[panel]["id"], value * 3)
        self.write("set " + str(panels[panel]["id"]) + " to " + str(value))


