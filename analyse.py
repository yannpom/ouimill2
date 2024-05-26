#!/usr/bin/env python

import numpy as np
import math
import sys

def parse(file):
    points = []
    with open(file) as f:
        lines = f.readlines()
        for line in lines:
            x,y,z,a,b,c,u,v,w = line.split()
            p = (float(x),float(y))
            points.append(p)
    return points


def lineFromPoints(points):
    x = list(i[0] for i in points)
    y = list(i[1] for i in points)
    z = np.polyfit(x, y, 1, full=True)

    if abs(z[0][0]) > 1.0:
        points_reversed = list((p[1], -p[0]) for p in points)
        return math.pi/2.0 + lineFromPoints(points_reversed)

    a = z[0][0]
    b = z[0][1]
    # y = a.x + b
    r = z[1][0]

    alpha = math.atan(a)
    
    #print "y = %f * x + %f" % (a, b)
    #print "r = %f" % r
    #print "alpha = %f" % (alpha * 180.0 / math.pi)

    # check max error
    max_d = 0.0
    p1 = np.array((0.0, b))
    p2 = np.array((1.0, a+b))
    for p3 in (np.array(p) for p in points):
        d = np.linalg.norm(np.cross(p2-p1, p1-p3))/np.linalg.norm(p2-p1)
        max_d = max(d, max_d)
        
    print "max_d", max_d

    return alpha

def findLines(data):
    p2 = None
    line = []
    points = []

    for p1 in data:
        if p2:
            dx = p2[0] - p1[0]
            dy = p2[1] - p1[1]
            if abs(dx) > 1.0 and abs(dy) > 1.0:
                yield lineFromPoints(points)
                points = []

        points.append(p1)
        p2 = p1
    yield lineFromPoints(points)

points = parse(sys.argv[1] if len(sys.argv) == 2 else 'probe.txt')
#print points
#print "AAA"
a1, a2 = list(findLines(points))
alpha = (a2-a1) * 180.0 / math.pi
print "alpha", alpha

print "error on 1000mm:", math.tan(a2-a1-math.pi/2.0)*1000.0


