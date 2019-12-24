import pygame
import game.settings as settings
from game.sprites import Player, Platform


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
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()

        # Add sprites to the groups

        for play in settings.PLAYER_LIST:
            player = Player(self, *play)
            self.players.add(player)
            self.all_sprites.add(player)

        for plat in settings.PLATFORM_LIST:
            platform = Platform(*plat)
            self.all_sprites.add(platform)
            self.platforms.add(platform)

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

        # Platform collision
        for player in self.players:
            print(player.vel.y)
            hits = pygame.sprite.spritecollide(player, self.platforms, False)
            if hits:
                for hit in hits:
                    print(hit)
                    player.pos.y = hit.rect.top
                    player.vel.y = 0
                    player.acc.y = 0
                    player.jumping = False

    def draw(self):
        self.screen.fill(self.white)
        self.all_sprites.draw(self.screen)
        pygame.display.flip()


g = Game()
print('Starting...')
while g.running:
    g.new()
