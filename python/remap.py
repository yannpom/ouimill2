#!/usr/bin/env python

import emccanon
from interpreter import *
throw_exceptions = 1

import geometry


# def m650(self, **words):
#     if not self.task: return INTERP_OK
#     points = read_last_n_points(self, 8)
#     probe_radius = float(self.params[5410]) / 2.0
#     xc, yc, a, a_skew = geometry.find_centrer_angle_and_skew_from_4_corners(points, probe_radius)
#     cmd = "G10 L2 P0 X%f Y%f R%f" % (xc, yc, get_new_angle_same_quadrant(self, a))
#     print("cmd", cmd)
#     self.execute(cmd)
#     return INTERP_OK

def m650(self, **words):
    if not self.task: return INTERP_OK
    points = read_last_n_points(self, 4)
    probe_radius = float(self.params[5410]) / 2.0
    xc, yc, a, a_skew = geometry.find_center_angle_and_skew_from_4_points(points, probe_radius)
    cmd = "G10 L2 P0 X%f Y%f R%f" % (xc, yc, get_new_angle_same_quadrant(self, a))
    print("cmd", cmd)
    self.execute(cmd)
    return INTERP_OK


def read_last_n_points(self, n):
    p = []
    for i in range(n):
        p.append((self.params[1310+10*i], self.params[1311+10*i]))
    return p


def get_new_angle_same_quadrant(self, a):
    current_wc = self.params[5220]
    current_wc = int(current_wc)
    current_a = self.params[5210+20*current_wc]
    quadrant = ((int(current_a)+45+2*360) % 360) / 90
    new_a = quadrant*90 + a
    return new_a
    

def m652(self, **words):
    if not self.task: return INTERP_OK
    points = read_last_n_points(self, 4)
    probe_radius = float(self.params[5410]) / 2.0
    xc, yc, a = geometry.find_centrer_and_angle_from_2_corners(points, probe_radius)
    cmd = "G10 L2 P0 X%f Y%f R%f" % (xc, yc, get_new_angle_same_quadrant(self, a))
    print("cmd", cmd)
    self.execute(cmd)
    return INTERP_OK


def m653(self, **words):
    if not self.task: return INTERP_OK
    p = read_last_n_points(self, 1)[0]
    cmd = "G10 L2 P0 X%f Y%f" % p
    print("cmd", cmd)
    self.execute(cmd)
    return INTERP_OK


def m654(self, **words):
    if not self.task: return INTERP_OK
    points = read_last_n_points(self, 3)
    probe_radius = float(self.params[5410]) / 2.0
    xc, yc, a = geometry.find_corner_and_angle_from_3_points(points, probe_radius)
    cmd = "G10 L2 P0 X%f Y%f R%f" % (xc, yc, get_new_angle_same_quadrant(self, a))
    print("cmd", cmd)
    self.execute(cmd)
    return INTERP_OK


def m655(self, **words):
    if not self.task: return INTERP_OK
    p1, p2 = read_last_n_points(self, 2)
    xc = (p1[0] + p2[0]) / 2.0
    yc = (p1[1] + p2[1]) / 2.0
    cmd = "G10 L2 P0 X%f Y%f" % (xc, yc)
    print("cmd", cmd)
    self.execute(cmd)
    return INTERP_OK


# class s:
#     params = {
#         1311: 101,
#         1312: 90.5,

#         1321: 90.3,
#         1322: 100.8,

#         1331: 100.1,
#         1332: -90.9,

#         1341: 90.4,
#         1342: -100.2,

#         1351: -100.8,
#         1352: 90.7,

#         1361: -90.2,
#         1362: 100.7,

#         1371: -100.5,
#         1372: -90.1,

#         1381: -90.4,
#         1382: -100.8,
#     }



# class s:
#     params = {
#         1311: 101,
#         1312: 90,

#         1321: 90,
#         1322: 100,

#         1331: 100,
#         1332: -90,

#         1341: 90,
#         1342: -100,

#         1351: -99,
#         1352: 90,

#         1361: -90,
#         1362: 100,

#         1371: -100,
#         1372: -90,

#         1381: -90,
#         1382: -100,
#     }



### 1 point

# find center                                       M653                          

### 2 points

# 2 holes: find center + angle

### 3 points

# 1 corner + 3rd point: find corner + angle         M654 

### 4 points

# 2 corners: center + angle                         M652
# 4 holes: center + angle + check squareness        M650
# 4 sides of a face: center only, NO ANGLE!

### 8 points

# 4 corners: center + angle + squareness


# m650(s)


