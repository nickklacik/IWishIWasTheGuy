import pygame
import constants
from platforms import Platform
from levels import Level
from projectiles import TrippedProjectile
import random


class Enemy(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()


class Boss(Enemy):

    def __init__(self):
        super().__init__()

        self.health = 50
        health_width = 5 * self.health
        health_height = 20
        self.health_bar = Platform(health_width, health_height)
        self.health_bar.rect.x = constants.SCREEN_WIDTH - health_width - 20
        self.health_bar.rect.y = constants.SCREEN_HEIGHT - health_height - 20
        self.health_bar.image.fill(constants.RED)
        self.attack_counter = 0

        width = 112
        height = 300

        self.defineAnimations()
        self.image = self.idle[0]
        self.frame_counter = 0
        self.currentAnimation = self.idle

        self.rect = self.image.get_rect()
        self.rect.x = constants.SCREEN_WIDTH - width
        self.rect.y = constants.GROUND_HEIGHT - height

        self.defineWinScreen()

        self.game = None

    def update(self):
        group = self.game.projectile_list
        hit_list = pygame.sprite.spritecollide(self, group, True)
        lost_health = len(hit_list)
        self.health -= lost_health

        self.health_bar.rect.width -= 5 * lost_health
        self.health_bar.rect.width = max(0, self.health_bar.rect.width)
        self.health_bar.rect.x += 5 * lost_health
        dimensions = [self.health_bar.rect.width, self.health_bar.rect.height]
        self.health_bar.image = pygame.Surface(dimensions)
        self.health_bar.image.fill(constants.RED)

        if self.health <= 0:
            self.win_screen.load(True)
            self.game.game_over = True

        if self.attack_counter >= 180:
            self.currentAnimation = self.idle
            self.attack_counter = 0
            self.attack()
        elif self.attack_counter == 140:
            self.currentAnimation = self.laugh

        self.animate(self.currentAnimation, 6)

        self.attack_counter += 1

    def defineWinScreen(self):
        self.win_screen = Level()
        Level.level_list.pop(self.win_screen.level_num)
        self.win_screen.background.fill(constants.BLACK)
        self.win_screen.start_pos = (50, -120)
        platform0 = Platform(constants.SCREEN_WIDTH, 60)
        platform0.rect.x = 0
        platform0.rect.y = -60
        self.win_screen.platform_list.add(platform0)
        font = pygame.font.SysFont('Helvetica', 64, True, False)
        text = font.render("You Win", True, constants.WHITE)
        x = constants.SCREEN_WIDTH/2 - text.get_rect().width/2
        y = 250
        self.win_screen.background.blit(text, [x, y])

    def defineAnimations(self):
        self.idle = []
        self.idle.append(pygame.image.load("eggman.png"))
        self.idle.append(pygame.image.load("eggman1.png"))

        self.laugh = []
        self.laugh.append(pygame.image.load("eggman2.png"))
        self.laugh.append(pygame.image.load("eggman3.png"))

    def animate(self, animation, buffer):
        if self.frame_counter >= buffer * len(animation):
            self.frame_counter = 0
        self.image = animation[self.frame_counter//buffer]
        self.frame_counter += 1

    def attack(self):
        x = random.randint(0, 100)
        for i in range(0, 5):
            tp = TrippedProjectile()
            tp.player = self.game.player
            tp.rect.x = i*150 + x
            tp.rect.y = 50
            self.game.projectile_list.add(tp)
            self.game.all_sprites_list.add(tp)
