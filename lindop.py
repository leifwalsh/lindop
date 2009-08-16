#!/usr/bin/python

## CONFIG ##
interface = 'wlan0'  # What interface to listen on?
hosts = ['facebook.com', 'twitter.com']  # Hosts to discourage
brightnessdelta = 15  # How much do we dim the lights?
minbrightness = 10  # How low can you go?
timedelay = 30.0  # How long must you abstain before you get the lights back?
procbrightness = '/proc/acpi/video/VID/LCD0/brightness'  # Where's the switch?

import os
import os.path
import re
from subprocess import Popen, PIPE
import sys
from threading import Event, Timer

linere = None

def main(argv):
    global linere
    linere = re.compile(r'(?P<packets>[0-9]*) packets captured')

    args = ['tcpdump', '-i', interface, '-c', '1']
    for host in hosts:
        args.extend(['host', host, 'or'])
    else:
        args = args[:-1]

    killed = Event()
    def killer(fn):
        def killfn():
            if not killed.is_set():
                killed.set()
                fn()
        return killfn

    with open(procbrightness, 'r') as br:
        for line in br:
            if line.startswith('current:'):
                normalbrightness = int(line.split()[1])
                lowerbrightness = max(normalbrightness - brightnessdelta,
                                      minbrightness)
                break
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
                mg = linere.match(line)
                if mg and int(mg.group('packets')) != 0:
                    if not islower:
                        with open(procbrightness, 'w') as br:
                            br.write('%d\n' % lowerbrightness)
                        islower = True
                    break
            else:
                if islower:
                    with open(procbrightness, 'w') as br:
                        br.write('%d\n' % normalbrightness)
                    islower = False

if __name__ == '__main__':
    if os.environ['USER'] != 'root':
        print >>sys.stderr, ('You must run %s as root!' %
                             os.path.basename(sys.argv[0]))
        sys.exit(2)
    else:
        sys.exit(main(sys.argv))
