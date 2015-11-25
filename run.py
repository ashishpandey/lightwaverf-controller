#!/usr/bin/python
from datetime import datetime
import tornado.ioloop
import tornado.web
import os
from handlers.DimmerHandler import DimmerHandler
from handlers.ScheduleHandler import ScheduleHandler
from Data import Data
from Scheduler import Scheduler

import argparse

parser = argparse.ArgumentParser(description='LightwaveRF Web Interface')
parser.add_argument('--data-file', dest='data_file', action='store', default="/var/tmp/light-controller-data",
                   help='The file location to save timer and other data')

parser.add_argument('--id', dest='id', action='store', default="1",
                   help='The id of the dimmer to transmit')

parser.add_argument('--port', dest='port', action='store', default="88",
                   help='The port to listen on')

args = parser.parse_args()
id = int(args.id)
port = int(args.port)

data = Data(args.data_file)
scheduler = Scheduler(data.get_schedules())

cwd =  os.path.dirname(os.path.realpath(__file__))
application = tornado.web.Application([
    ("/api/dimmer", DimmerHandler, dict(id=id, data=data)),
    ("/api/schedules", ScheduleHandler, dict(scheduler=scheduler, id=id, data=data)),
    (r'/(.*)', tornado.web.StaticFileHandler, {'path': cwd + '/static', "default_filename":"index.html"}),
])


application.listen(port)
print "Started"
try:
    tornado.ioloop.IOLoop.instance().start()
except KeyboardInterrupt:
    tornado.ioloop.IOLoop.instance().stop()
