# Ouimill2

Here are the LinuxCNC configuration files of my CNC router shown is those videos:

https://youtu.be/0U_ZFNjyZ00

https://youtu.be/3_ACFM97Wnw


My custom G codes for probing are defined in `ouimill2.ini`. I mainly use those:

`REMAP=G39.1 modalgroup=1 argspec=XYZDR ngc=probe-circle`

The G code is in `probe-circle.ngc`. It probes 4 points around the given XY point to find the center of a cylinder.
Then, thanks to the `M630` it pushes the result in a stack of "last probe results"

`REMAP=M650 modalgroup=10 python=m650`

Code in `python/remap.py::m650`. Given you've probed 4 cylinders representing a rectangle, this `M650` will compute the center of the 4 cylinders and the skew angle. It will then update the current coordinate system (`G10 L2 P0 ...`) with the result. It will even give you (debug print) the squareness error value of your 4 cylinders.

Typical usage:

```
G39.1 X100 Y80 D 12 Z15 R25
G39.1 X-100 Y80 D 12 Z15 R25
G39.1 X-100 Y-80 D 12 Z15 R25
G39.1 X-100 Y-80 D 12 Z15 R25
M650
```
