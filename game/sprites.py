import game.settings as settings
from game.logic import Vector2
import pygame

vec = pygame.math.Vector2


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y, color, key_left, key_right, key_jump):
        # Player
        pygame.sprite.Sprite.__init__(self)
        self.width = 20
        self.heigt = 40
        self.image = pygame.Surface((self.width, self.heigt))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (500, 500)
        self.game = game

        # Player constants
        self.friction = settings.PLAYER_FRICTION
        self.gravity = settings.PLAYER_GRAVITY
        self.player_acc = settings.PLAYER_ACC
        self.jumpspeed = settings.JUMP_SPEED

        # Physics
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.jumping = False

        # Controls
        self.key_right = key_right
        self.key_left = key_left
        self.key_jump = key_jump

    def update(self):
        self.acc = vec(0, self.gravity)

        keys = pygame.key.get_pressed()
        if keys[self.key_jump]:
            # self.pos = vec(500, 500)
            self.jump()


        if keys[self.key_left]:
            self.acc.x = -self.player_acc
        if keys[self.key_right]:
            self.acc.x = self.player_acc

        self.acc.x += self.vel.x * self.friction
        self.vel += self.acc
        self.pos += self.vel + self.acc

        # Check if outside screen
        # TEMP
        if self.pos.y > settings.HEIGHT:
            self.vel.y = 0
            self.pos.y = settings.HEIGHT

        if self.pos.y < 0:
            self.pos.y = 0 + self.heigt

            self.vel.y = 0



        # End with updating rect
        self.rect.midbottom = self.pos


    def jump(self):
        self.rect.y += 1
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 1
        if hits and not self.jumping:
            print('T 2 J')
            self.vel.y -= 20
            self.jumping = True

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.width = w
        self.height = h
        self.pos = vec(x, y)
        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.top = y + h/2

    def update(self):
        pass
