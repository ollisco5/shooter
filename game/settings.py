import pygame
FPS = 60
WIDTH = 1440
HEIGHT = 900
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Player
PLAYER_FRICTION = -0.2
PLAYER_ACC = 1.5
PLAYER_GRAVITY = 1
JUMP_SPEED = 5

# TEST PLATFORMS

PLATFORM_LIST = [(WIDTH/2, HEIGHT * 0.85, 100, 30),
                (WIDTH/2, HEIGHT * 0.65, 100, 30),
                 (WIDTH/2, HEIGHT-10, WIDTH, 30)]


PLAYER_LIST = [(50, 50, (111, 50, 200), pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP),
           (1000, 50, (12, 200, 78), pygame.K_a, pygame.K_d, pygame.K_w)]