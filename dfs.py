# DFS algorithm to find a path in a maze
# This code implements a depth-first search (DFS) algorithm to find a path in a maze.

def ghost_dfs_search(start, goal, tiles, last_position):
    rows, cols = len(tiles), len(tiles[0])
    visited = set()     # store place that visited
    stack = []          # store position that need to visit
    stack.append(start)
    trace = {}          # store path that visited\
    expanded_nodes = 0    # count number of expanded nodes

    while stack:
        current = stack.pop()
        expanded_nodes += 1

        if current == goal:
            path = []
            while current != start:
                path.append(current)
                current = trace[current]
            path.append(start)
            path.reverse()  # reverse the path to get the correct order
            return path, expanded_nodes
    
        x, y = current

        for dx, dy in [(0, 1), (0, -1), (-1, 0), (1, 0)]:
            next_x, next_y = x + dx, y + dy
            next_pos = (next_x, next_y)
            # Check next position is in the maze, is not a wall and not visited
            if 0 <= next_y < rows and 0 <= next_x < cols and tiles[next_y][next_x] != '#':
                if next_pos not in visited and (current != start or next_pos != last_position):
                    stack.append(next_pos)
                    visited.add(next_pos)  # mark as visited
                    trace[next_pos] = current   # store the path
    return [], 0
