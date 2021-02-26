# geometry.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Jongdeog Lee (jlee700@illinois.edu) on 09/12/2018
import numpy as np
"""
This file contains geometry functions that relate with Part1 in MP2.
"""

import math
import numpy as np
from const import *

def computeCoordinate(start, length, angle):
    """Compute the end cooridinate based on the given start position, length and angle.

        Args:
            start (tuple): base of the arm link. (x-coordinate, y-coordinate)
            length (int): length of the arm link
            angle (int): degree of the arm link from x-axis to couter-clockwise

        Return:
            End position of the arm link, (x-coordinate, y-coordinate)
    """
    angle_r = math.radians(angle)
    y_coor = length * math.sin(angle_r)
    x_coor = length * math.cos(angle_r)
    pos_x = start[0] + x_coor
    pos_y = start[1] - y_coor
    #if (angle > 90):
    #    pos_x -= x_coor
    #else:
#        pos_x += x_coor
    return (pos_x , pos_y)

def doesArmTouchObstacles(armPos, obstacles):
    """Determine whether the given arm links touch obstacles

        Args:
            armPos (list): start and end position of all arm links [(start, end)]
            obstacles (list): x-, y- coordinate and radius of obstacles [(x, y, r)]

        Return:
            True if touched. False it not.
    """

    # version 1
    '''
    for i in range(len(armPos)):
        start = armPos[i][0]
        end = armPos[i][1]

        for j in range(len(obstacles)):

            obx = obstacles[j][0]
            oby = obstacles[j][1]
            obr = obstacles[j][2]

            len_arm = math.sqrt((end[1] - start[1]) ** 2 + (end[0] - start[0]) ** 2)
            len_center_to_start = math.sqrt((obx - start[0]) ** 2 + (oby - start[1]) ** 2)
            len_tip_to_center = math.sqrt((obx - end[0]) ** 2 + (oby - end[1]) ** 2)
            cos_angle_between = len_center_to_start ** 2 + len_arm ** 2 - len_tip_to_center ** 2
            cos_angle_between = cos_angle_between / (2 * len_center_to_start * len_arm)
            curr_angle = math.acos(cos_angle_between)
            max_angle = math.asin(obr / len_center_to_start)
            len_tangent_line = math.cos(max_angle) * len_center_to_start

            #checks for short arm
            if (len_arm < (len_center_to_start - obr)):
                continue
            elif (len_arm <= len_tangent_line):
                if (len_tip_to_center <= obr):
                    return True
                else:
                    continue
            elif (curr_angle <= max_angle):
                return True

            #if (dist2 < dist_to_rad):
            #    dist_to_rad = dist2
            #if (dist_to_rad < obr):
                #return True



    #version2\

    for i in range(len(armPos)):
        start = armPos[i][0]
        end = armPos[i][1]
        for j in range(len(obstacles)):
            obx = obstacles[j][0]
            oby = obstacles[j][1]
            obr = obstacles[j][2]

            d, v = np.zeros(2), np.zeros(2)
            d[0] = end[0]
            d[1] = end[1]
            v[0] = obx - start[0]
            v[1] = oby - start[1]

            coeff = np.dot(d, v) / np.dot(d, d)
            new_v = coeff * d
            distance = np.linalg.norm(v - new_v, 2)
            if (distance <= obr):
                return True


                '''
    #version 3
    '''
    obx = obstacles[j][0]
    oby = obstacles[j][1]
    obr = obstacles[j][2]
    vec_a, vec_b = np.zeros(2), np.zeros(2)
    vec_a[0] = obx - start[0]
    vec_a[1] = oby - start[1]
    vec_b[0] = end[0] - start[0]
    vec_b[1] = end[1] - start[1]

    ab = np.dot(vec_a, vec_b)
    if (ab < 0):
        len_center_to_start = math.sqrt((obx - start[0]) ** 2 + (oby - start[1]) ** 2)
        if (len_center_to_start <= obr):
            return True
    else:
        b_sq = np.dot(vec_b, vec_b)
        if (ab > b_sq):
            len_tip_to_center = math.sqrt((obx - end[0]) ** 2 + (oby - end[1]) ** 2)
            if (len_tip_to_center <= obr):
                return True
        else:
            vec_proj = (np.dot(vec_a, vec_b) / np.dot(vec_b, vec_b))
            #len_vec = np.dot(vec_proj, vec_proj)
            a_len = np.dot(vec_a, vec_a)
            len_dist = math.sqrt(a_len ** 2 -(vec_proj) ** 2)
            if (len_dist <= obr):
                return True
    '''

    #version4
    for i in range(len(armPos)):
        start = armPos[i][0]
        end = armPos[i][1]

        for j in range(len(obstacles)):
            obx = obstacles[j][0]
            oby = obstacles[j][1]
            obr = obstacles[j][2]
            len_arm = math.sqrt((end[1] - start[1]) ** 2 + (end[0] - start[0]) ** 2)
            len_center_to_start = math.sqrt((obx - start[0]) ** 2 + (oby - start[1]) ** 2)
            len_tip_to_center = math.sqrt((obx - end[0]) ** 2 + (oby - end[1]) ** 2)
            if (len_center_to_start >= len_arm):
                if (len_tip_to_center <= obr):
                    return True
            elif (len_tip_to_center >= len_arm):
                if (len_tip_to_center <= obr):
                    return True
            else:
                p = len_arm + len_center_to_start + len_tip_to_center
                p = p / 2
                area = p * (p - len_arm) * (p - len_tip_to_center) * (p - len_center_to_start)
                area = math.sqrt(area)
                height = area * 2 / len_arm
                if (height <= obr):
                    return True


    return False

def doesArmTouchGoals(armEnd, goals):
    """Determine whether the given arm links touch goals

        Args:
            armEnd (tuple): the arm tick position, (x-coordinate, y-coordinate)
            goals (list): x-, y- coordinate and radius of goals [(x, y, r)]

        Return:
            True if touched. False it not.
    """
    cond = False
    for i in range(len(goals)):
        dist = math.sqrt((armEnd[1] - goals[i][1])**2 + (armEnd[0] - goals[i][0]) ** 2)
        if (dist < goals[i][2]):
            cond = True
    return cond


def isArmWithinWindow(armPos, window):
    """Determine whether the given arm stays in the window

        Args:
            armPos (list): start and end position of all arm links [(start, end)]
            window (tuple): (width, height) of the window

        Return:
            True if all parts are in the window. False it not.
    """

    window_x = window[0]
    window_y = window[1]
    out = True
    for i in range(len(armPos)):
        start = armPos[i][0]
        end = armPos[i][1]
        if (start[0] > window_x or start[1] > window_y or start[0] < 0 or start[1] < 0):
            out = False
        if (end[0] > window_x or end[1] > window_y or end[0] < 0 or end[1] < 0):
            out = False

    return out
