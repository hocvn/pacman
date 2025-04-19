# Pacman AI Ghost Pathfinding Report

##  Project Overview

This project implements various search algorithms (DFS, BFS, UCS, A*) to control ghost movement in a Pacman-style game. Each ghost is driven by a different pathfinding strategy to chase Pacman in real-time. The project includes algorithmic implementation, performance evaluation, memory usage analysis, and final reporting.

---

##  1. Project Planning and Task Assignment (5 points)

Each member was assigned specific tasks, and all members achieved full task completion.

| MSSV      | Name              | Assigned Task                                                                 | Completion % | Individual Score (out of 9.0) |
|-----------|-------------------|------------------------------------------------------------------------------|--------------|-------------------------------|
| 22120050  | Hồ Mạnh Đào       | UCS implementation, Update README file                                      | 100%         | **9.0**                       |
| 22120113  | Nguyễn Việt Hoàng | BFS implementation, Game Menu, Scoring, Time & Memory Analysis              | 100%         | **9.0**                       |
| 22120115  | Đỗ Thái Học       | DFS implementation, Game UI, Time & Memory Analysis, Video Recording        | 100%         | **9.0**                       |
| 22120418  | Huỳnh Trần Ty     | A* implementation, Time & Memory Analysis, Graphs and Final Report Writing  | 100%         | **9.0**                       |

---

##  2. Algorithm Description (10 points)

### Depth-First Search (DFS)
- Explores as deep as possible before backtracking.
- Uses a stack (LIFO).
- May not find the shortest path.

### Breadth-First Search (BFS)
- Explores all nodes at the present depth before moving deeper.
- Uses a queue (FIFO).
- Guarantees the shortest path in unweighted graphs.

### Uniform Cost Search (UCS)
- Always expands the least-cost node.
- Uses a priority queue with actual cost as the priority.
- Finds the shortest path when costs vary.

### A* Search
- Uses cost-so-far + heuristic (estimated cost to goal).
- Efficient and optimal when using admissible heuristic.
- Speeds up search compared to UCS.

---

##  3. Experiments & Evaluation (15 points)

Search performance was evaluated based on:
-  Search Time (seconds)
-  Memory Usage (MB)
-  Number of Expanded Nodes

### Record of Search Time, Memory Usage, and Expanded Nodes

####  Pink Ghost – DFS

| Ghost Position        | Pacman Position         | Time (s) | Memory (MB) | Peak Memory (MB) | Expanded Nodes |
|-----------------------|--------------------------|----------|--------------|-------------------|-----------------|
| Top-left              | Center of maze           | 32.92    | 0.183794     | 0.394721          | 118             |
| Top-right             | Center-bottom of maze    | 46.38    | 0.178122     | 0.388914          | 173             |
| Bottom-left           | Right-center of maze     | 46.38    | 0.178122     | 0.388914          | 173             |
| Bottom-right          | Left-top of maze         | 43.13    | 0.181949     | 0.392876          | 185             |
| Center of maze        | Right-bottom of maze     | 44.95    | 0.179742     | 0.390669          | 173             |

####  Blue Ghost – BFS

| Ghost Position        | Pacman Position         | Time (s) | Memory (MB) | Peak Memory (MB) | Expanded Nodes |
|-----------------------|--------------------------|----------|--------------|-------------------|-----------------|
| Top-left              | Center of maze           | 7.91     | 0.188382     | 0.399309          | 104             |
| Top-right             | Center-bottom of maze    | 12.08    | 0.179135     | 0.389927          | 208             |
| Bottom-left           | Right-center of maze     | 13.92    | 0.182488     | 0.393415          | 225             |
| Bottom-right          | Left-top of maze         | 16.24    | 0.179675     | 0.390512          | 247             |
| Center of maze        | Right-bottom of maze     | 7.91     | 0.182082     | 0.392964          | 238             |

####  Orange Ghost – UCS

| Ghost Position        | Pacman Position         | Time (s) | Memory (MB) | Peak Memory (MB) | Expanded Nodes |
|-----------------------|--------------------------|----------|--------------|-------------------|-----------------|
| Top-left              | Center of maze           | 7.91     | 0.187842     | 0.398769          | 199             |
| Top-right             | Center-bottom of maze    | 12.08    | 0.181891     | 0.392773          | 407             |
| Bottom-left           | Right-center of maze     | 14.03    | 0.184186     | 0.395158          | 452             |
| Bottom-right          | Left-top of maze         | 16.25    | 0.181036     | 0.391918          | 490             |
| Center of maze        | Right-bottom of maze     | 7.91     | 0.178355     | 0.389147          | 467             |

####  Red Ghost – A*

| Ghost Position        | Pacman Position         | Time (s) | Memory (MB) | Peak Memory (MB) | Expanded Nodes |
|-----------------------|--------------------------|----------|--------------|-------------------|-----------------|
| Top-left              | Center of maze           | 7.89     | 0.186357     | 0.397284          | 42              |
| Top-right             | Center-bottom of maze    | 12.07    | 0.183209     | 0.394181          | 74              |
| Bottom-left           | Right-center of maze     | 13.91    | 0.179069     | 0.389906          | 142             |
| Bottom-right          | Left-top of maze         | 16.25    | 0.183659     | 0.394586          | 65              |
| Center of maze        | Right-bottom of maze     | 7.90     | 0.179157     | 0.390039          | 42              |

---

##  4. References

- Russell, S., & Norvig, P. (2010). *Artificial Intelligence: A Modern Approach*.  
- Pygame Documentation: https://www.pygame.org/docs/  
- Python Standard Library: `heapq`, `collections`, `tracemalloc`  
- [Your video demo link here if available]

---

##  5. Installation & How to Run the Program

###  Requirements

- Python 3.10+
- Pygame
- Tracemalloc (built-in)
- Các thư viện chuẩn như `heapq`, `deque`, `time`, v.v.

Cài đặt thư viện cần thiết bằng pip:
```bash
pip install pygame
