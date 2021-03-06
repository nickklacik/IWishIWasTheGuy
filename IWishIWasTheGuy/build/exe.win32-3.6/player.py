import pygame
import constants
from platforms import MovingPlatform
from projectiles import Bullet
from spritesheet_functions import SpriteSheet


class Player(pygame.sprite.Sprite):

    WIDTH = 48
    HEIGHT = 48

    # -- Methods
    def __init__(self):
        """ Constructor function """

        # Call the parent's constructor
        super().__init__()

        # Load all of the player's animations
        self.defineAnimations()
        self.image = self.idle[0]
        self.frame_counter = 0

        # Set a reference to the image rect.
        self.rect = self.image.get_rect()

        # Set speed vector of player
        self.x_change = 0
        self.y_change = 0

        self.facing_right = True

        self.game = None

        # Load sounds
        self.jump_sound = pygame.mixer.Sound("jump_sound.ogg")
        self.double_jump_sound = pygame.mixer.Sound("double_jump_sound.ogg")
        self.shoot_sound = pygame.mixer.Sound("shoot.ogg")

    def defineAnimations(self):
        spritesheet = SpriteSheet("TheKid.png")

        # Define idle animation
        self.idle = []
        img = spritesheet.get_image(0, 0, Player.WIDTH//2, Player.HEIGHT//2)
        self.idle.append(pygame.transform.scale2x(img))
        img = spritesheet.get_image(27, 0, Player.WIDTH//2, Player.HEIGHT//2)
        self.idle.append(pygame.transform.scale2x(img))
        img = spritesheet.get_image(55, 0, Player.WIDTH//2, Player.HEIGHT//2)
        self.idle.append(pygame.transform.scale2x(img))
        img = spritesheet.get_image(82, 0, Player.WIDTH//2, Player.HEIGHT//2)
        self.idle.append(pygame.transform.scale2x(img))

        # Define walking animation
        self.walking = []
        img = spritesheet.get_image(1, 25, Player.WIDTH//2, Player.HEIGHT//2)
        self.walking.append(pygame.transform.scale2x(img))
        img = spritesheet.get_image(31, 25, Player.WIDTH//2, Player.HEIGHT//2)
        self.walking.append(pygame.transform.scale2x(img))
        img = spritesheet.get_image(59, 25, Player.WIDTH//2, Player.HEIGHT//2)
        self.walking.append(pygame.transform.scale2x(img))
        img = spritesheet.get_image(87, 25, Player.WIDTH//2, Player.HEIGHT//2)
        self.walking.append(pygame.transform.scale2x(img))
        img = spritesheet.get_image(118, 25, Player.WIDTH//2, Player.HEIGHT//2)
        self.walking.append(pygame.transform.scale2x(img))

        # Define jumping animation
        self.jumping = []
        img = spritesheet.get_image(0, 69, Player.WIDTH//2, Player.HEIGHT//2)
        self.jumping.append(pygame.transform.scale2x(img))
        img = spritesheet.get_image(24, 69, Player.WIDTH//2, Player.HEIGHT//2)
        self.jumping.append(pygame.transform.scale2x(img))

        # Define falling animation
        self.falling = []
        img = spritesheet.get_image(4, 101, Player.WIDTH//2, Player.HEIGHT//2)
        self.falling.append(pygame.transform.scale2x(img))
        img = spritesheet.get_image(33, 101, Player.WIDTH//2, Player.HEIGHT//2)
        self.falling.append(pygame.transform.scale2x(img))

    def update(self):
        # Gravity
        self.calc_grav()

        # Save current x and y value before changes
        previous_x = self.rect.x
        previous_y = self.rect.y

        # Move left/right based on colliding Moving Platforms
        self.rect.y += 2
        group = self.game.current_level.platform_list
        block_hit_list = pygame.sprite.spritecollide(self, group, False)
        self.rect.y -= 2
        for block in block_hit_list:
            if isinstance(block, MovingPlatform):
                self.rect.x += block.x_change

        # Move left/right
        self.rect.x += self.x_change

        # See if we hit anything
        group = self.game.current_level.platform_list
        block_hit_list = pygame.sprite.spritecollide(self, group, False)
        for block in block_hit_list:
            if self.rect.x < previous_x:
                self.rect.left = block.rect.right
            else:
                self.rect.right = block.rect.left

        # Move up/down
        self.rect.y += self.y_change

        # Check and see if we hit anything
        group = self.game.current_level.platform_list
        block_hit_list = pygame.sprite.spritecollide(self, group, False)
        for block in block_hit_list:
            # Reset our position based on the top/bottom of the object.
            if block.rect.y > previous_y:
                self.rect.bottom = block.rect.top
                self.double_jump = True
            else:
                self.rect.top = block.rect.bottom

            # Stop our vertical movement
            self.y_change = 0

        # Check and see if we hit any projectiles
        group = self.game.projectile_list
        projectile_hit_list = pygame.sprite.spritecollide(self, group, False)

        for projectile in projectile_hit_list:
            if not isinstance(projectile, Bullet):
                self.die()

        if self.rect.y > constants.SCREEN_HEIGHT:
            self.die()

        group = self.game.current_level.enemy_list
        hit_list = pygame.sprite.spritecollide(self, group, False)
        if len(hit_list) > 0:
            self.die()

        # Determine the player's current frame of animation
        if self.y_change < 0:
            self.animate(self.jumping, 4)
        elif self.y_change > 0:
            self.animate(self.falling, 4)
        elif self.x_change == 0:
            self.animate(self.idle, 6)
        else:
            self.animate(self.walking, 2)

    def animate(self, animation, buffer):
        if self.frame_counter >= buffer * len(animation):
            self.frame_counter = 0
        self.image = animation[self.frame_counter//buffer]
        self.frame_counter += 1

        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)

    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.y_change == 0:
            self.y_change = 1
        else:
            self.y_change += .35

    def jump(self):
        """ Called when user hits 'jump' button. """
        self.rect.y += 2
        group = self.game.current_level.platform_list
        platform_hit_list = pygame.sprite.spritecollide(self, group, False)
        self.rect.y -= 2

        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0:
            self.y_change = -8
            self.double_jump = True
            self.jump_sound.play()
        elif self.double_jump:
            self.y_change = -6
            self.double_jump = False
            self.double_jump_sound.play()

    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.x_change = -4
        self.facing_right = False

    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.x_change = 4
        self.facing_right = True

    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.x_change = 0

    def shoot(self):
        if self.facing_right:
            bullet = Bullet(1)
            bullet.rect.x = self.rect.right + self.x_change
            bullet.rect.y = self.rect.centery
        else:
            bullet = Bullet(-1)
            bullet.rect.x = self.rect.x - Bullet.WIDTH + self.x_change
            bullet.rect.y = self.rect.centery

        self.game.all_sprites_list.add(bullet)
        self.game.projectile_list.add(bullet)
        self.shoot_sound.play()

    def die(self):
        self.game.current_level.load(True)
