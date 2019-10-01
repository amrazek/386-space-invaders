from abc import abstractmethod
import pygame
from pygame.sprite import Sprite, Group
import config


class Bullet(Sprite):
    """A class to manage bullets fired from the ship"""

    def __init__(self, stats, top_left_pos):
        """Create a bullet object at the ship's current position"""
        super().__init__()

        # Create a bullet rect at (0, 0) and then set correct position
        self.rect = pygame.Rect(0, 0, config.bullet_width,
                                config.bullet_height)
        self.rect.center = top_left_pos

        # Store the bullet's position as a decimal value
        self.y = float(self.rect.y)

        self.color = config.bullet_color
        self.speed_factor = stats.bullet_speed

        self.image = pygame.Surface((config.bullet_width, config.bullet_height))
        self.image.fill(color=self.color)

    def update(self, elapsed):
        """Move the bullet up the screen"""
        # Update the decimal position of the bullet
        self.y -= self.speed_factor * elapsed

        # Update the rect position
        self.rect.y = self.y


class BulletManager:
    def __init__(self):
        self._bullets = Group()

    @abstractmethod
    def create(self, spawner):
        pass

    def update(self, elapsed):
        self._bullets.update(elapsed)

        # Get rid of bullets that have disappeared
        for bullet in self._bullets.copy():
            if bullet.rect.bottom <= 0 or bullet.rect.top >= config.screen_height:
                self._bullets.remove(bullet)

    def clear(self):
        self._bullets.empty()

    def draw(self, screen):
        self._bullets.draw(screen)

    def sprites(self):
        return self._bullets.sprites()

    def __iter__(self):
        return self._bullets.__iter__()


class PlayerBulletManager(BulletManager):
    def __init__(self, stats):
        super().__init__()
        self.stats = stats

    def create(self, ship):
        location = (ship.rect.centerx, ship.rect.top)

        bullet = Bullet(self.stats, location)
        self._bullets.add(bullet)


class EnemyBulletManager(PlayerBulletManager):  # todo: implement enemy bullets
    pass
