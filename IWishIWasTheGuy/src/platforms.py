import pygame
import constants
from projectiles import Cannonball


class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """

    def __init__(self, width, height):
        """ Platform constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this code.
            """
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(constants.GREEN)

        self.rect = self.image.get_rect()

        self.player = None


class MovingPlatform(Platform):
    """ This is a fancier platform that can actually move. """
    def __init__(self, width, height):
        super().__init__(width, height)

        self.x_change = 0
        self.y_change = 0

        self.boundary_top = 0
        self.boundary_bottom = 0
        self.boundary_left = 0
        self.boundary_right = 0

    def update(self):
        """ Move the platform.
            If the player is in the way, it will shove the player
            out of the way. This does NOT handle what happens if a
            platform shoves a player into another object. Make sure
            moving platforms have clearance to push the player around
            or add code to handle what happens if they don't. """

        # Move left/right
        self.rect.x += self.x_change

        # See if we hit the player
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            # We did hit the player. Shove the player around and
            # assume he/she won't hit anything else.

            # If we are moving right, set our right side
            # to the left side of the item we hit
            if self.x_change < 0:
                self.player.rect.right = self.rect.left
            else:
                # Otherwise if we are moving left, do the opposite.
                self.player.rect.left = self.rect.right

        # Move up/down
        self.rect.y += self.y_change

        # Check and see if we the player
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            # We did hit the player. Shove the player around and
            # assume he/she won't hit anything else.

            # Reset our position based on the top/bottom of the object.
            if self.y_change < 0:
                self.player.rect.bottom = self.rect.top
            else:
                self.player.rect.top = self.rect.bottom

        # Check the boundaries and see if we need to reverse
        # direction.
        at_bottom = self.rect.bottom > self.boundary_bottom
        at_top = self.rect.top < self.boundary_top
        if at_bottom or at_top:
            self.y_change *= -1

        at_left = self.rect.x < self.boundary_left
        at_right = self.rect.x > self.boundary_right
        if at_left or at_right:
            self.x_change *= -1


class Cannon(Platform):

    WIDTH = 32
    HEIGHT = 32

    def __init__(self, init_orientation):
        super().__init__(Cannon.WIDTH, Cannon.HEIGHT)
        self.orientation = init_orientation
        self.firerate = 90
        self.fire_counter = 0

        self.image = pygame.image.load("cannon2.png").convert()
        self.image.set_colorkey(constants.MAGENTA)
        self.rect = self.image.get_rect()

        self.canon_sound = pygame.mixer.Sound("canon.ogg")

        self.game = None

    def update(self):
        self.fire_counter += 1
        if self.fire_counter >= self.firerate:
            self.shoot()
            self.fire_counter = 0

    def shoot(self):
        cannonball = Cannonball(self.rect.x, self.rect.y+4, self.orientation)
        self.game.projectile_list.add(cannonball)
        self.game.all_sprites_list.add(cannonball)
        self.canon_sound.play()
