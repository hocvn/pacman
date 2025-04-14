# UCS (Uniform Cost Search) algorithm implementation
# This code implements a uniform cost search (UCS) algorithm to find the shortest path in a maze.

import heapq

def ghost_uniform_cost_search(start, goal, tiles, banned_position=None):
    rows, cols = len(tiles), len(tiles[0])
    visited = set()
    pq = []
    heapq.heappush(pq, (0, start, [start]))
    expanded_nodes = 0

    while pq:
        cost, current, path = heapq.heappop(pq)
        expanded_nodes += 1

        if current == goal:
            return path, expanded_nodes
        if current in visited:
            continue
        visited.add(current)
        x, y = current
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= ny < rows and 0 <= nx < cols and tiles[ny][nx] != '#' and (banned_position != (ny, nx) or current != start):
                heapq.heappush(pq, (cost + 1, (nx, ny), path + [(nx, ny)]))
    return [], 0