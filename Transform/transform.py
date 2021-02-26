
# transform.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Jongdeog Lee (jlee700@illinois.edu) on 09/12/2018

"""
This file contains the transform function that converts the robot arm map
to the maze.
"""
import copy
from arm import Arm
from maze import Maze
from search import *
from geometry import *
from const import *
from util import *

def transformToMaze(arm, goals, obstacles, window, granularity):
    """This function transforms the given 2D map to the maze in MP1.

        Args:
            arm (Arm): arm instance
            goals (list): [(x, y, r)] of goals
            obstacles (list): [(x, y, r)] of obstacles
            window (tuple): (width, height) of the window
            granularity (int): unit of increasing/decreasing degree for angles

        Return:
            Maze: the maze instance generated based on input arguments.

    """

    alpha, beta = arm.getArmLimit()
    offset = (alpha[0], beta[0])


    num_row = int((alpha[1] - alpha[0]) / granularity) + 1
    num_col = int((beta[1] - beta[0]) / granularity) + 1


    #print(arm.getArmLimit())
    #curr_angle = (alpha[0], beta[0])
    minalpha = alpha[0]
    minbeta = beta[0]
    start_pos = angleToIdx(arm.getArmAngle(), offset, granularity)
    #print(start_pos)

    maze = []
    temp_list = []
    for i in range(num_row):
        for j in range(num_col):
            temp_list.append(SPACE_CHAR)
        maze.append(temp_list)
        temp_list = []
    maze[start_pos[0]][start_pos[1]] = START_CHAR

    #print(maze)
    #print("maze printed")
    for i in range(num_row):
        #reset
        for j in range(num_col):

            #x = minalpha + (i * granularity)
            #y = minbeta + (j * granularity)
            angles = (minalpha + (i * granularity), minbeta + (j * granularity))
            arm.setArmAngle(angles)
            curr_arm = arm.getArmPos()
            if (not isArmWithinWindow(curr_arm, window) or doesArmTouchObstacles(curr_arm, obstacles)):
                maze[i][j] = WALL_CHAR
            elif (doesArmTouchGoals(arm.getEnd(), goals)):
                maze[i][j] = OBJECTIVE_CHAR
            elif(doesArmTouchObstacles(curr_arm, goals)):
                maze[i][j] = WALL_CHAR

                #print("goal = ", i, " ", j)

    maze[start_pos[0]][start_pos[1]] = START_CHAR
    #print (start_pos)
    #for i in range(num_row):
        #print(maze[i])
    #print("maze created")
    return Maze(maze, offset, granularity)
