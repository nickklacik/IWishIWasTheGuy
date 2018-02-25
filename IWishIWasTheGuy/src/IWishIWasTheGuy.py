"""
Author: Nicholas Klacik
Version: Beta

The code defines a series of levels which the player must traverse through.
The player currently has unlimited lives. However, if the player gets hit or
falls off the level, it will be sent back to the beginning of the level.

How to play:
    Use the arrow keys to move and jump
    Use the X button to shoot
    Keep moving right to make it through each level
    Defeat the boss enemy at the final level to Win
    Enter starts/restarts the game
    numpad can be used to load different levels for debug purposes
"""

import pygame
import constants
from player import Player
from levels import Level
from platforms import Platform
from platforms import MovingPlatform
from platforms import Cannon
from enemies import Boss
from projectiles import TrippedProjectile


# --- Classes ---
class Game(object):
    """ This class represents an instance of the game. If we need to
        reset the game we'd just need to create a new instance of this
        class. """

    def __init__(self):
        """ Constructor. Create all our attributes and initialize
        the game. """
        self.all_sprites_list = pygame.sprite.Group()

        self.projectile_list = pygame.sprite.Group()

        self.player = Player()
        self.player.game = self
        self.all_sprites_list.add(self.player)

        self.start = False
        self.game_over = False

        Level.game = self
        self.current_level = None
        self.define_levels(-1, True)

        pygame.mixer.music.load("TameImpala-TheLessIKnowTheBetter8-Bit.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.3)

    def define_levels(self, level_num, init):
        # Define Level 0
        if init or level_num == 0:
            if init:
                level0 = Level()
                level0.start_pos = (100, constants.GROUND_HEIGHT-Player.HEIGHT)
                x = constants.SCREEN_WIDTH - self.player.rect.width
                y = constants.GROUND_HEIGHT-Player.HEIGHT
                level0.end_pos = (x, y)
            else:
                level0 = Level.level_list[0]
                level0.platform_list.empty()
                level0.enemy_list.empty()
                level0.tripped_projectiles.empty()

            platform0 = Platform(constants.SCREEN_WIDTH, 60)
            platform0.rect.x = 0
            platform0.rect.y = constants.SCREEN_HEIGHT - platform0.rect.height
            level0.platform_list.add(platform0)

            for i in range(4, 8):
                tp0 = TrippedProjectile()
                tp0.player = self.player
                tp0.rect.x = i*100
                tp0.rect.y = constants.GROUND_HEIGHT - 250
                level0.tripped_projectiles.add(tp0)

            hidden_wall = Platform(20, constants.SCREEN_HEIGHT)
            hidden_wall.rect.x = -20
            hidden_wall.rect.y = 0
            level0.platform_list.add(hidden_wall)

        # Define Level 1
        if init or level_num == 1:
            if init:
                level1 = Level()
                level1.start_pos = (0, constants.GROUND_HEIGHT-Player.HEIGHT)
                x = constants.SCREEN_WIDTH - self.player.rect.width
                y = constants.GROUND_HEIGHT-Player.HEIGHT
                level1.end_pos = (x, y)
            else:
                level1 = Level.level_list[1]
                level1.platform_list.empty()
                level1.enemy_list.empty()
                level1.tripped_projectiles.empty()

            platform0 = Platform(200, 60)
            platform0.rect.x = 0
            platform0.rect.y = constants.SCREEN_HEIGHT - platform0.rect.height
            level1.platform_list.add(platform0)

            platform1 = MovingPlatform(100, 20)
            platform1.player = self.player
            right = constants.SCREEN_WIDTH - platform1.rect.width - 140
            platform1.rect.x = right
            platform1.rect.y = constants.SCREEN_HEIGHT - 140
            platform1.x_change = -4
            platform1.boundary_left = 140
            platform1.boundary_right = right
            level1.platform_list.add(platform1)

            platform2 = Platform(200, 60)
            platform2.rect.x = constants.SCREEN_WIDTH - platform2.rect.width
            platform2.rect.y = constants.SCREEN_HEIGHT - platform2.rect.height
            level1.platform_list.add(platform2)

        # Define Level 2
        if init or level_num == 2:
            if init:
                level2 = Level()
                level2.start_pos = (0, constants.GROUND_HEIGHT-Player.HEIGHT)
                x = constants.SCREEN_WIDTH - self.player.rect.width
                y = constants.GROUND_HEIGHT-Player.HEIGHT
                level2.end_pos = (x, y)
            else:
                level2 = Level.level_list[2]
                level2.platform_list.empty()
                level2.enemy_list.empty()
                level2.tripped_projectiles.empty()

            platform0 = Platform(constants.SCREEN_WIDTH, 60)
            platform0.rect.x = 0
            platform0.rect.y = constants.SCREEN_HEIGHT - platform0.rect.height
            level2.platform_list.add(platform0)

            platform1 = Platform(20, constants.SCREEN_HEIGHT - 100)
            platform1.rect.x = constants.SCREEN_WIDTH/2
            platform1.rect.y = 100
            level2.platform_list.add(platform1)

            platform2 = MovingPlatform(100, 20)
            platform2.player = self.player
            right = constants.SCREEN_WIDTH - platform2.rect.width - 140
            platform2.rect.x = right
            platform2.rect.y = constants.SCREEN_HEIGHT - 140
            platform2.x_change = -4
            platform2.boundary_left = 40
            platform2.boundary_right = right + 100
            level2.platform_list.add(platform2)

            platform3 = MovingPlatform(100, 20)
            platform3.player = self.player
            platform3.rect.x = 200
            platform3.rect.y = 300
            platform3.y_change = -2
            platform3.boundary_bottom = constants.GROUND_HEIGHT - 140
            platform3.boundary_top = 100
            level2.platform_list.add(platform3)

            cannon0 = Cannon("left")
            cannon0.game = self
            cannon0.rect.x = constants.SCREEN_WIDTH - Cannon.WIDTH
            cannon0.rect.y = constants.GROUND_HEIGHT - 80
            level2.platform_list.add(cannon0)

            cannon1 = Cannon("left")
            cannon1.game = self
            cannon1.rect.x = constants.SCREEN_WIDTH - Cannon.WIDTH
            cannon1.rect.y = cannon0.rect.y - 60
            cannon1.fire_counter = 45
            level2.platform_list.add(cannon1)

            tp0 = TrippedProjectile()
            tp0.player = self.player
            tp0.rect.x = 700
            tp0.rect.y = 50
            level2.tripped_projectiles.add(tp0)

        # define final level
        if init or level_num == len(Level.level_list)-1:
            if init:
                final_level = Level()
                x = 100
                y = constants.GROUND_HEIGHT-Player.HEIGHT
                final_level.start_pos = (x, y)
                x = constants.SCREEN_WIDTH - self.player.rect.width
                final_level.end_pos = (x, y)
            else:
                final_level = Level.level_list[level_num]
                final_level.platform_list.empty()
                final_level.enemy_list.empty()
                final_level.tripped_projectiles.empty()

            platform0 = Platform(constants.SCREEN_WIDTH, 60)
            platform0.rect.x = 0
            platform0.rect.y = constants.SCREEN_HEIGHT - platform0.rect.height
            final_level.platform_list.add(platform0)

            hidden_wall = Platform(20, constants.SCREEN_HEIGHT)
            hidden_wall.rect.x = -20
            hidden_wall.rect.y = 0
            final_level.platform_list.add(hidden_wall)

            cannon0 = Cannon("left")
            cannon0.game = self
            cannon0.rect.x = constants.SCREEN_WIDTH - Cannon.WIDTH - 112
            cannon0.rect.y = constants.GROUND_HEIGHT - Cannon.HEIGHT
            final_level.platform_list.add(cannon0)

            boss = Boss()
            boss.game = self
            final_level.enemy_list.add(boss)
            final_level.platform_list.add(boss.health_bar)

    def process_events(self):
        """ Process all of the events. Return a "True" if we need
            to close the window. """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.go_left()
                if event.key == pygame.K_RIGHT:
                    self.player.go_right()
                if event.key == pygame.K_UP:
                    self.player.jump()
                if event.key == pygame.K_x:
                    self.player.shoot()
                if event.key == pygame.K_RETURN:
                    self.start = True
                    self.game_over = False
                    Level.level_list[0].load(True)
                if event.key == pygame.K_KP0:
                    Level.level_list[0].load(True)
                if event.key == pygame.K_KP1:
                    Level.level_list[1].load(True)
                if event.key == pygame.K_KP2:
                    Level.level_list[2].load(True)
                if event.key == pygame.K_KP3:
                    Level.level_list[3].load(True)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and self.player.x_change < 0:
                    self.player.stop()
                if event.key == pygame.K_RIGHT and self.player.x_change > 0:
                    self.player.stop()

        return False

    def run_logic(self):
        """
        This method is run each time through the frame. It
        updates positions and checks for collisions.
        """
        if self.start:
            # Check if a new level should be loaded
            if self.player.rect.x >= constants.SCREEN_WIDTH:
                Level.level_list[Level.current_level_num + 1].load(True)
            elif self.player.rect.x <= -self.player.rect.width:
                Level.level_list[Level.current_level_num - 1].load(False)

            if not self.game_over:
                # Move all the sprites
                self.all_sprites_list.update()

    def display_frame(self, screen):
        """ Display everything to the screen for the game. """
        screen.fill(constants.WHITE)

        if not self.start:
            title_font = pygame.font.SysFont('Helvetica', 64, True, False)
            text = "I Wish I was the Guy"
            title_text = title_font.render(text, True, constants.BLACK)
            x = constants.SCREEN_WIDTH/2 - title_text.get_rect().width/2
            y = 100
            screen.blit(title_text, [x, y])

            sub_font = pygame.font.SysFont('Helvetica', 28, True, False)
            text = "Press Enter to Start"
            sub_text = sub_font.render(text, True, constants.BLACK)
            x = constants.SCREEN_WIDTH/2 - sub_text.get_rect().width/2
            y = 400
            screen.blit(sub_text, [x, y])

            sub_font = pygame.font.SysFont('Helvetica', 28, True, False)
            text = "By: Nicholas Klacik"
            sub_text = sub_font.render(text, True, constants.BLACK)
            x = constants.SCREEN_WIDTH/2 - sub_text.get_rect().width/2
            y = 500
            screen.blit(sub_text, [x, y])
        else:
            screen.blit(self.current_level.background, [0, 0])

            if not self.game_over:
                self.all_sprites_list.draw(screen)

        pygame.display.flip()


def main():
    """ Main program function. """
    # Initialize Pygame and set up the window
    pygame.init()

    size = [constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("I Wish I was the Guy")
    pygame.mouse.set_visible(False)

    # Create our objects and set the data
    done = False
    clock = pygame.time.Clock()

    # Create an instance of the Game class
    game = Game()

    # Main game loop
    while not done:

        # Process events (keystrokes, mouse clicks, etc)
        done = game.process_events()

        # Update object positions, check for collisions
        game.run_logic()

        # Draw the current frame
        game.display_frame(screen)

        # Pause for the next frame
        clock.tick(60)

    # Close window and exit
    pygame.quit()

# Call the main function, start up the game
if __name__ == "__main__":
    main()
