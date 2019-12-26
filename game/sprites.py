import game.settings as settings
from game.logic import Vector2
import pygame

vec = pygame.math.Vector2


class Physics(object):
    def __init__(self):
        # Player constants
        self.groundfriction = settings.PLAYER_FRICTION
        self.air_resistance = settings.AIR_RESISTANCE
        self.gravity = settings.PLAYER_GRAVITY
        self.player_acc = settings.PLAYER_ACC
        self.jumpspeed = settings.JUMP_SPEED
        self.throwspeed = vec(settings.THROW_SPEED_X, settings.THROW_SPEED_Y)

    def update(self, friction):
        self.acc.x += self.vel.x * friction
        self.vel += self.acc
        self.pos += self.vel + self.acc
        return self.pos

class InputHandler(object):
    def __init__(self, key_list):
        # KEY ORDER: LEFT, RIGHT, UP, DOWN, PICKUP, DROP, THROW, SHOOT
        self.key_left = key_list[0]
        self.key_right = key_list[1]
        self.key_jump = key_list[2]
        self.key_down = key_list[3]
        self.key_pickup = key_list[4]
        self.key_drop = key_list[5]
        self.key_throw = key_list[6]
        self.key_shoot = key_list[7]

class Eye(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((5, 5))
        self.image.fill(settings.BLACK)
        self.rect = self.image.get_rect()

class Player(pygame.sprite.Sprite, Physics, InputHandler):
    def __init__(self, game, x, y, color, key_list):
        Physics.__init__(self)
        InputHandler.__init__(self, key_list)  # Player
        pygame.sprite.Sprite.__init__(self)
        self.width = 20
        self.heigt = 40
        self.image = pygame.Surface((self.width, self.heigt))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (500, 500)
        self.game = game
        self.hand = self.rect.center
        # Holing should be gun object
        self.pickupable = []
        self.holding = None


        # Physics
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.jumping = False
        self.direction = 'right'
        self.eye = Eye()
        game.all_sprites.add(self.eye)
        # Controls

    def update(self):
        self.acc = vec(0, self.gravity)

        keys = pygame.key.get_pressed()
        # Jump
        if keys[self.key_jump]:
            # self.pos = vec(500, 500)
            self.jump()
        # Left and right
        if keys[self.key_left]:
            self.acc.x = -self.player_acc
            self.direction = 'left'
        if keys[self.key_right]:
            self.acc.x = self.player_acc
            self.direction = 'right'

        # Movement
        self.pos = Physics.update(self, settings.PLAYER_FRICTION)

        # Pickup, Drop, Throw
        if keys[self.key_pickup]:
            if self.pickupable and self.holding is None:
                self.pickup()
        if keys[self.key_drop]:
            if self.holding:
                self.drop(throw=False)
        if keys[self.key_throw]:
            if self.holding:
                self.drop(throw=True)
        if keys[self.key_shoot]:
            if self.holding:
                self.use()
        # End with updating rect
        self.rect.midbottom = self.pos

        if self.direction == 'right':
            self.eye.rect.center = (self.rect.right, self.rect.centery - int(self.width / 2))
        if self.direction == 'left':
            self.eye.rect.center = (self.rect.left, self.rect.centery - int(self.width / 2))

    def jump(self):
        self.rect.y += 1
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 1
        if hits and not self.jumping:
            self.vel.y -= 20
            self.jumping = True

    def pickup(self):
        item = self.pickupable[0]
        self.holding = item
        item.locked = True
        item.parent = self
        item.pos = self.rect.center

    def drop(self, throw):
        item = self.holding
        item.locked = False
        item.parent = None
        self.holding = None
        item.pos = item.rect.center
        if throw:
            if self.direction == 'left':
                item.vel = vec(-self.throwspeed.x, self.throwspeed.y)
            if self.direction == 'right':
                item.vel = vec(self.throwspeed)

    def use(self):
        self.holding.shoot()

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.width = w
        self.height = h
        self.pos = vec(x, y)
        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.top = y + h / 2

    def update(self):
        pass


class Gun(pygame.sprite.Sprite, Physics):
    def __init__(self, game, pos, w, h, firerate=250, bulletspeed=10, bulletw=10, bulleth=5, color=(123, 123, 123), recoil=5, type='weapon'):
        pygame.sprite.Sprite.__init__(self)
        Physics.__init__(self)
        self.game = game
        self.width = w
        self.height = h
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        # Defines sprite holding the gun
        self.parent = None
        # If the gun is in a hand
        self.locked = False
        self.firerate = firerate
        self.last_shot = pygame.time.get_ticks()
        self.bulletspeed = bulletspeed
        self.bulletw = bulletw
        self.bulleth = bulleth


        # Physics
        self.pos = vec(pos)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.gravity = settings.PLAYER_GRAVITY


    def update(self):
        if not self.locked:
            self.acc = vec(0, self.gravity)
            self.pos = Physics.update(self, settings.AIR_RESISTANCE)

            # End with updating rect
            self.rect.midbottom = self.pos

        if self.locked:
            self.rect.center = self.parent.rect.center

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.firerate:
            bullet = Bullet(self, self.parent, self.bulletspeed, self.bulletw, self.bulleth)
            self.game.all_sprites.add(bullet)
            self.game.bullets.add(bullet)
            self.last_shot = now

class Bullet(pygame.sprite.Sprite, Physics):
    def __init__(self, gun, shooter, absbulletspeed, w=10, h=5):
        Physics.__init__(self)
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h))
        self.image.fill(settings.BLACK)
        self.rect = self.image.get_rect()
        self.direction = shooter.direction
        self.shooter = shooter
        self.bulletspeed = absbulletspeed
        if self.direction == 'left':
            self.pos = vec(gun.rect.midleft)
            self.rect.midright = self.pos
            self.bulletspeed = -self.bulletspeed
        if self.direction == 'right':
            self.pos = vec(gun.rect.midright)
            self.rect.midleft = self.pos
        self.vel = vec(self.bulletspeed, 0)
        self.acc = vec(0, 0)



    def update(self):
        self.pos = Physics.update(self, friction=0)
        self.rect.center = self.pos
        # Destroys bullet if outside screen
        if self.pos.x < 0 or self.pos.x > settings.WIDTH:
            self.kill()


class Usable:
    def __init__(self):
        pass

    def drop(self):
        pass

    def throw(self):
        pass

    def use(self):
        pass
