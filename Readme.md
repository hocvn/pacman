# Pacman AI Ghost Pathfinding Report

## 📌 Project Overview

This project implements various search algorithms (DFS, BFS, UCS, A*) to control ghost movement in a Pacman-style game. The ghosts are programmed to chase Pacman based on different pathfinding strategies, and we evaluate their performance across multiple dimensions.

---

## 📋 1. Project Planning and Task Assignment (5 points)

Each group member was assigned specific responsibilities as listed below. Completion percentage reflects the contribution to the final report and implementation.

| Member Name | Responsibility                                 | Completion % | Individual Score (out of 9.0) |
|-------------|-------------------------------------------------|--------------|-------------------------------|
| A           | DFS Algorithm + Evaluation                      | 90%          | 9.0 * 90% = **8.1**           |
| B           | UCS + A* Algorithm, Charts and Visualization    | 100%         | 9.0 * 100% = **9.0**          |
| C           | BFS Algorithm + Memory Profiling                | 80%          | 9.0 * 80% = **7.2**           |
| D           | Integration + PDF Report and README Formatting  | 95%          | 9.0 * 95% = **8.55**          |

---

## 🧠 2. Algorithm Description (10 points)

### Depth-First Search (DFS)
- Explores as far as possible along each branch before backtracking.
- Implemented using a stack (LIFO).
- Not guaranteed to find the shortest path.

### Breadth-First Search (BFS)
- Explores all neighbors at the present depth prior to moving on to nodes at the next depth level.
- Implemented using a queue (FIFO).
- Guaranteed to find the shortest path (unweighted).

### Uniform Cost Search (UCS)
- Expands the node with the lowest total cost from the start node.
- Implements a priority queue with path cost as priority.
- Optimal for graphs with varying edge costs.

### A* Search
- Combines UCS with heuristics to guide the search.
- Priority = Cost so far + Heuristic estimate to goal.
- More efficient than UCS if the heuristic is admissible.

---

## 🔬 3. Experiments & Evaluation (15 points)

We evaluated each algorithm based on:
- ⏱️ **Search Time**
- 💾 **Memory Usage**
- 🔄 **Number of Expanded Nodes**

### Sample Test Case: Pink Ghost (DFS)
- Start: Top-left corner, Pacman: Center of Maze  
  > Memory usage: 0.183 MB (current), 0.395 MB (peak)  
  > Time taken: 32.92 seconds  
  > Expanded nodes: 118  

- Start: Top-right corner, Pacman: Center-bottom  
  > Memory usage: 0.178 MB (current), 0.389 MB (peak)  
  > Time taken: 46.38 seconds  
  > Expanded nodes: 173  

### Visualization

_Refer to the final PDF report for charts and visual comparison of the metrics across all algorithms._

---

## 📚 4. References

- [1] Artificial Intelligence: A Modern Approach - Russell & Norvig  
- [2] Pygame Documentation  
- [3] Python `heapq` and `collections.deque` modules  
- [4] tracemalloc — Track memory allocations in Python

---
