def ghost_astar_search(maze, ghost_pos, pacman_pos, personality="chaser"):
    """
    A* search algorithm for Pacman ghosts.
    
    Parameters:
    - maze: 2D grid representation of the game board
    - ghost_pos: (x, y) tuple of the ghost's current position
    - pacman_pos: (x, y) tuple of Pacman's current position
    - personality: String indicating ghost behavior type
                  "chaser" - directly pursues Pacman
                  "ambusher" - tries to predict and intercept Pacman
                  "random" - alternates between chasing and random movements
                  "patrol" - patrols between key points, only chases when Pacman is close
    
    Returns:
    - Next position for the ghost to move to
    """
    import heapq
    import random
    
    # Define directions: up, right, down, left
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    
    # Set target based on ghost personality
    target = get_ghost_target(maze, ghost_pos, pacman_pos, personality)
    
    # Priority queue for open nodes
    open_set = []
    
    # Dictionary to store g scores (cost from start to current node)
    g_score = {ghost_pos: 0}
    
    # Dictionary to store f scores (g_score + heuristic)
    f_score = {ghost_pos: ghost_heuristic(ghost_pos, target, personality)}
    
    # Push start node to open set with priority = f_score
    heapq.heappush(open_set, (f_score[ghost_pos], ghost_pos))
    
    # Dictionary to store the parent of each node for path reconstruction
    came_from = {}
    
    # Set to keep track of closed nodes
    closed_set = set()
    
    # Limit search depth for performance reasons
    max_iterations = 20
    iterations = 0
    
    while open_set and iterations < max_iterations:
        iterations += 1
        
        # Get node with lowest f_score
        current_f, current = heapq.heappop(open_set)
        
        # If we reached the goal, reconstruct the path and return the next step
        if current == target:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            if path:
                return path[-1]  # Return first step towards target
            return ghost_pos  # Fallback to current position
        
        # Add current node to closed set
        closed_set.add(current)
        
        # Check all neighbors
        for dx, dy in directions:
            neighbor = (current[0] + dx, current[1] + dy)
            
            # Skip if out of bounds, wall, or already evaluated
            if (not is_valid_ghost_position(neighbor, maze) or 
                neighbor in closed_set):
                continue
            
            # Calculate new g_score for this neighbor
            tentative_g_score = g_score[current] + 1  # Each step costs 1
            
            # If this path to neighbor is better than any previous one, record it
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + ghost_heuristic(neighbor, target, personality)
                
                # Add to open set if not already there
                if neighbor not in [item[1] for item in open_set]:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
    
    # If we've reached here, either no path was found or we hit the iteration limit
    # Return the best next step based on available information
    if len(came_from) > 0:
        # Find the node closest to the ghost that has a parent
        current = min([pos for pos in came_from.keys()], 
                      key=lambda pos: abs(pos[0] - ghost_pos[0]) + abs(pos[1] - ghost_pos[1]))
        
        # Reconstruct path to this node
        path = []
        while current in came_from:
            path.append(current)
            current = came_from[current]
        
        if path:
            return path[-1]  # Return first step
    
    # Fallback: choose a random valid direction
    valid_moves = []
    for dx, dy in directions:
        next_pos = (ghost_pos[0] + dx, ghost_pos[1] + dy)
        if is_valid_ghost_position(next_pos, maze):
            valid_moves.append(next_pos)
    
    if valid_moves:
        return random.choice(valid_moves)
    
    return ghost_pos  # Stay in place if no valid moves

def is_valid_ghost_position(pos, maze):
    """Check if a position is valid for a ghost (in bounds and not a wall)"""
    x, y = pos
    if x < 0 or y < 0 or x >= len(maze) or y >= len(maze[0]):
        return False
    # Assuming: 0=empty path, 1=wall, 2=food dot, 3=power pellet, etc.
    return maze[x][y] != 1  # Ghosts can't move through walls

def ghost_heuristic(current, target, personality):
    """
    Heuristic function for ghost A* algorithm.
    
    Parameters:
    - current: Current position (x, y)
    - target: Target position (x, y)
    - personality: Ghost personality type
    
    Returns:
    - Heuristic value
    """
    # Base heuristic: Manhattan distance
    manhattan_distance = abs(current[0] - target[0]) + abs(current[1] - target[1])
    
    # Adjust heuristic based on personality
    if personality == "chaser":
        return manhattan_distance
    elif personality == "ambusher":
        # Ambushers are more determined, so heuristic is lower
        return manhattan_distance * 0.8
    elif personality == "random":
        # Add some randomness to the heuristic
        import random
        return manhattan_distance * (0.7 + random.random() * 0.6)
    elif personality == "patrol":
        # Patrollers care less about reaching the target unless close
        if manhattan_distance < 8:
            return manhattan_distance * 0.9
        else:
            return manhattan_distance * 1.2
    
    return manhattan_distance

def get_ghost_target(maze, ghost_pos, pacman_pos, personality):
    """
    Determine the target position for a ghost based on its personality.
    
    Parameters:
    - maze: The game maze
    - ghost_pos: Current ghost position
    - pacman_pos: Current Pacman position
    - personality: Ghost personality type
    
    Returns:
    - Target position (x, y)
    """
    import random
    
    # Predict Pacman's direction (simplified)
    pacman_direction = predict_pacman_direction(maze, pacman_pos)
    
    if personality == "chaser":
        # Chasers directly target Pacman
        return pacman_pos
    
    elif personality == "ambusher":
        # Ambushers try to intercept Pacman by targeting ahead of him
        prediction_steps = 4  # Look 4 steps ahead
        target_x = pacman_pos[0] + (pacman_direction[0] * prediction_steps)
        target_y = pacman_pos[1] + (pacman_direction[1] * prediction_steps)
        
        # Make sure target is in bounds and not a wall
        if (0 <= target_x < len(maze) and 0 <= target_y < len(maze[0]) and 
            maze[target_x][target_y] != 1):
            return (target_x, target_y)
        return pacman_pos  # Fallback to chasing
    
    elif personality == "random":
        # Sometimes chase, sometimes move randomly
        if random.random() < 0.7:  # 70% chance to chase
            return pacman_pos
        else:
            # Choose a random valid position within a certain range
            range_limit = 8
            while True:
                target_x = random.randint(max(0, ghost_pos[0] - range_limit), 
                                        min(len(maze) - 1, ghost_pos[0] + range_limit))
                target_y = random.randint(max(0, ghost_pos[1] - range_limit), 
                                        min(len(maze[0]) - 1, ghost_pos[1] + range_limit))
                if maze[target_x][target_y] != 1:  # Not a wall
                    return (target_x, target_y)
    
    elif personality == "patrol":
        # Define key patrol points (can be customized for specific maps)
        # For now, use corners and center as patrol points
        patrol_points = [
            (1, 1),  # Top-left (approximate)
            (1, len(maze[0]) - 2),  # Top-right
            (len(maze) - 2, 1),  # Bottom-left
            (len(maze) - 2, len(maze[0]) - 2),  # Bottom-right
            (len(maze) // 2, len(maze[0]) // 2)  # Center
        ]
        
        # Filter valid points (not walls)
        valid_points = [p for p in patrol_points if maze[p[0]][p[1]] != 1]
        
        if not valid_points:
            return pacman_pos  # Fallback
        
        # Chase Pacman if close, otherwise patrol
        manhattan_to_pacman = abs(ghost_pos[0] - pacman_pos[0]) + abs(ghost_pos[1] - pacman_pos[1])
        if manhattan_to_pacman < 5:  # Within 5 cells
            return pacman_pos
        else:
            # Choose closest patrol point not at current position
            valid_points = [p for p in valid_points if p != ghost_pos]
            if not valid_points:
                return pacman_pos  # Fallback
            
            # Find closest patrol point
            closest_point = min(valid_points, 
                              key=lambda p: abs(p[0] - ghost_pos[0]) + abs(p[1] - ghost_pos[1]))
            return closest_point
    
    # Default to chasing Pacman
    return pacman_pos

def predict_pacman_direction(maze, pacman_pos):
    """
    Simple function to predict Pacman's movement direction.
    This is a placeholder - in a real game, you would use Pacman's
    current velocity or analyze the board to make better predictions.
    
    Returns (dx, dy) direction vector.
    """
    # Define directions: up, right, down, left
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    
    # Find valid directions (not walls)
    valid_directions = []
    for dx, dy in directions:
        next_pos = (pacman_pos[0] + dx, pacman_pos[1] + dy)
        if (0 <= next_pos[0] < len(maze) and 
            0 <= next_pos[1] < len(maze[0]) and 
            maze[next_pos[0]][next_pos[1]] != 1):
            valid_directions.append((dx, dy))
    
    if not valid_directions:
        return (0, 0)  # No valid direction
    
    # In a real implementation, you would use Pacman's current direction
    # and possibly analyze the food distribution to make better predictions
    import random
    return random.choice(valid_directions)

def ghost_controller(maze, ghost_data, pacman_pos, power_pellet_active=False):
    """
    Main controller for ghosts using A* algorithm.
    
    Parameters:
    - maze: 2D grid of the game board
    - ghost_data: List of dictionaries with ghost information
                  Each dict contains: 'position', 'personality', 'scared' flags
    - pacman_pos: Current position of Pacman
    - power_pellet_active: Boolean indicating if Pacman has eaten a power pellet
    
    Returns:
    - List of next positions for each ghost
    """
    next_positions = []
    
    for ghost in ghost_data:
        current_pos = ghost['position']
        personality = ghost['personality']
        
        if power_pellet_active:
            # Ghosts run away when Pacman has a power pellet
            # Calculate a "run away" target that's opposite to Pacman
            run_direction = (
                current_pos[0] - pacman_pos[0],
                current_pos[1] - pacman_pos[1]
            )
            
            # Normalize
            magnitude = max(1, abs(run_direction[0]) + abs(run_direction[1]))
            normalized_direction = (
                int(run_direction[0] / magnitude * 10),
                int(run_direction[1] / magnitude * 10)
            )
            
            # Calculate target far from Pacman
            run_target = (
                max(0, min(len(maze) - 1, current_pos[0] + normalized_direction[0])),
                max(0, min(len(maze[0]) - 1, current_pos[1] + normalized_direction[1]))
            )
            
            # Use A* to find path away from Pacman
            next_pos = ghost_astar_search(maze, current_pos, run_target, "random")
        else:
            # Normal ghost behavior
            next_pos = ghost_astar_search(maze, current_pos, pacman_pos, personality)
        
        next_positions.append(next_pos)
    
    return next_positions
