#!/usr/bin/env python

import math
#import matplotlib.pyplot as plt


######################################################################
######################################################################
######################################################################

def rotate_point(p, a):
    x = p[0]
    y = p[1]
    xo = x*math.cos(a) - y*math.sin(a)
    yo = x*math.sin(a) + y*math.cos(a)
    return (xo, yo)


def rotate_line(l, a):
    return [rotate_point(i, a) for i in l]


def angle_two_points(p1, p2):
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        a = math.atan2(dy, dx)
        return a


def angle_line(l):
    return angle_two_points(l[0], l[1])


def angle_two_lines(l1, l2):
        return angle_line(l2)-angle_line(l1)


def angle_modulo_180deg(a):
    return math.fmod(a+2*math.pi+math.pi/2, math.pi)-math.pi/2


def angle_modulo_90deg(a):
    return math.fmod(a+2*math.pi+math.pi/4, math.pi/2)-math.pi/4


# compute the abs angle between 2 lines
def abs_angle_2_lines(lines):
    l1, l2 = lines
    a = abs(angle_modulo_180deg(angle_two_lines(l1, l2)))
    return a


def line_length(line):
    p1 = line[0]
    p2 = line[1]
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    return math.sqrt(dx*dx+dy*dy)


######################################################################
######################################################################
######################################################################

def find_centrer_angle_and_skew_from_4_corners(points, probe_radius=3.175/2):
    assert(len(points) == 8)

    p_left_right = sorted(points, key=lambda i: i[0])
    p_top_bottom = sorted(points, key=lambda i: i[1])

    l_bottom = [p_top_bottom[0],  p_top_bottom[1]]
    l_top    = [p_top_bottom[-2], p_top_bottom[-1]]
    l_right  = [p_left_right[-2], p_left_right[-1]]
    l_left   = [p_left_right[0],  p_left_right[1]]

    l1 = l_top
    l2 = l_left
    l3 = l_bottom
    l4 = l_right

    as1 = angle_modulo_90deg(angle_two_lines(l1, l2))
    as2 = angle_modulo_90deg(angle_two_lines(l2, l3))
    as3 = angle_modulo_90deg(angle_two_lines(l3, l4))
    as4 = angle_modulo_90deg(angle_two_lines(l4, l1))
    a_skew = (as2+as4-as1-as3)/4.0
    print("as1 %f as2 %f as3 %f as4 %f" % tuple(math.degrees(i) for i in (as1, as2, as3, as4)))
    print("a_skew", math.degrees(a_skew))

    a1 = angle_modulo_90deg(angle_line(l1))
    a2 = angle_modulo_90deg(angle_line(l2))
    a3 = angle_modulo_90deg(angle_line(l3))
    a4 = angle_modulo_90deg(angle_line(l4))
    print("a1 %f a2 %f a3 %f a4 %f" % tuple(math.degrees(i) for i in (a1, a2, a3, a4)))

    a = (a1+a2+a3+a4)/4.0
    print("a", math.degrees(a))

    # compute center of points in the rotated coordinate space
    # compute the average X position of l_left + l_right
    avg_x = (rotate_line(l_left, a)[0][0] + rotate_line(l_left, a)[1][0] + rotate_line(l_right, a)[0][0] + rotate_line(l_right, a)[1][0]) / 4.0
    # compute the average Y position of l_top + l_bottom
    avg_y = (rotate_line(l_top, a)[0][1] + rotate_line(l_top, a)[1][1] + rotate_line(l_bottom, a)[0][1] + rotate_line(l_bottom, a)[1][1]) / 4.0

    # apply inverse rotation
    p_center = rotate_point((avg_x, avg_y), -a)
    xc, yc = p_center

    print("xc", xc, "yc", yc)

    return xc, yc, math.degrees(a), math.degrees(a_skew)


def find_centrer_and_angle_from_2_corners(points, probe_radius=3.175/2):
    p1, p2, p3, p4 = points
    # combinaison of possible pair of points
    c = [
            [(p1, p2), (p3, p4)],
            [(p1, p3), (p2, p4)],
            [(p1, p4), (p2, p3)],
        ]    

    # find the 2 parrallel lines
    lines = sorted(c, key=abs_angle_2_lines)[0]
    print("parralel lines", lines)

    # sort by length
    l_short, l_long = sorted(lines, key=line_length)
    print("sorted", l_short, l_long)

    # l_short give the angle
    a = angle_line(l_short)
    print("a", math.degrees(a))

    l_short_r = rotate_point(l_short[0], -a)
    
    p1r = rotate_point(l_long[0], -a)
    p2r = rotate_point(l_long[1], -a)

    dy = p1r[1]-l_short_r[1]

    y_direction = dy / abs(dy)

    yc_r = l_short_r[1] +y_direction*probe_radius

    xc_r = (p1r[0] + p2r[0]) / 2.0

    xc, yc = rotate_point((xc_r, yc_r), a)

    a = angle_modulo_90deg(a)

    print("c", xc, yc, math.degrees(a))

    return xc, yc, math.degrees(a)


def plot(points, style='ro'):
    plt_x = [i[0] for i in points]
    plt_y = [i[1] for i in points]
    plt.plot(plt_x, plt_y, style)
    plt.axes().set_aspect('equal', 'datalim')    


def find_corner_and_angle_from_3_points(points, probe_radius):
    p1, p2, p3 = points

    data = [
        (p1, (p2, p3)),
        (p2, (p3, p1)),
        (p3, (p1, p2)),
    ]

    p, line = sorted(data, key=(lambda x: line_length(x[1])))[1]
    #a = angle_modulo_180deg(angle_line(line))
    a = angle_line(line)
    am = angle_modulo_90deg(a)

    # probe offset direction

    line_r = rotate_line(line, -a)
    p_r = rotate_point(p, -a)

    yr = (line_r[0][1] + line_r[1][1]) / 2.0
    xr = p_r[0]

    dy = p_r[1]-yr
    dx = ((line_r[0][0] + line_r[1][0]) / 2.0) - xr

    dx = dx / abs(dx)
    dy = dy / abs(dy)

    yr += dy * probe_radius
    xr += dx * probe_radius

    xc, yc = rotate_point((xr, yr), a)

    print("p", p)
    print("line", line)
    print("am", math.degrees(am))
    print("xc", xc, "yc", yc)

    print("dx", dx, "dy", dy)

    # plot(points, 'ro')
    # plot([(xc, yc)], 'bo')
    # plt.show()

    return xc, yc, math.degrees(am)


######################################################################
######################################################################
######################################################################


if __name__ == "__main__":
    #find_centrer_and_angle_from_2_corners([(200,100), (210,90), (200,180), (210,190)])
    #find_centrer_angle_and_skew_from_4_corners([(110+10,100), (100-5,110), (190,100), (200,110), (110,200), (100,190), (190,200), (200,190)])


    #find_corner_and_angle_from_3_points([[10,0], [0,10], [100,1]], 3.175/2.0)
    #find_corner_and_angle_from_3_points([[-1,10], [10,1], [100,10]], 3.175/2.0)


    find_corner_and_angle_from_3_points([[0,10], [0,100], [-10,0]], 3.175/2.0)

    #find_corner_and_angle_from_3_points([[100,50+10], [100-10,50+100], [100-10,50]], 3.175/2.0)





