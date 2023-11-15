# This file was created by: Chris Cozort
# Content from Chris Bradfield; Kids Can Code
# KidsCanCode - Game Development with Pygame video series
# Video link: https://youtu.be/OmlQ0XCvIn0 
from random import randint
# game settings 
WIDTH = 720
HEIGHT = 700
FPS = 30
SCORE = 0

# player settings
PLAYER_JUMP = 25
PLAYER_GRAV = 1.25
global PLAYER_FRIC
PLAYER_FRIC = 0.3

# #initial values of all players/enemies for new SI game:
# BLOCKERS_POSITION = 450
# ENEMY_DEFAULT_POSITION = 65  
# ENEMY_MOVE_DOWN = 35

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (203, 0, 255)
YELLOW = (255, 255, 0)

GROUND = (0, HEIGHT - 40, WIDTH, 40, "normal")

# create platform list w/ tuples to define parameters from Platform class
PLATFORM_LIST = [(WIDTH / 2 - 50, HEIGHT * 3 / 4, 100, 20,"moving"),
                 (125, HEIGHT - 350, 100, 20, "normal"),
                 (300, 220, 100, 20, "moving"),
                 (175, 100, 200, 20, "normal"),
                 (150, HEIGHT - 125, 100, 20, "normal"),
                 (WIDTH / 2 - 50, HEIGHT * 1.5, 100, 20,"moving"),
                 (600, -160, 100, 20, "normal"),
                 (300, -235, 150, 20, "moving"),
                 (175, -100, 50, 20, "moving"),
                 (150, -350, 120, 20, "normal"),
                 (WIDTH / 2 - 50, HEIGHT * 2, 130, 20,"moving"),
                 (60, -400, 100, 20, "normal"),
                 (WIDTH - 70, -500, 75, 20, "moving"),
                 (175, -570, 200, 20, "normal"),
                 (450, -600, 100, 20, "moving"),
                 (WIDTH / 2 - 50, HEIGHT * 3.5, 130, 20,"moving"),
                 (60, -700, 100, 20, "normal"),
                 (WIDTH - 70, -880, 75, 20, "moving"),
                 (100, -940, 200, 20, "normal"),
                 (450, -1000, 100, 20, "moving"),
                 (WIDTH / 2 - 50, HEIGHT * 4.5, 130, 20,"moving"),
                 (60, -1178, 100, 20, "normal"),
                 (WIDTH - 70, -1200, 75, 20, "moving"),
                 (175, -1300, 200, 20, "normal"),
                 (450, -1500, 100, 20, "moving")
]
