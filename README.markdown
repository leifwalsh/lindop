lindop
======

Given a set of hosts with whom you want to avoid communicating, `lindop` lowers
your laptop's brightness whenever you visit one of them.

Concept
-------

Uses `tcpdump` to watch for connections to blacklisted hosts.  Dims with
`/proc/` api, or a small gamma-based Xlib program (greetz Michal Janeczek) when
necessary.

Config
------

Possible config options include:

 * *interface*: Which interface to watch?  (Mine is `wlan0`, YMMV)

 * *hosts*: The aforementioned list of hosts

 * *timedelay*: How long should you be a good worker before we turn the lights
   back up?

 * *dimmode*: Select between `'acpi'` (if you have the `/proc/` stuff below) and
   `'xdim'` (if you don't or just want to use the gamma-based version).

#### ACPI config:

 * *brightnessdelta*: How much should we dim the lights (percentage)?

 * *minbrightness*: In case you have the normal brightness fairly low, what's
   the lowest we should go?

 * *procbrightness*: The file somewhere in `/proc/` that controls brightness.
   Mine is `/proc/acpi/video/VID/LCD0/brightness`, but yours may be different.

My `/proc/.../brightness` file responds as follows (if yours has a different
api, you'll need to understand and change the code):

    % cat /proc/acpi/video/VID/LCD0/brightness
    levels:  20 25 30 35 40 45 50 55 60 65 70 75 80 85 90 100
    current: 85
    % su -c 'echo 70 >/proc/acpi/video/VID/LCD0/brightness'
    # ((lights go down))

#### xdim config:

 * *xdim_lower*: How much should we dim the lights (fraction between 0 and 1,
   lower is darker)?

Usage
-----

    % make  # if you want to use xdim
    % sudo ./lindop.py

Bugs
----

Probably.

Forking
-------

I am particularly interested in forks that add platform support.  If you have a
different laptop and get this script running on yours, send me a pull request.

ACKS
----

Michal Janeczek
