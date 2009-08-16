lindop
======

Given a set of hosts with whom you want to avoid communicating, `lindop` lowers
your laptop's brightness whenever you visit one of them.

Config
------

Possible config options include:

 * *interface*: Which interface to watch?  (Mine is `"wlan0"`, YMMV)

 * *hosts*: The aforementioned list of hosts

 * *brightnessdelta*: How much should we dim the lights (percentage)?

 * *minbrightness*: In case you have the normal brightness fairly low, what's
   the lowest we should go?

 * *timedelay*: How long should you be a good worker before we turn the lights
   back up?

 * *procbrightness*: The file somewhere in `/proc/` that controls brightness.
   Mine is `/proc/acpi/video/VID/LCD0/brightsess`, but yours may be different.
   Mine responds as follows:

    % cat /proc/acpi/video/VID/LCD0/brightness
    levels:  20 25 30 35 40 45 50 55 60 65 70 75 80 85 90 100
    current: 85
    % su -c 'echo 70 >/proc/acpi/video/VID/LCD0/brightness'
    # ((lights go down))

   If yours has a different api, you'll need to understand and change the code.

Usage
-----

    % sudo ./lindop.py

Bugs
----

Probably.

Forking
-------

I am particularly interested in forks that add platform support.  If you have a
different laptop and get this script running on yours, send me a pull request.
