from lightwaverf.light import Light
from apscheduler.schedulers.tornado import TornadoScheduler


class Scheduler():

    def __init__(self, schedules=None):
        self.scheduler = TornadoScheduler()
        self.scheduler.start()
        if schedules is not None:
            self.update(schedules)

    def update(self, schedules):
        for job in self.scheduler.get_jobs():
            self.scheduler.remove_job(job.id)
        for schedule in schedules["timers"]:
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
        Light().write_value(self.id, brightness * 3)
