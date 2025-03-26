import pygame
from collections import deque

# Initialize Pygame
pygame.init()

# Screen settings
N = 21
GRID_SIZE = 28
CHARACTER_SIZE = 24
WIDTH, HEIGHT = GRID_SIZE * N, GRID_SIZE * N
DISTANCE_WITH_WALL = 2
PACMAN_SPEED = 4
GHOST_SPEED = 4
ROWS, COLS = HEIGHT // GRID_SIZE, WIDTH // GRID_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man with 4 AI Ghosts")

# Colors
# Black: Background
# Green: Maze/Walls
# Yellow: Game Over text
BLACK, GREEN, YELLOW = (0, 0, 0), (0, 128, 0), (255, 255, 0)

# Right, Left, Up, Down
directions = [(PACMAN_SPEED, 0), (-PACMAN_SPEED, 0), (0, -PACMAN_SPEED), (0, PACMAN_SPEED)]

pacman_dir = (0, 0)

class Pacman(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.sprites = [
            pygame.image.load("./assets/pacman-1.png"), 
            pygame.image.load("./assets/pacman-2.png"), 
            pygame.image.load("./assets/pacman-3.png")
        ]
        # Resize images
        self.sprites = [pygame.transform.scale(img, (CHARACTER_SIZE, CHARACTER_SIZE)) for img in self.sprites]

        self.image = self.sprites[0] 
        self.rect = self.image.get_rect(topleft=(int(x), int(y)))
        self.index = 0  # index for animation
        self.angle = 0  # angle for rotation

    def update(self):
        # Animation
        self.index = (self.index + 1) % len(self.sprites)
        self.image = pygame.transform.rotate(self.sprites[self.index], self.angle)

    def Move(self, direction):
        dx, dy = directions[direction]
        # Move Pacman
        self.rect.x += dx
        self.rect.y += dy

        # Rotate Pacman
        if direction == 0:   # Right
            self.angle = 0
        elif direction == 1: # Left
            self.angle = 180
        elif direction == 2: # Up
            self.angle = 90
        elif direction == 3: # Down
            self.angle = -90


class Ghost(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.sprites = [pygame.image.load(f"./assets/{color}-ghost-{i}.png") for i in range(8)]
        # Resize image
        self.sprites = [pygame.transform.scale(img, (CHARACTER_SIZE, CHARACTER_SIZE)) for img in self.sprites]

        self.image = self.sprites[0]
        self.rect = self.image.get_rect(topleft=(int(x), int(y)))
        self.index = 0  # index for animation
        self.direction = -1

    def update(self):
        # Animation
        if self.index % 2 == 0:
            self.index += 1
        else:
            self.index += -1

        self.image = self.sprites[self.index]

    def Move(self, direction):
        dx, dy = directions[direction]
        # Move Ghost
        self.rect.x += dx
        self.rect.y += dy

        if direction != self.direction: # Change direction - avoid re-assiging sprite index
            self.direction = direction
            if direction == 0:
                self.index = 0      # Right
            elif direction == 1:
                self.index = 2      # Left
            elif direction == 2:
                self.index = 4      # Up
            elif direction == 3:
                self.index = 6      # Down
            self.image = self.sprites[self.index]

# Create Pacman
pacman = Pacman(GRID_SIZE * (N // 2) + DISTANCE_WITH_WALL // 2, GRID_SIZE * (N // 2) + DISTANCE_WITH_WALL // 2) # Center

# Create 4 ghosts
ghosts = [
    Ghost(GRID_SIZE + DISTANCE_WITH_WALL // 2, GRID_SIZE + DISTANCE_WITH_WALL // 2, "red"),                         # top-left
    Ghost(GRID_SIZE * (N - 2) + DISTANCE_WITH_WALL // 2, GRID_SIZE + DISTANCE_WITH_WALL // 2, "pink"),              # top-right
    Ghost(GRID_SIZE + DISTANCE_WITH_WALL // 2, GRID_SIZE * (N - 2) + DISTANCE_WITH_WALL // 2, "blue"),              # bottom-left
    Ghost(GRID_SIZE * (N - 2) + DISTANCE_WITH_WALL // 2, GRID_SIZE * (N - 2) + DISTANCE_WITH_WALL // 2, "orange")   # bottom-right
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

dot = pygame.image.load("./assets/dot.png")
dot = pygame.transform.scale(dot, (CHARACTER_SIZE, CHARACTER_SIZE))

# Create dots in the maze
for y, row in enumerate(tiles):
    for x, tile in enumerate(row):
        if tile == " ":
            screen.blit(dot, (x * GRID_SIZE + 2, y * GRID_SIZE + 2))

def check_collision(rect1, rect2):
    return rect1.colliderect(rect2)

def check_move_collision(rect, direction):
    next_position = rect.copy()

    next_position.x += directions[direction][0]
    next_position.y += directions[direction][1]

    return any(check_collision(next_position, pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
               for y, row in enumerate(tiles) for x, tile in enumerate(row) if tile == "#")


# Game loop
running = True
clock = pygame.time.Clock()
direction = -1
next_direction = -1

while running:

    # Fill screen with black color
    screen.fill(BLACK)

    # Draw maze
    for y, row in enumerate(tiles):
        for x, tile in enumerate(row):
            if tile == "#":
                pygame.draw.rect(screen, GREEN, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                next_direction = 0 # Right
            elif event.key == pygame.K_LEFT:
                next_direction = 1 # Left
            elif event.key == pygame.K_UP:
                next_direction = 2 # Up
            elif event.key == pygame.K_DOWN:
                next_direction = 3 # Down

    if next_direction != -1:    # Check if next direction is valid
        if not check_move_collision(pacman.rect, next_direction):
            pacman_dir = directions[next_direction]
            direction = next_direction

        if not check_move_collision(pacman.rect, direction):
            pacman.Move(direction)

    # Draw Pacman
    pacman.update()
    
    # Draw Ghosts
    red_ghost = ghosts[0]

    red_ghost.Move(0)
    red_ghost.update()

    blue_ghost = ghosts[2]
    blue_ghost.Move(2)
    blue_ghost.update()

    all_sprites.draw(screen)
    pygame.display.flip()

    if any(ghost.rect.colliderect(pacman.rect) for ghost in ghosts):
        running = False
        # print("Game Over")
        pygame.font.init()
        font = pygame.font.SysFont('Comic Sans MS', 50)
        text = font.render('Game Over', True, YELLOW)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

        # Pasuse screen for 2 seconds before closing
        pygame.display.flip()
        pygame.time.wait(2000)

    clock.tick(10)  # 10 FPS

pygame.quit()
