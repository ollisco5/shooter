import pygame
import game.settings as settings
from game.sprites import Player, Platform, Gun, vec
from itertools import chain


class Game(object):
    def __init__(self):
        pygame.init()
        self.running = True
        self.width = settings.WIDTH
        self.height = settings.HEIGHT
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.fps = settings.FPS
        self.clock = pygame.time.Clock()

        # Colors
        self.black = settings.BLACK
        self.white = settings.WHITE

    def new(self):
        self.playing = True

        # Create sprite groups
        self.players = pygame.sprite.Group()
        self.guns = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.fallings = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()

        # Add sprites to the groups

        for play in settings.PLAYER_LIST:
            player = Player(self, *play)
            self.players.add(player)
            self.all_sprites.add(player)

        for plat in settings.PLATFORM_LIST:
            platform = Platform(*plat)
            self.all_sprites.add(platform)
            self.platforms.add(platform)

        for g in settings.GUN_LIST:
            gun = Gun(self, *g)
            self.all_sprites.add(gun)
            self.guns.add(gun)



        self.run()

    def run(self):

        while self.playing:
            self.clock.tick(self.fps)
            self.events()
            self.update()
            self.draw()

    def quit(self):
        self.running = False
        self.playing = False if self.playing else True

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.quit()
            if event.type == pygame.QUIT:
                self.quit()

    def update(self):
        self.all_sprites.update()

        # Platform collision for players
        for thing in chain(self.players, self.guns):
            hits = pygame.sprite.spritecollide(thing, self.platforms, False)

            if hits:
                for hit in hits:

                    if thing.vel.y > 0:
                        thing.pos.y = hit.rect.top
                        thing.vel.y = 0
                        thing.acc.y = 0
                        thing.jumping = False


        # Check if player can pickup a gun
        for player in self.players:
            player.pickupable = []
            pickups = pygame.sprite.spritecollide(player, self.guns, False)
            if pickups:
                for pickup in pickups:
                    player.pickupable.append(pickup)
            hits = pygame.sprite.spritecollide(player, self.bullets, True)
            if hits:
                for bullet in hits:
                    if player != bullet.shooter:
                        player.eye.kill()
                        player.kill()
            #print(player.pickupable)


    def draw(self):
        self.screen.fill(self.white)
        self.all_sprites.draw(self.screen)
        pygame.display.flip()


g = Game()
print('Starting...')
while g.running:
    g.new()
