# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Jongdeog Lee (jlee700@illinois.edu) on 09/12/2018

"""
This file contains search functions.
"""
# Search should return the path and the number of states explored.
# The path should be a list of tuples in the form (alpha, beta, gamma) that correspond
# to the positions of the path taken by your search algorithm.
# Number of states explored should be a number.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,dfs,greedy,astar)
# You may need to slight change your previous search functions in MP1 since this is 3-d maze

def search(maze, searchMethod):
    return {
        "bfs": bfs,
        "dfs": dfs,
        "greedy": greedy,
        "astar": astar,
    }.get(searchMethod, [])(maze)

def create_path(path, goal, start):
    path2 = []
    tmp = goal
    while(path[tmp] != None):
        path2.append(tmp)
        tmp = path[tmp]
    path2.append(start)
    path2.reverse()
    return path2


def bfs(maze):
    # TODO: Write your code here
    visited = []
    #path dictionary to store prev nodes
    path = {}
    path2 = []
    start = maze.getStart()
    queue = [start]
    path[start] = None
    #print("test1, ", type(path2))
    #queue_size check
    while(queue):
        curr = queue.pop(0)
        if (curr not in visited):
            visited.append(curr)
            r = curr[0]
            c = curr[1]
            #found goal
            if (maze.isObjective(r, c)):
                path2 = create_path(path, curr, start).copy()
                return path2, 0
                break

            neighbors = maze.getNeighbors(r, c)
            for i in neighbors:
                if (i not in visited):
                    path[i] = curr
                    queue.append(i)
    return [],0


def dfs(maze):
    # TODO: Write your code here
    return [], 0

def greedy(maze):
    # TODO: Write your code here
    return [], 0

def astar(maze):
    # TODO: Write your code here
    return [], 0
