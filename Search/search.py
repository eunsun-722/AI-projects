# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Michael Abir (abir2@illinois.edu) on 08/28/2018
import math
"""
This is the main entry point for MP1. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
# Search should return the path.
# The path should be a list of tuples in the form (row, col) that correspond
# to the positions of the path taken by your search algorithm.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,dfs,astar,astar_multi,extra)

def search(maze, searchMethod):
    return {
        "bfs": bfs,
        "dfs": dfs,
        "astar": astar,
        "astar_multi": astar_multi,
        "extra": extra,
    }.get(searchMethod)(maze)


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
    """
    Runs BFS for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
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
                break

            neighbors = maze.getNeighbors(r, c)
            for i in neighbors:
                if (i not in visited):
                    path[i] = curr
                    queue.append(i)
    return path2


def dfs(maze):
    """
    Runs DFS for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    #visited = []
    path = {}
    path2 = []
    start = maze.getStart()
    stack = [start]
    path[start] = None
    while(stack):
        curr = stack.pop()
        #if (curr not in visited):
        #visited.append(curr)
        r = curr[0]
        c = curr[1]
        #found goal
        if (maze.isObjective(r, c)):
            path2 = create_path(path, curr, start).copy()
            break
        neighbors = maze.getNeighbors(r, c)
        for i in neighbors:
            if (i not in path):
                path[i] = curr
                #visited.append(i)
                stack.append(i)
    return path2

def calculate_h(maze, node):
    r, c = node
    list = maze.getObjectives()
    gr, gc = list[0]
    dist = abs(r - gr) + abs(c - gc)
    return dist

def return_shortest(open_set, f):
    min = None
    for i in open_set:
        if (min == None or f[i] < f[min]):
            min = i
    return min

def astar(maze):
    """
    Runs A star for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    start = maze.getStart()
    open_set = [start]
    closed_set = []
    visited = {}
    visited[start] = None
    g = {}
    g[start] = 0

    f = {}
    f[start] = calculate_h(maze, start)

    #queue.put((f[start], start))
    while(open_set):
        curr = return_shortest(open_set, f)
        if (maze.isObjective(curr[0], curr[1])):
            return create_path(visited, curr, start).copy()
        open_set.remove(curr)
        closed_set.append(curr) #??
        neighbors = maze.getNeighbors(curr[0], curr[1])
        for i in neighbors:
            if (i not in g.keys()):
                g[i] = math.inf
            if (i in closed_set):
                continue
            #if (i not in open_set):
                #open_set.append(i)
            temp_score = g[curr] + 1
            if (temp_score < g[i]):
                visited[i] = curr
                g[i] = temp_score
                f[i] = g[i] + calculate_h(maze, i)
                if (i not in open_set):
                    open_set.append(i)
        #closed_set.append(curr) #visited all of its neighbors
    return []
def h_mst(start, end):
    return abs(start[0] - end[0]) + abs(start[1] - end[1])

def astar_mst(curr, goal, maze):
    start = curr
    open_set = [start]
    closed_set = []
    visited = {}
    visited[start] = None
    g = {}
    g[start] = 0
    f = {}
    f[start] = h_mst(start, goal)

    while(open_set):
        curr = return_shortest(open_set, f)
        if (curr[0] == goal[0] and curr[1] == goal[1]):
            return len(visited)
        open_set.remove(curr)
        closed_set.append(curr) #??
        neighbors = maze.getNeighbors(curr[0], curr[1])
        for i in neighbors:
            if (i not in g.keys()):
                g[i] = math.inf
            if (i in closed_set):
                continue
            #if (i not in open_set):
                #open_set.append(i)
            temp_score = g[curr] + 1
            if (temp_score < g[i]):
                visited[i] = curr
                g[i] = temp_score
                f[i] = g[i] + h_mst(i, goal)
                if (i not in open_set):
                    open_set.append(i)
    return len(visited)

def shortest_path(dict):
    min = math.inf
    node = None
    for i in dict:
        if (dict[i] < min):
            min = dict[i]
            node = i
    return node

def MST(curr, nodes, maze):
    visited = [curr]
    #mst = {}
    #mst[curr] = 0
    sum = 0
    while(len(visited) < len(nodes) + 1):
        min_cost = math.inf #current minimum cost of node to weight
        min_node = None
        for node in visited: #loops all highlighted nodes
            for i in (maze.getNeighbors(node[0], node[1])): #neighbors of highlighted nodes
                if (i not in visited):
                    cost = astar_mst(i, node, maze)
                    if (cost < min_cost):
                        min_cost = cost
                        min_node = i
        visited.append(min_node)
        #mst[min_node] = min_cost
        sum += min_cost
    return sum



def astar_multi(maze):
    """
    Runs A star for part 2 of the assignment in the case where there are
    multiple objectives.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    dots = maze.getObjectives()
    start = maze.getStart()
    prev_start = start
    open_set = [start]
    closed_set = []
    visited = {}
    visited[start] = None
    total_path = []
    g = {}
    g[start] = 0
    last_node = None
    f = {}
    min_h = math.inf
    for dot in dots:
        calc = h_mst(start, dot)
        if (calc < min_h):
            min_h = calc
    f[start] = min_h + MST(start, dots, maze)

    while(dots):
        curr = return_shortest(open_set, f)
        if (curr in dots):
            path = create_path(visited, curr, prev_start).copy()
            #print(path)
            if (len(dots) != 1):
                path.remove(curr)
            prev_start = curr
            total_path = total_path + path
            dots.remove(curr)

            #reset
            closed_set = []
            open_set = [curr]
            g = {}
            g[curr] = 0

            #min_h = math.inf
            #for dot in dots:
            #    calc = h_mst(curr, dot)
            #    if (calc < min_h):
            #        min_h = calc
            #0f[curr] = min_h + MST(curr, dots, maze)
            visited = {}
            visited[curr] = None

            #continue
        open_set.remove(curr)
        closed_set.append(curr)
        neighbor = maze.getNeighbors(curr[0], curr[1])
        for n in neighbor:
            if (n not in g.keys()):
                g[n] = math.inf
            temp_g = g[curr] + 1
            mst = MST(n, dots, maze)
            min_val = math.inf
            if (n in closed_set):
                continue
            for goal in dots:
                this_f = mst + g[curr] + 1 + h_mst(n, goal)
                if (this_f < min_val):
                    min_val = this_f
            if (temp_g < g[n]):
                g[n] = temp_g
                visited[n] = curr
                f[n] = min_val
            if (n not in open_set):
                open_set.append(n)
    #print("-------------------------------------")
    #print(total_path)
    return total_path


def extra(maze):
    """
    Runs extra credit suggestion.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    '''
    start = maze.getStart()
    prev_start = start
    open_set = [start]
    closed_set = []
    visited = {}
    visited[start] = None
    g = {}
    g[start] = 0

    f = {}
    f[start] = calculate_h(maze, start)
    path = []
    goals = maze.getObjectives()
    for curr_goal in goals:
        g = {}
        g[prev_start] = 0
        closed_set = []
        visited = {}
        visited[prev_start] = None
        open_set = [prev_start]
        while(open_set):
            curr = return_shortest(open_set, f)
            if (curr == curr_goal):
                path = path + create_path(visited, curr, prev_start).copy()
                prev_start = curr
                #update
                open_set = []
                g = {}
                g[start] = 0
                closed_set = []
                visited = {}
                visited[prev_start] = None
                break
            open_set.remove(curr)
            closed_set.append(curr) #??
            neighbors = maze.getNeighbors(curr[0], curr[1])
            for i in neighbors:
                if (i not in g.keys()):
                    g[i] = math.inf
                if (i in closed_set):
                    continue
                #if (i not in open_set):
                    #open_set.append(i)
                temp_score = g[curr] + 1
                if (temp_score < g[i]):
                    visited[i] = curr
                    g[i] = temp_score
                    f[i] = g[i] + calculate_h(maze, i)
                    if (i not in open_set):
                        open_set.append(i)
    return path
    '''
    dots = maze.getObjectives()
    start = maze.getStart()
    prev_start = start
    open_set = [start]
    closed_set = []
    visited = {}
    visited[start] = None
    total_path = []
    g = {}
    g[start] = 0
    last_node = None
    f = {}
    min_h = math.inf
    for dot in dots:
        calc = h_mst(start, dot)
        if (calc < min_h):
            min_h = calc
    f[start] = min_h + MST(start, dots, maze)

    while(dots):
        curr = return_shortest(open_set, f)
        if (curr in dots):
            path = create_path(visited, curr, prev_start).copy()
            #print(path)
            if (len(dots) != 1):
                path.remove(curr)
            prev_start = curr
            total_path = total_path + path
            dots.remove(curr)

            #reset
            closed_set = []
            open_set = [curr]
            g = {}
            g[curr] = 0
            visited = {}
            visited[curr] = None

            #continue
        open_set.remove(curr)
        closed_set.append(curr)
        neighbor = maze.getNeighbors(curr[0], curr[1])
        for n in neighbor:
            if (n not in g.keys()):
                g[n] = math.inf
            temp_g = g[curr] + 1
            mst = MST(n, dots, maze)
            min_val = math.inf
            if (n in closed_set):
                continue
            for goal in dots:
                this_f = mst + g[curr] + 1 + h_mst(n, goal)
                if (this_f < min_val):
                    min_val = this_f
            if (temp_g < g[n]):
                g[n] = temp_g
                visited[n] = curr
                f[n] = min_val
            if (n not in open_set):
                open_set.append(n)

    return total_path
