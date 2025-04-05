import pygame
from enum import Enum
from config import GRID_SIZE, WIDTH, HEIGHT

screen = pygame.display.set_mode((WIDTH, HEIGHT))

class WallType(Enum):
    UP= 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    LEFT_RIGHT = 4
    UP_DOWN = 5
    RIGHT_DOWN = 6
    LEFT_DOWN = 7
    LEFT_UP = 8
    RIGHT_UP = 9
    RIGHT_UP_DOWN = 10
    LEFT_UP_DOWN = 11
    LEFT_RIGHT_UP = 12
    LEFT_RIGHT_DOWN = 13
    LEFT_RIGHT_UP_DOWN = 14
    NONE = 15
    NULL = 16

wall_sprites = [pygame.transform.scale(pygame.image.load(f"./assets/wall/{i}.png"), (GRID_SIZE, GRID_SIZE)) for i in range(16)]

def classify_wall(tiles):
    rows, cols = len(tiles), len(tiles[0])
    wall_types = [[WallType.NULL for _ in range(cols)] for _ in range(rows)]

    for i in range(rows):
        for j in range(cols):
            if tiles[i][j] != '#':
                continue

            up = i > 0 and tiles[i - 1][j] == '#'
            down = i < rows - 1 and tiles[i + 1][j] == '#'
            left = j > 0 and tiles[i][j - 1] == '#'
            right = j < cols - 1 and tiles[i][j + 1] == '#'

            if left and right and up and down:
                wall_types[i][j] = WallType.LEFT_RIGHT_UP_DOWN
            elif left and right and up:
                wall_types[i][j] = WallType.LEFT_RIGHT_UP
            elif left and right and down:
                wall_types[i][j] = WallType.LEFT_RIGHT_DOWN
            elif left and up and down:
                wall_types[i][j] = WallType.LEFT_UP_DOWN
            elif right and up and down:
                wall_types[i][j] = WallType.RIGHT_UP_DOWN
            elif left and right:
                wall_types[i][j] = WallType.LEFT_RIGHT
            elif up and down:
                wall_types[i][j] = WallType.UP_DOWN
            elif left and up:
                wall_types[i][j] = WallType.LEFT_UP
            elif left and down:
                wall_types[i][j] = WallType.LEFT_DOWN
            elif right and up:
                wall_types[i][j] = WallType.RIGHT_UP
            elif right and down:
                wall_types[i][j] = WallType.RIGHT_DOWN
            elif up:
                wall_types[i][j] = WallType.UP
            elif down:
                wall_types[i][j] = WallType.DOWN
            elif left:
                wall_types[i][j] = WallType.LEFT
            elif right:
                wall_types[i][j] = WallType.RIGHT
            else:
                wall_types[i][j] = WallType.NONE  

    return wall_types

# Draw the grid with walls
def draw_grid(screen, tiles, wall_types):
    for i in range(len(tiles)):
        for j in range(len(tiles[0])):
            if tiles[i][j] == '#':
                wall_type = wall_types[i][j]
                index = wall_type.value
                if 0 <= index < len(wall_sprites):
                    screen.blit(wall_sprites[index], (j * GRID_SIZE, i * GRID_SIZE))