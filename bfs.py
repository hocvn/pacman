from collections import deque
import time

def ghost_bfs_search(start, goal, tiles):
    rows, cols = len(tiles), len(tiles[0])
    visited = set()
    queue = deque([(start, [start])])
    expanded_nodes = 0  # Đếm số nút được mở rộng
    max_queue_size = 1  # Theo dõi kích thước hàng đợi tối đa (cho memory usage)

    start_time = time.time()  # Đo thời gian bắt đầu

    while queue:
        current, path = queue.popleft()
        expanded_nodes += 1

        if current == goal:
            end_time = time.time()
            search_time = end_time - start_time
            return path, expanded_nodes#, search_time, max_queue_size, 

        if current in visited:
            continue
        visited.add(current)

        x, y = current
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Trái, Phải, Lên, Xuống
            nx, ny = x + dx, y + dy
            if 0 <= ny < rows and 0 <= nx < cols and tiles[ny][nx] != '#' and (nx, ny) not in visited:
                queue.append(((nx, ny), path + [(nx, ny)]))
                max_queue_size = max(max_queue_size, len(queue))

    return [], 0#, 0, expanded_nodes  # Không tìm thấy đường