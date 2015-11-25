import tornado
import json
from lightwaverf.light import Light

file = "/var/light-schedules/config"
#file = "c:/temp/light-schedules"
template = {'global_enabled':False, 'timers': []}
panels = {"bedroom" : {"id": 1, "value": 0}}

class ScheduleHandler(tornado.web.RequestHandler):
    def initialize(self, scheduler):
        self.scheduler = scheduler

    def get(self):
        try:
            f = open(file, 'r')
            schedules = f.read();
            f.close()
        except IOError:
            schedules = json.dumps(template)
        self.write(schedules)

    def post(self):
        f = open(file, 'w')
        f.write(self.request.body)
        f.close()
        dict=json.loads(self.request.body)
        print dict
        for job in self.scheduler.get_jobs():
            self.scheduler.remove_job(job.id)
        for schedule in dict["timers"]:
            self.scheduler.add_job(
                self.update_light,
                'cron',
                day_of_week=",".join(schedule["days"]),
                hour=schedule["hour"],
                minute=schedule["min"],
                kwargs={"brightness":int(schedule["brightness"])}
            )
            print "Added job for " + schedule["hour"] + ":" + schedule["min"] + " on days " + ",".join(schedule["days"])

    def update_light(self, brightness):
        print("Updating light to " + str(brightness))
        light = Light()
        light.write_value(panels["bedroom"]["id"], brightness * 3)



