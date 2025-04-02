import heapq

def heuristic(pos, target, danger_zones=None, weight=1):
    """Combined heuristic: Manhattan distance + danger zone penalty."""
    penalty = 0
    if danger_zones and pos in danger_zones:
        penalty = 10  # Add a penalty for being in a danger zone
    return weight * (abs(pos[0] - target[0]) + abs(pos[1] - target[1])) + penalty
def is_valid_ghost_position(pos, maze):
    """Check if the position is within bounds and not a wall."""
    x, y = pos
    return 0 <= x < len(maze) and 0 <= y < len(maze[0]) and maze[x][y] != '#'

def ghost_astar_search(tiles, start, goal, danger_zones=None):

    rows, cols = len(tiles), len(tiles[0])
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]

        x, y = current
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (x + dx, y + dy)
            if 0 <= neighbor[1] < rows and 0 <= neighbor[0] < cols and tiles[neighbor[1]][neighbor[0]] != "#":
                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return []


