#!/usr/bin/python
from datetime import datetime
import tornado.ioloop
import tornado.web
import os
from handlers.panel import PanelHandler
from handlers.schedules import ScheduleHandler
from apscheduler.schedulers.tornado import TornadoScheduler



scheduler = TornadoScheduler()
scheduler.start()

cwd =  os.path.dirname(os.path.realpath(__file__))
application = tornado.web.Application([
    (r"/api/panel/(.*)", PanelHandler),
    (r"/api/schedules", ScheduleHandler, dict(scheduler=scheduler)),
    (r'/(.*)', tornado.web.StaticFileHandler, {'path': cwd + '/static', "default_filename":"index.html"}),
])


application.listen(88)
print "Started"
try:
    tornado.ioloop.IOLoop.instance().start()
except KeyboardInterrupt:
    tornado.ioloop.IOLoop.instance().stop()
