
This is a python website (using tornado) that can run on a raspberry pi and controls a LightwaveRF dimmer lightswitch.

# Notes
This has been modified from original fork:
* support for multiple dimmers
* removed schedules/timers, to simplify purely as a controller API for my Home Assistant

# Installation
Follow the instructions at  [https://markinbristol.wordpress.com/2015/12/01/controlling-lightwaverf-panels-with-a-raspbery-pi/](https://markinbristol.wordpress.com/2015/12/01/controlling-lightwaverf-panels-with-a-raspbery-pi/)
to install pigpiod, pair the transmitter, and get the basic LightwaveRF control working

Then:

- Install Python dependencies, you can either do this globally, or use a virtualenv:
`pip install tornado==4.2.1 apscheduler==3.0.3`
- Clone this project somewhere, e.g. /opt/lightwaverf/
- Ensure the pigpiod daemon is running.  Just running `pigpiod` should start the daemon.
- Run the project: `./run.py`

This will start the website on port 88.  

Run `./run.py -h` for more command line options.
 
You can then browse to the site, e.g. `http://raspberry_pi:88`

Assuming everything is paired and working OK, hitting one of the light level buttons on the website should control the light.

To start the website in the background, and on startup there are two init-v style startup scripts in the `init` folder in the Github repo.
Copy these to "/etc/init.d", and then 
  
     update-rc.d pigpiod defaults
     update-rc.d lightwaverf defaults

You should then be able to stop and start the website using `service lightwaverf start` 

If you cloned the project somewhere other than /opt/lightwaverf, then edit the init script and adjust the daemon 
location accordingly.

Many thanks to [https://github.com/roberttidey/LightwaveRF](https://github.com/roberttidey/LightwaveRF) for all the heavy
lifting to decode the LightwaveRF signal and provide python libraries.