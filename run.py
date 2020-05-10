
#!/usr/bin/python -u

from datetime import datetime
import tornado.ioloop
import tornado.web
import os
from handlers.DimmerHandler import DimmerHandler
from handlers.ScheduleHandler import ScheduleHandler
from Util import Util

import argparse

parser = argparse.ArgumentParser(description='LightwaveRF Web Interface')
parser.add_argument('--data-file', action='store', default="/var/tmp/light-controller-data",
                   help='The file location to save timer and other data')

parser.add_argument('--id', action='store', default=1, type=int,
                   help='The id of the dimmer to transmit')

parser.add_argument('--gpio-pin', action='store', default=7, type=int,
                   help='The GPIO pin the RF module is attached on the Pi')

parser.add_argument('--repeat', action='store', default=3, type=int,
                   help='The number of times to repeat the transmission')

parser.add_argument('--port', action='store', default=88, type=int,
                   help='The TCP port to listen on')

args = parser.parse_args()
id = int(args.id)
port = int(args.port)

util = Util(args.data_file, args.id, args.gpio_pin, args.repeat)

cwd =  os.path.dirname(os.path.realpath(__file__))
application = tornado.web.Application([
    ("/api/dimmer/(\d*)", DimmerHandler, dict(util=util)),
    (r'/(.*)', tornado.web.StaticFileHandler, {'path': cwd + '/static', "default_filename":"index.html"}),
])


application.listen(port)
print "Started"
try:
    tornado.ioloop.IOLoop.instance().start()
except KeyboardInterrupt:
    tornado.ioloop.IOLoop.instance().stop()
