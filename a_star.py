import heapq

import pycosat

def is_move_valid(clauses, assumptions):
    """
    clauses: CNF clauses as list of lists (e.g., [[1, -2], [3]])
    assumptions: current known facts (e.g., [4, -5])
    Returns: True if satisfiable, False otherwise
    """
    solution = pycosat.solve(clauses + [[a] for a in assumptions])
    return solution != 'UNSAT'


def heuristic(pos, target, danger_zones=None, weight=1, clauses=None, current_assignments=None):
    """
    Heuristic with SAT-checking:
    - Rejects paths that lead to logic inconsistency.
    """
    assumptions = current_assignments.copy() if current_assignments else []

    # Encode the next move as a propositional assignment (e.g., pos -> variable)
    # For example, assume pos = (x=3, y=4) maps to variable id = 3 * N + 4
    move_var = pos[0] * 100 + pos[1]  # Just an example encoding
    assumptions.append(move_var)

    # Use SAT solver to validate move
    if clauses and not is_move_valid(clauses, assumptions):
        return float('inf')  # Blocked by logic rule

    # Otherwise, return normal heuristic
    base_distance = abs(pos[0] - target[0]) + abs(pos[1] - target[1])
    penalty = 0
    if danger_zones and pos in danger_zones:
        penalty = 10
    return weight * base_distance + penalty

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
    nodes_opened = 0

    while open_set:
        _, current = heapq.heappop(open_set)
        nodes_opened += 1

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1], nodes_opened

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

    return [], nodes_opened