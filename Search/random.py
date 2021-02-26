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
