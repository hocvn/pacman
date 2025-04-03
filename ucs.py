# UCS (Uniform Cost Search) algorithm implementation
# This code implements a uniform cost search (UCS) algorithm to find the shortest path in a maze.

import heapq

def ucs(start, goal, tiles):
    rows, cols = len(tiles), len(tiles[0])
    visited = set()
    pq = []
    heapq.heappush(pq, (0, start, [start]))
    while pq:
        cost, current, path = heapq.heappop(pq)
        if current == goal:
            return path
        if current in visited:
            continue
        visited.add(current)
        x, y = current
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= ny < rows and 0 <= nx < cols and tiles[ny][nx] != '#':
                heapq.heappush(pq, (cost + 1, (nx, ny), path + [(nx, ny)]))
    return []