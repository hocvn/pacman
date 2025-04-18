from enum import Enum

# Screen settings
N = 21
GRID_SIZE = 28
CHARACTER_SIZE = 28
WIDTH = GRID_SIZE * N
HEIGHT = GRID_SIZE * N

DISTANCE_WITH_WALL = 2
PACMAN_SPEED = 2
GHOST_SPEED = 2
DOT_SCORE = 10  # Points for each dot collected

ROWS = HEIGHT // GRID_SIZE
COLS = WIDTH // GRID_SIZE

# Directions: Right, Left, Up, Down
class Direction(Enum):
    NONE = (0, 0)
    RIGHT = (PACMAN_SPEED, 0)
    LEFT = (-PACMAN_SPEED, 0)
    UP = (0, -PACMAN_SPEED)
    DOWN = (0, PACMAN_SPEED)


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