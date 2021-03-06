import pygame
import constants


class Projectile(pygame.sprite.Sprite):

    def __init__(self, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.rect = self.image.get_rect()
        self.x_change = 0
        self.y_change = 0

    def update(self):
        self.rect.x += self.x_change
        self.rect.y += self.y_change

        at_right = self.rect.x > constants.SCREEN_WIDTH
        at_left = self.rect.x < -self.rect.width
        at_bottom = self.rect.y > constants.SCREEN_HEIGHT
        at_top = self.rect.y < self.rect.height
        if at_right or at_left or at_bottom or at_top:
            self.kill()


class Bullet(Projectile):

    WIDTH = 4
    HEIGTH = 4
    SPEED = 10

    def __init__(self, direction):
        super().__init__(Bullet.WIDTH, Bullet.HEIGTH)
        self.x_change = direction * Bullet.SPEED
        self.image.fill(constants.BLACK)


class Cannonball(Projectile):

    WIDTH = 24
    HEIGHT = 24
    SPEED = 4

    def __init__(self, x_val, y_val, orientation):
        super().__init__(Cannonball.WIDTH, Cannonball.HEIGHT)
        self.rect.x = x_val
        self.rect.y = y_val

        if orientation == "left":
            self.x_change = -Cannonball.SPEED
        elif orientation == "right":
            self.x_change = Cannonball.SPEED
        elif orientation == "down":
            self.x_change = Cannonball.SPEED
        elif orientation == "up":
            self.x_change = -Cannonball.SPEED

        self.image = pygame.image.load("cannonball.png").convert()
        self.image.set_colorkey(constants.MAGENTA)


class TrippedProjectile(Projectile):

    WIDTH = 16
    HEIGHT = 16
    SPEED = 15

    def __init__(self):
        super().__init__(TrippedProjectile.WIDTH, TrippedProjectile.HEIGHT)
        self.image.fill(constants.RED)

        self.moving = False

        self.player = None

    def update(self):
        super().update()
        trip_verticle1 = self.player.rect.right >= self.rect.x
        trip_verticle2 = self.player.rect.x <= self.rect.right
        if trip_verticle1 and trip_verticle2 and not self.moving:
            self.moving = True
            if self.player.rect.y > self.rect.y:
                self.y_change = TrippedProjectile.SPEED
            else:
                self.y_change = -TrippedProjectile.SPEED

        trip_horizontal1 = self.player.rect.bottom >= self.rect.y
        trip_horizontal2 = self.player.rect.y <= self.rect.bottom
        if trip_horizontal1 and trip_horizontal2 and not self.moving:
            self.moving = True
            if self.player.rect.x > self.rect.x:
                self.x_change = TrippedProjectile.SPEED
            else:
                self.x_change = -TrippedProjectile.SPEED
