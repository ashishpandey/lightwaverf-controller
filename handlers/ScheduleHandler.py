import tornado
import json

class ScheduleHandler(tornado.web.RequestHandler):

    def initialize(self, scheduler, id, data):
        self.scheduler = scheduler
        self.id = id
        self.data = data


    def get(self):
        self.write(json.dumps(self.data.get_schedules()))

    def post(self):
        schedules=json.loads(self.request.body)
        self.data.set_schedules(schedules)
        self.scheduler.update(schedules)
        print schedules



