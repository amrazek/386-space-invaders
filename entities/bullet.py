from pygame.sprite import Sprite, Group
from config import BulletStats
import config


class Bullet(Sprite):
    """A class to manage bullets fired from the ship"""

    def __init__(self, bullet_stats: BulletStats, center_pos, animation):  # visual can be static or animation
        """Create a bullet object at the ship's current position"""
        super().__init__()

        # Create a bullet rect at (0, 0) and then set correct position
        self.animation = animation
        self.rect = animation.image.get_rect()
        self.rect.center = center_pos

        # Store the bullet's position as a decimal value
        self.y = float(self.rect.y)

        self.color = bullet_stats.color
        self.speed = bullet_stats.speed

        self.image = animation.image

    def update(self, elapsed):
        """Move the bullet up the screen"""
        # Update the decimal position of the bullet
        self.y -= self.speed * elapsed

        # Update the rect position
        self.rect.y = self.y

        # update animation (if any)
        self.animation.update(elapsed)
        self.image = self.animation.image


class BulletManager:
    def __init__(self, bullet_stats: BulletStats):
        self._bullets = Group()
        self._bullet_stats = bullet_stats

    def add(self, bullet):
        self._bullets.add(bullet)

    def update(self, elapsed):
        self._bullets.update(elapsed)

        # Get rid of bullets that have disappeared
        for bullet in self._bullets.copy():
            if bullet.rect.bottom <= 0 or bullet.rect.top >= config.screen_height:
                self._bullets.remove(bullet)

    def empty(self):
        self._bullets.empty()

    def draw(self, screen):
        self._bullets.draw(screen)

    def sprites(self):
        return self._bullets.sprites()

    def __iter__(self):
        return self._bullets.__iter__()
