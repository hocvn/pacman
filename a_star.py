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


def is_valid_ghost_position(pos, maze):
    """Check if the position is within bounds and not a wall."""
    x, y = pos
    return 0 <= x < len(maze) and 0 <= y < len(maze[0]) and maze[x][y] != '#'

def heuristic(pos, target, danger_zones=None, weight=1, clauses=None, current_assignments=None, 
                            game_state=None, ghost_index=None):

    if clauses and current_assignments is not None:
        assumptions = current_assignments.copy()
        move_var = pos[0] * 100 + pos[1]
        assumptions.append(move_var)
        
        if not is_move_valid(clauses, assumptions):
            return float('inf')
    
    # Tính khoảng cách cơ bản
    base_distance = abs(pos[0] - target[0]) + abs(pos[1] - target[1])
    
    # Tính điểm chiến lược
    strategic_score = 0
    if game_state and ghost_index is not None:
        other_ghost_positions = game_state.get_ghost_positions()
        print(f"Other ghost positions: {other_ghost_positions}")
        if len(other_ghost_positions) > 1:
            # Tính điểm cho việc phối hợp với ghost khác
            for i, other_pos in enumerate(other_ghost_positions):
                if i != ghost_index:
                    # Ưu tiên ghost ở vị trí phù hợp để bao vây
                    if abs(other_pos[0] - target[0]) + abs(other_pos[1] - target[1]) < 5:
                        strategic_score -= 2  # Giảm điểm heuristic khi có thể bao vây
    
    # Xử lý vùng nguy hiểm
    danger_penalty = 0
    if danger_zones and pos in danger_zones:
        danger_penalty = 10
    
    return weight * base_distance + danger_penalty + strategic_score

def ghost_astar_search(tiles, start, goal, banned_position=None, danger_zones=None, 
                       clauses=None, current_assignments=None, 
                       game_state=None, ghost_index=None, weight=1):

    rows, cols = len(tiles), len(tiles[0])
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(
        start, goal, danger_zones=danger_zones, weight=weight, 
        clauses=clauses, current_assignments=current_assignments, 
        game_state=game_state, ghost_index=ghost_index
    )}
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
                if (neighbor not in g_score or tentative_g_score < g_score[neighbor]) and (banned_position != neighbor or current != start):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score

                    f_score_neighbor = tentative_g_score + heuristic(
                        neighbor, goal, danger_zones=danger_zones, weight=weight, 
                        clauses=clauses, current_assignments=current_assignments, 
                        game_state=game_state, ghost_index=ghost_index
                    )

                    f_score[neighbor] = f_score_neighbor
                    heapq.heappush(open_set, (f_score_neighbor, neighbor))

    return [], nodes_opened
