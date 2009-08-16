#!/usr/bin/python

### CONFIG ##

# What interface to listen on?
interface = 'wlan0'

# Hosts to discourage
hosts = ['reddit.com', 'www.reddit.com', 'www.google.com:443', 'news.ycombinator.com']

# How long must you abstain before you get the lights back?
timedelay = 30.0

# What do we use to dim the screen? (xdim / acpi)
dimmode = 'xdim'  

# How much do we dim the lights?
xdim_lower = 0.5

# for acpi
procbrightness  = '/proc/acpi/video/VID/LCD0/brightness'  # Where's the switch?
brightnessdelta = 15  # How much do we dim the lights?
minbrightness   = 10  # How low can you go?

###


import os
import os.path
import re
import signal
from subprocess import Popen, PIPE
import sys
from threading import Event, Timer


def xdim_brightness_functions():
    def punish():
        os.system("./xdim %f" % xdim_lower)
    def unpunish():
        os.system("./xdim 1")
    return punish, unpunish

def acpi_brightness_functions():
    br = open(procbrightness, 'r')
    for line in br:
        if line.startswith('current:'):
            normalbrightness = int(line.split()[1])
            lowerbrightness = max(normalbrightness - brightnessdelta, minbrightness)
            break
    br.close()
    def punish():
        br = open(procbrightness, 'w')
        br.write('%d\n' % lowerbrightness)
        br.close()
    def unpunish():
        br = open(procbrightness, 'w')
        br.write('%d\n' % normalbrightness)
        br.close()
    return punish, unpunish


def brightness_functions():
    if dimmode == 'xdim':
        return xdim_brightness_functions()
    elif dimmode == 'acpi':
        return acpi_brightness_functions()


def capture_filter(hosts):
    return " or ".join("(host " + host.replace(":", " and port ") + ")" for host in hosts)


def main(argv):
    linere = re.compile(r'(?P<packets>[0-9]*) packets captured')
    args = ['tcpdump', '-i', interface, '-c', '1', capture_filter(hosts)]
    punish, unpunish = brightness_functions()

    killed = Event()
    def killer(fn):
        def killfn():
            if not killed.isSet():
                killed.set()
                fn()
        return killfn

    islower = False

    null = open('/dev/null', 'w')
    while True:
        tcpdump = Popen(args, stdout=null, stderr=PIPE)

        timer = Timer(timedelay, killer(lambda: os.kill(tcpdump.pid, signal.SIGTERM)))
        killed.clear()
        timer.daemon = True
        timer.start()

        _, err = tcpdump.communicate()

        if not killed.isSet():
            killed.set()
            timer.cancel()

        for line in err.split('\n'):
            mg = linere.match(line)
            if mg and int(mg.group('packets')) != 0:
                if not islower:
                    punish()
                    islower = True
                break
        else:
            if islower:
                unpunish()
                islower = False


if __name__ == '__main__':
    if os.environ['USER'] != 'root':
        print >>sys.stderr, ('You must run %s as root!' %
                             os.path.basename(sys.argv[0]))
        sys.exit(2)
    else:
        sys.exit(main(sys.argv))
