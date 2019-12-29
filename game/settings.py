import pygame
from game.sprites import vec

FPS = 60
WIDTH = 1440
HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Player
PLAYER_FRICTION = -0.2
AIR_RESISTANCE = -0.1
PLAYER_ACC = 1.5
PLAYER_GRAVITY = 1
JUMP_SPEED = 5
THROW_SPEED_X = 50
THROW_SPEED_Y = -5

# TEST PLATFORMS

PLATFORM_LIST = [(WIDTH / 2, HEIGHT * 0.85, 100, 30),
                 (WIDTH / 2, HEIGHT * 0.65, 100, 30),
                 (WIDTH / 2, HEIGHT - 10, WIDTH, 30)]

# KEY ORDER: LEFT, RIGHT, UP, DOWN, PICKUP, DROP, THROW, SHOOT
PLAYER_LIST = [(50, 50, (111, 50, 200),
                [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_KP1, pygame.K_KP2, pygame.K_KP3,
                 pygame.K_KP0]),
               (1000, 50, (12, 200, 78),
                [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_e, pygame.K_q, pygame.K_r, pygame.K_f])]

GUN_PISTOL = (30, 7)
GUN_SNIPER = (80, 5, 500, 35, 20, 5)
GUN_ROCKET = ((250, 20), 80, 20, 1000, 10, 30, 15)

# ORDER: Pos, *Gun
GUN_LIST = [((50, 50), *GUN_PISTOL),
            ((1000, 50), *GUN_SNIPER)]
