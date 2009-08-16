#!/usr/bin/python

from __future__ import with_statement

## CONFIG ##

interface = 'wlan0'  # What interface to listen on?
hosts = ['facebook.com', 'twitter.com']  # Hosts to discourage
timedelay = 30.0  # How long must you abstain before you get the lights back?

# What do we use to dim the screen? (xdim / acpi)
dimmode = 'xdim'

# xdim config
xdim_lower = 0.5  # How much do we dim the lights?  (0-1)

# acpi config
procbrightness  = '/proc/acpi/video/VID/LCD0/brightness'  # Where's the switch?
brightnessdelta = 15  # How much do we dim the lights?  (percentage)
minbrightness   = 10  # How low can you go?


import os
import os.path
import re
from subprocess import call, Popen, PIPE
import sys
from threading import Event, Timer


def xdim_brightness_functions():
    return (lambda : call(['./xdim', str(xdim_lower)]),
            lambda : call(['./xdim', '1']))

def acpi_brightness_functions():
    with open(procbrightness, 'r') as br:
        for line in br:
            if line.startswith('current:'):
                normalbrightness = int(line.split()[1])
                lowerbrightness = max(normalbrightness - brightnessdelta,
                                      minbrightness)
                break

    def punish():
        with open(procbrightness, 'w') as br:
            br.write('%d\n' % lowerbrightness)
    def unpunish():
        with open(procbrightness, 'w') as br:
            br.write('%d\n' % normalbrightness)
    return punish, unpunish

def capture_filter(hosts):
    return (' or '.join('(host %s)' % host.replace(':', ' and port ')
                        for host in hosts)).split()

def main(argv):
    linere = re.compile(r'(?P<packets>[0-9]*) packets captured')
    args = ['tcpdump', '-i', interface, '-c', '1']
    args.extend(capture_filter(hosts))

    if dimmode == 'xdim':
        punish, unpunish = xdim_brightness_functions()
    elif dimmode == 'acpi':
        punish, unpunish = acpi_brightness_functions()

    killed = Event()
    def killer(fn):
        def killfn():
            if not killed.is_set():
                killed.set()
                fn()
        return killfn

    islower = False

    with open('/dev/null', 'w') as null:
        while True:
            tcpdump = Popen(args, stdout=null, stderr=PIPE)

            timer = Timer(timedelay, killer(tcpdump.terminate))
            killed.clear()
            timer.daemon = True
            timer.start()

            _, err = tcpdump.communicate()

            if not killed.is_set():
                killed.set()
                timer.cancel()

                for line in err.split('\n'):
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
