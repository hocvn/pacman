import pygame
from enum import Enum
from DFS import ghost_dfs_search
from UCS import ghost_uniform_cost_search
from AStar import ghost_astar_search 

# Initialize Pygame
pygame.init()

# Screen settings
N = 21
GRID_SIZE = 28
CHARACTER_SIZE = 26
WIDTH, HEIGHT = GRID_SIZE * N, GRID_SIZE * N
DISTANCE_WITH_WALL = 2
PACMAN_SPEED = 2
GHOST_SPEED = 2
ROWS, COLS = HEIGHT // GRID_SIZE, WIDTH // GRID_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man with 4 AI Ghosts")

# Colors
BLACK, GREEN, YELLOW = (0, 0, 0), (0, 128, 0), (255, 255, 0)

# Directions: Right, Left, Up, Down
class Direction(Enum):
    NONE = (0, 0)
    RIGHT = (PACMAN_SPEED, 0)
    LEFT = (-PACMAN_SPEED, 0)
    UP = (0, -PACMAN_SPEED)
    DOWN = (0, PACMAN_SPEED)

pacman_dir = (0, 0)

dot_img = pygame.image.load("./assets/dot.png")
dot_img = pygame.transform.scale(dot_img, (CHARACTER_SIZE // 2, CHARACTER_SIZE // 2))
dot_positions = set()

def pixel_to_grid(x, y):
    return x // GRID_SIZE, y // GRID_SIZE

def grid_to_pixel(x, y):
    return x * GRID_SIZE + DISTANCE_WITH_WALL // 2, y * GRID_SIZE + DISTANCE_WITH_WALL // 2

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
        dx, dy = direction.value
        self.rect.x += dx
        self.rect.y += dy
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
        self.last_position = pixel_to_grid(x, y)
        
    def update(self):
        if self.index % 2 == 0:
            self.index += 1
        else:
            self.index -= 1
        self.image = self.sprites[self.index]

    def Move(self, direction):
        dx, dy = direction.value
        current_position = self.rect.copy()
        self.rect.x += dx
        self.rect.y += dy

        if pixel_to_grid(self.rect.x, self.rect.y) != pixel_to_grid(current_position.x, current_position.y):
            self.last_position = pixel_to_grid(current_position.x, current_position.y)

        if self.color == "pink":
            print(pixel_to_grid(self.rect.x, self.rect.y))
            print(pixel_to_grid(current_position.x, current_position.y))
            print(self.last_position)

        if direction != self.direction:
            self.direction = direction

            if direction == Direction.RIGHT: self.index = 0
            elif direction == Direction.LEFT: self.index = 2
            elif direction == Direction.UP: self.index = 4
            elif direction == Direction.DOWN: self.index = 6
            self.image = self.sprites[self.index]

pacman = Pacman(GRID_SIZE * (N // 2) + DISTANCE_WITH_WALL // 2, GRID_SIZE * (N // 2) + DISTANCE_WITH_WALL // 2)

ghosts = [
    Ghost(GRID_SIZE + DISTANCE_WITH_WALL // 2, GRID_SIZE + DISTANCE_WITH_WALL // 2, "red"),                         ## Red ghost - top left
    Ghost(GRID_SIZE * (N - 2) + DISTANCE_WITH_WALL // 2, GRID_SIZE + DISTANCE_WITH_WALL // 2, "pink"),              ## Pink ghost - top right
    Ghost(GRID_SIZE + DISTANCE_WITH_WALL // 2, GRID_SIZE * (N - 2) + DISTANCE_WITH_WALL // 2, "blue"),              ## Blue ghost - bottom left
    Ghost(GRID_SIZE * (N - 2) + DISTANCE_WITH_WALL // 2, GRID_SIZE * (N - 2) + DISTANCE_WITH_WALL // 2, "orange")     ## Orange ghost - bottom right
]

all_sprites = pygame.sprite.Group()
all_sprites.add(pacman, *ghosts)

tiles = [
    "#####################",
    "#                   #",
    "# ### ### ### ### ###",
    "# #   #       #   # #",
    "# # ### # # # ### # #",
    "#     #   #   #     #",
    "### # ###   ### # ###",
    "#   #     #     #   #",
    "# ### ### # ### ### #",
    "# #   #   #   #   # #",
    "# ### ###   ### ### #",
    "#   #           #   #",
    "### # #### #### # ###",
    "#               #   #",
    "# ### ### # ### ### #",
    "# #   #       #   # #",
    "# ###   #####   ### #",
    "#     #       #     #",
    "# ### # ##### # #####",
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
    dx, dy = direction.value

    next_position.x += dx
    next_position.y += dy
    return any(check_collision(next_position, pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
               for y, row in enumerate(tiles) for x, tile in enumerate(row) if tile == "#")


# Function to move the ghost towards the next position in the path which is calculated by the algorithm
def move_ghost(ghost, path):
    if len(path) < 2:
        return
    
    direction = ghost.direction
    next_pos = path[1]

    tx, ty = grid_to_pixel(*next_pos)
    gx, gy = ghost.rect.x, ghost.rect.y

    if ghost.color == "pink":
        print(pixel_to_grid(gx, gy))
        print(pixel_to_grid(tx, ty))

    if tx > gx and not check_move_collision(ghost.rect, Direction.RIGHT):
        direction = Direction.RIGHT
    elif tx < gx and not check_move_collision(ghost.rect, Direction.LEFT):
        direction = Direction.LEFT
    elif ty < gy and not check_move_collision(ghost.rect, Direction.UP):
        direction = Direction.UP
    elif ty > gy and not check_move_collision(ghost.rect, Direction.DOWN):
        direction = Direction.DOWN

    ghost.Move(direction)

    if ghost.color == "pink":
        print(direction)

running = True
clock = pygame.time.Clock()
direction = Direction.NONE
next_direction = Direction.NONE
loop = 0

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
            if event.key == pygame.K_RIGHT: next_direction = Direction.RIGHT
            elif event.key == pygame.K_LEFT: next_direction = Direction.LEFT
            elif event.key == pygame.K_UP: next_direction = Direction.UP
            elif event.key == pygame.K_DOWN: next_direction = Direction.DOWN

    # Pacman movement
    if next_direction != Direction.NONE:
        if not check_move_collision(pacman.rect, next_direction):
            pacman_dir = next_direction.value
            direction = next_direction

    if direction != Direction.NONE and not check_move_collision(pacman.rect, direction):
        pacman.Move(direction)

    px, py = pixel_to_grid(pacman.rect.centerx, pacman.rect.centery)
    if (px, py) in dot_positions:
        dot_positions.remove((px, py))

    if loop % 3 == 0: 
        pacman.update()

    # Ghost movement
    pacman_pos = pixel_to_grid(pacman.rect.x, pacman.rect.y)

    for ghost in ghosts:
        ghost_pos = pixel_to_grid(ghost.rect.x, ghost.rect.y)
        path = []

        if ghost.color == "red":
            continue
            path = ghost_astar_search(tiles, ghost_pos, pacman_pos)
        elif ghost.color == "pink":
            path = ghost_dfs_search(ghost_pos, pacman_pos, tiles, ghost.last_position)
        elif ghost.color == "blue":
            pass # TODO: Implement BFS algorithm for blue ghost
        elif ghost.color == "orange":
            continue
            path = ghost_uniform_cost_search(ghost_pos, pacman_pos, tiles)

        move_ghost(ghost, path)
        if loop % 3 == 0:
            ghost.update()

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
            pygame.time.wait(3000)

    loop = (1 + loop) % 3
    clock.tick(30)

pygame.quit()
