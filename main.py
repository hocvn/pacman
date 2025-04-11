import pygame
import time
import tracemalloc

from dfs import ghost_dfs_search
from ucs import ghost_uniform_cost_search
from a_star import ghost_astar_search 
from bfs import ghost_bfs_search

import draw_grid
from config import N, GRID_SIZE, WIDTH, HEIGHT, CHARACTER_SIZE, Direction, tiles

# Initialize Pygame
pygame.init()

# Screen settings
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man with 4 AI Ghosts")

# Colors
BLACK, GREEN, YELLOW = (0, 0, 0), (0, 128, 0), (255, 255, 0)

pacman_dir = (0, 0)

dot_img = pygame.image.load("./assets/dot.png")
dot_img = pygame.transform.scale(dot_img, (CHARACTER_SIZE // 2, CHARACTER_SIZE // 2))
dot_positions = set()

def pixel_to_grid(x, y):
    return x // GRID_SIZE, y // GRID_SIZE

def grid_to_pixel(x, y):
    return x * GRID_SIZE, y * GRID_SIZE

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
        self.next_direction = Direction.NONE
        self.direction = Direction.NONE
        self.last_position = pixel_to_grid(x, y)
        self.changed_position = False

    def update(self):
        self.index = (self.index + 1) % len(self.sprites)
        self.image = pygame.transform.rotate(self.sprites[self.index], self.angle)

    def Move(self, direction):
        prev_position = self.rect.copy()
        dx, dy = direction.value
        self.rect.x += dx
        self.rect.y += dy

        if pixel_to_grid(self.rect.x, self.rect.y) != pixel_to_grid(prev_position.x, prev_position.y):
            self.changed_position = True
            self.last_position = pixel_to_grid(prev_position.x, prev_position.y)
        else:
            self.changed_position = False

        if direction == Direction.RIGHT: self.angle = 0
        elif direction == Direction.LEFT: self.angle = 180
        elif direction == Direction.UP: self.angle = 90
        elif direction == Direction.DOWN: self.angle = -90

class Ghost(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.color = color.lower()
        self.sprites = [pygame.image.load(f"./assets/{color}-ghost-{i}.png") for i in range(8)]
        self.sprites = [pygame.transform.scale(img, (CHARACTER_SIZE, CHARACTER_SIZE)) for img in self.sprites]
        self.image = self.sprites[0]
        self.rect = self.image.get_rect(topleft=(int(x), int(y)))
        self.index = 0
        self.direction = Direction.NONE
        self.path = []
        self.last_position = pixel_to_grid(x, y)
        self.expanded_nodes = 0
        
    def update(self):
        if self.index % 2 == 0:
            self.index += 1
        else:
            self.index -= 1
        self.image = self.sprites[self.index]

    def Move(self, direction):
        dx, dy = direction.value
        prev_position = self.rect.copy()
        self.rect.x += dx
        self.rect.y += dy

        if pixel_to_grid(self.rect.x, self.rect.y) != pixel_to_grid(prev_position.x, prev_position.y):
            self.path.pop(0)
            self.last_position = pixel_to_grid(prev_position.x, prev_position.y)

        if direction != self.direction:
            self.direction = direction

            if direction == Direction.RIGHT: self.index = 0
            elif direction == Direction.LEFT: self.index = 2
            elif direction == Direction.UP: self.index = 4
            elif direction == Direction.DOWN: self.index = 6
            self.image = self.sprites[self.index]

pacman = Pacman(GRID_SIZE * (N // 2), GRID_SIZE * (N // 2))

ghosts = [
    Ghost(GRID_SIZE, GRID_SIZE, "red"),                         ## Red ghost - top left
    Ghost(GRID_SIZE * (N - 2), GRID_SIZE, "pink"),              ## Pink ghost - top right
    Ghost(GRID_SIZE, GRID_SIZE * (N - 2), "blue"),              ## Blue ghost - bottom left
    Ghost(GRID_SIZE * (N - 2), GRID_SIZE * (N - 2), "orange")   ## Orange ghost - bottom right
]

all_sprites = pygame.sprite.Group()
all_sprites.add(pacman, *ghosts)

for y, row in enumerate(tiles):
    for x, tile in enumerate(row):
        if tile == " ":
            dot_positions.add((x, y))

def check_collision(rect1, rect2):
    return rect1.colliderect(rect2)

def check_move_collision(rect, direction):
    next_position = rect.copy()
    dx, dy = direction.value

    next_position.x += dx
    next_position.y += dy
    return any(check_collision(next_position, pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
               for y, row in enumerate(tiles) for x, tile in enumerate(row) if tile == "#")

def get_ghost_path(ghost, pacman_pos):
    ghost_pos = pixel_to_grid(ghost.rect.x, ghost.rect.y)
    path = []
    expanded_nodes = 0

    if ghost.color == "red":
        path, expanded_nodes = ghost_astar_search(tiles, ghost_pos, pacman_pos)
    elif ghost.color == "pink":
        path, expanded_nodes = ghost_dfs_search(ghost_pos, pacman_pos, tiles, ghost.last_position)
    elif ghost.color == "blue":
        path, expanded_nodes = ghost_bfs_search(ghost_pos, pacman_pos, tiles)
    elif ghost.color == "orange":
        path, expanded_nodes = ghost_uniform_cost_search(ghost_pos, pacman_pos, tiles)
    
    return path, expanded_nodes

# Function to move the ghost towards the next position in the path which is calculated by the algorithm
def move_ghost(ghost, pacman_pos):
    if pacman.changed_position == True or ghost.path == []:
       ghost.path, ghost.expanded_nodes = get_ghost_path(ghost, pacman_pos)

    direction = ghost.direction
    next_pos = ghost.path[1]

    tx, ty = grid_to_pixel(*next_pos)
    gx, gy = ghost.rect.x, ghost.rect.y

    if tx > gx and not check_move_collision(ghost.rect, Direction.RIGHT):
        direction = Direction.RIGHT
    elif tx < gx and not check_move_collision(ghost.rect, Direction.LEFT):
        direction = Direction.LEFT
    elif ty < gy and not check_move_collision(ghost.rect, Direction.UP):
        direction = Direction.UP
    elif ty > gy and not check_move_collision(ghost.rect, Direction.DOWN):
        direction = Direction.DOWN

    ghost.Move(direction)

wall_types = draw_grid.classify_wall(tiles)

running = True
clock = pygame.time.Clock()
loop = 0

start_time = time.time()
tracemalloc.start()


while running:
    # Clear the screen
    screen.fill(BLACK)

    # Draw the grid
    draw_grid.draw_grid(screen, tiles, wall_types)

    # Draw the dots
    for dx, dy in dot_positions:
        screen.blit(dot_img, (dx * GRID_SIZE + GRID_SIZE // 4, dy * GRID_SIZE + GRID_SIZE // 4))

    # Key press event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT: pacman.next_direction = Direction.RIGHT
            elif event.key == pygame.K_LEFT: pacman.next_direction = Direction.LEFT
            elif event.key == pygame.K_UP: pacman.next_direction = Direction.UP
            elif event.key == pygame.K_DOWN: pacman.next_direction = Direction.DOWN

    # Pacman movement
    if pacman.next_direction != Direction.NONE and not check_move_collision(pacman.rect, pacman.next_direction):
        pacman_dir = pacman.next_direction.value
        pacman.direction = pacman.next_direction

    if pacman.direction != Direction.NONE and not check_move_collision(pacman.rect, pacman.direction):
        pacman.Move(pacman.direction)
    else:
        pacman.changed_position = False

    px, py = pixel_to_grid(pacman.rect.centerx, pacman.rect.centery)
    if (px, py) in dot_positions:
        dot_positions.remove((px, py))

    if loop % 3 == 0: 
        pacman.update()
    
    # Ghost movement
    pacman_pos = pixel_to_grid(pacman.rect.x, pacman.rect.y)

    for ghost in ghosts:
        move_ghost(ghost, pacman_pos)
        if loop % 3 == 0:
            ghost.update()
    
    pacman_movement = False

    all_sprites.draw(screen)
    pygame.display.flip()

    # Check if Pacman colliderect ghosts
    if any(ghost.rect.colliderect(pacman.rect) or
        pixel_to_grid(ghost.rect.x, ghost.rect.y) == pixel_to_grid(pacman.rect.x, pacman.rect.y)
        for ghost in ghosts):
            running = False
            pygame.font.init()
            font = pygame.font.SysFont('Comic Sans MS', 50)
            text = font.render('Game Over', True, YELLOW)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height()))
            text = font.render('Press any key to exit', True, GREEN)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
            pygame.display.flip()

            # Capture memory usage and time taken
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            print(f"Current memory usage: {current / 10**6}MB")
            print(f"Peak: {peak / 10**6}MB")
            end_time = time.time()
            search_time = end_time - start_time
            print(f"Time taken: {search_time:.2f} seconds")
            print(f"Expanded nodes: {ghosts[1].expanded_nodes}")
            
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        waiting = False
                    elif event.type == pygame.KEYDOWN:
                        waiting = False

    loop = (1 + loop) % 3
    clock.tick(30)

pygame.quit()
