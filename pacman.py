import pygame
from collections import deque
import heapq
import time 
import tracemalloc

from AStar import ghost_astar_search 

# Initialize Pygame
pygame.init()

# Screen settings
N = 21
GRID_SIZE = 28
CHARACTER_SIZE = 24
WIDTH, HEIGHT = GRID_SIZE * N, GRID_SIZE * N
DISTANCE_WITH_WALL = 2
PACMAN_SPEED = 4
GHOST_SPEED = 3
ROWS, COLS = HEIGHT // GRID_SIZE, WIDTH // GRID_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man with 4 AI Ghosts")

# Colors
BLACK, GREEN, YELLOW = (0, 0, 0), (0, 128, 0), (255, 255, 0)

# Directions: Right, Left, Up, Down
directions = [(PACMAN_SPEED, 0), (-PACMAN_SPEED, 0), (0, -PACMAN_SPEED), (0, PACMAN_SPEED)]

pacman_dir = (0, 0)

dot_img = pygame.image.load("./assets/dot.png")
dot_img = pygame.transform.scale(dot_img, (CHARACTER_SIZE // 2, CHARACTER_SIZE // 2))
dot_positions = set()

class Pacman(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.sprites = [
            pygame.image.load("./assets/pacman-1.png"), 
            pygame.image.load("./assets/pacman-2.png"), 
            pygame.image.load("./assets/pacman-3.png")
        ]
        self.sprites = [pygame.transform.scale(img, (CHARACTER_SIZE, CHARACTER_SIZE)) for img in self.sprites]
        self.image = self.sprites[0] 
        self.rect = self.image.get_rect(topleft=(int(x), int(y)))
        self.index = 0
        self.angle = 0

    def update(self):
        self.index = (self.index + 1) % len(self.sprites)
        self.image = pygame.transform.rotate(self.sprites[self.index], self.angle)

    def Move(self, direction):
        dx, dy = directions[direction]
        self.rect.x += dx
        self.rect.y += dy
        if direction == 0: self.angle = 0
        elif direction == 1: self.angle = 180
        elif direction == 2: self.angle = 90
        elif direction == 3: self.angle = -90

class Ghost(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        color = color.lower()
        self.sprites = [pygame.image.load(f"./assets/{color}-ghost-{i}.png") for i in range(8)]
        self.sprites = [pygame.transform.scale(img, (CHARACTER_SIZE, CHARACTER_SIZE)) for img in self.sprites]
        self.image = self.sprites[0]
        self.rect = self.image.get_rect(topleft=(int(x), int(y)))
        self.index = 0
        self.direction = -1

    def update(self):
        if self.index % 2 == 0:
            self.index += 1
        else:
            self.index -= 1
        self.image = self.sprites[self.index]

    def Move(self, direction):
        dx, dy = directions[direction]
        self.rect.x += dx
        self.rect.y += dy
        if direction != self.direction:
            self.direction = direction
            if direction == 0: self.index = 0
            elif direction == 1: self.index = 2
            elif direction == 2: self.index = 4
            elif direction == 3: self.index = 6
            self.image = self.sprites[self.index]

pacman = Pacman(GRID_SIZE * (N // 2) + DISTANCE_WITH_WALL // 2, GRID_SIZE * (N // 2) + DISTANCE_WITH_WALL // 2)

ghosts = [
    Ghost(GRID_SIZE + DISTANCE_WITH_WALL // 2, GRID_SIZE + DISTANCE_WITH_WALL // 2, "red"),
    Ghost(GRID_SIZE * (N - 2) + DISTANCE_WITH_WALL // 2, GRID_SIZE + DISTANCE_WITH_WALL // 2, "pink"),
    Ghost(GRID_SIZE + DISTANCE_WITH_WALL // 2, GRID_SIZE * (N - 2) + DISTANCE_WITH_WALL // 2, "blue"),
    Ghost(GRID_SIZE * (N - 2) + DISTANCE_WITH_WALL // 2, GRID_SIZE * (N - 2) + DISTANCE_WITH_WALL // 2, "orange")
]

all_sprites = pygame.sprite.Group()
all_sprites.add(pacman, *ghosts)

tiles = [
    "#####################",
    "#                   #",
    "# ### ### ### ### ###",
    "# #   #   #   #   # #",
    "# # ### # # # ### # #",
    "#     #   #   #     #",
    "### # ###   ### # ###",
    "#   #     #     #   #",
    "# ### ### # ### ### #",
    "# #   #   #   #   # #",
    "# ### ###   ### ### #",
    "#   #           #   #",
    "### # ######### # ###",
    "#   #     #     #   #",
    "# ### ### # ### ### #",
    "# #   #       #   # #",
    "# ###   #####   ### #",
    "#     #       #     #",
    "# ### # ##### # ### #",
    "#                   #",
    "#####################",
]

for y, row in enumerate(tiles):
    for x, tile in enumerate(row):
        if tile == " ":
            dot_positions.add((x, y))

def check_collision(rect1, rect2):
    return rect1.colliderect(rect2)

def check_move_collision(rect, direction):
    next_position = rect.copy()
    next_position.x += directions[direction][0]
    next_position.y += directions[direction][1]
    return any(check_collision(next_position, pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
               for y, row in enumerate(tiles) for x, tile in enumerate(row) if tile == "#")

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

def pixel_to_grid(x, y):
    return x // GRID_SIZE, y // GRID_SIZE

def grid_to_pixel(x, y):
    return x * GRID_SIZE + DISTANCE_WITH_WALL // 2, y * GRID_SIZE + DISTANCE_WITH_WALL // 2

running = True
clock = pygame.time.Clock()
direction = -1
next_direction = -1

total_search_time = 0
total_memory_usage = 0
total_nodes_opened = 0

while running:
    screen.fill(BLACK)
    for y, row in enumerate(tiles):
        for x, tile in enumerate(row):
            if tile == "#":
                pygame.draw.rect(screen, GREEN, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    for dx, dy in dot_positions:
        screen.blit(dot_img, (dx * GRID_SIZE + GRID_SIZE // 4, dy * GRID_SIZE + GRID_SIZE // 4))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT: next_direction = 0
            elif event.key == pygame.K_LEFT: next_direction = 1
            elif event.key == pygame.K_UP: next_direction = 2
            elif event.key == pygame.K_DOWN: next_direction = 3

    if next_direction != -1:
        if not check_move_collision(pacman.rect, next_direction):
            pacman_dir = directions[next_direction]
            direction = next_direction

    if direction != -1 and not check_move_collision(pacman.rect, direction):
        pacman.Move(direction)

    px, py = pixel_to_grid(pacman.rect.centerx, pacman.rect.centery)
    if (px, py) in dot_positions:
        dot_positions.remove((px, py))

    pacman.update()

    # red ghost using A* search
    red_ghost = ghosts[0]
    red_ghost_pos = pixel_to_grid(ghosts[0].rect.x, ghosts[0].rect.y)
    pacman_pos = pixel_to_grid(pacman.rect.x, pacman.rect.y)
    
    
    tracemalloc.start()
    start_time = time.time()
    path_to_pacman, nodes_opened = ghost_astar_search(tiles, red_ghost_pos, pacman_pos)
    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    total_search_time += end_time - start_time
    total_memory_usage += current
    total_nodes_opened += nodes_opened
    
    
    if len(path_to_pacman) >= 2:
        next_pos = path_to_pacman[1]  # First step in the path
        tx, ty = grid_to_pixel(*next_pos)  # Convert to pixel position
        gx, gy = red_ghost.rect.x, red_ghost.rect.y
        if tx > gx and not check_move_collision(red_ghost.rect, 0):
            red_ghost.Move(0)
        elif tx < gx and not check_move_collision(red_ghost.rect, 1):
            red_ghost.Move(1)
        elif ty < gy and not check_move_collision(red_ghost.rect, 2):
            red_ghost.Move(2)
        elif ty > gy and not check_move_collision(red_ghost.rect, 3):
            red_ghost.Move(3)
    red_ghost.update()


    blue_ghost = ghosts[2]
    blue_ghost.Move(2)
    blue_ghost.update()                

    orange_ghost = ghosts[3]
    ghost_pos = pixel_to_grid(orange_ghost.rect.x, orange_ghost.rect.y)
    pacman_pos = pixel_to_grid(pacman.rect.x, pacman.rect.y)
    path = ucs(ghost_pos, pacman_pos, tiles)

    if len(path) >= 2:
        next_pos = path[1]
        tx, ty = grid_to_pixel(*next_pos)
        gx, gy = orange_ghost.rect.x, orange_ghost.rect.y
        if tx > gx and not check_move_collision(orange_ghost.rect, 0):
            orange_ghost.Move(0)
        elif tx < gx and not check_move_collision(orange_ghost.rect, 1):
            orange_ghost.Move(1)
        elif ty < gy and not check_move_collision(orange_ghost.rect, 2):
            orange_ghost.Move(2)
        elif ty > gy and not check_move_collision(orange_ghost.rect, 3):
            orange_ghost.Move(3)
    orange_ghost.update()

    all_sprites.draw(screen)
    pygame.display.flip()

    if any(ghost.rect.colliderect(pacman.rect) or
       pixel_to_grid(ghost.rect.centerx, ghost.rect.centery) == pixel_to_grid(pacman.rect.centerx, pacman.rect.centery)
       for ghost in ghosts):
        running = False
        pygame.font.init()
        font = pygame.font.SysFont('Comic Sans MS', 50)
        text = font.render('Game Over', True, YELLOW)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(2000)

    clock.tick(10)

print(f"Total A* Search Time: {total_search_time:.6f} seconds")
print(f"Total Peak Memory Usage: {total_memory_usage:.2f} KB")
print(f"Total Nodes Opened: {total_nodes_opened}")
pygame.quit()
