import pygame
import constants


class Level(object):

    current_level_num = None
    level_list = []
    game = None

    def __init__(self):
        self.start_pos = (0, 0)
        self.end_pos = (0, 0)

        dimensions = [constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT]
        self.background = pygame.Surface(dimensions)
        self.background.fill(constants.WHITE)

        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.tripped_projectiles = pygame.sprite.Group()

        self.level_num = len(Level.level_list)
        Level.level_list.append(self)

    def load(self, start):
        Level.current_level_num = self.level_num
        Level.game.current_level = self
        Level.game.define_levels(self.level_num, False)

        if start:
            Level.game.player.rect.x = self.start_pos[0]
            Level.game.player.rect.y = self.start_pos[1]
        else:
            Level.game.player.rect.x = self.end_pos[0]
            Level.game.player.rect.y = self.end_pos[1]

        Level.game.all_sprites_list.empty()
        Level.game.projectile_list.empty()
        Level.game.all_sprites_list.add(Level.game.player)
        Level.game.all_sprites_list.add(self.platform_list)
        Level.game.all_sprites_list.add(self.enemy_list)
        Level.game.all_sprites_list.add(self.tripped_projectiles)
        Level.game.projectile_list.add(self.tripped_projectiles)
