import tornado
import json

class ScheduleHandler(tornado.web.RequestHandler):
    """ Handle getting and setting schedules  """

    def initialize(self, util):
        """
        :param util: A Data object
        :return:
        """
        self.util = util

    def get(self):
        self.write(json.dumps(self.util.get_schedules()))

    def post(self):
        schedules=json.loads(self.request.body)
        self.util.set_schedules(schedules)
        print schedules



