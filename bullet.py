import pygame
from pygame.sprite import Sprite, Group
import config


class Bullet(Sprite):
    """A class to manage bullets fired from the ship"""

    def __init__(self, ai_settings, ship):
        """Create a bullet object at the ship's current position"""
        super().__init__()

        # Create a bullet rect at (0, 0) and then set correct position
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width,
                                ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # Store the bullet's position as a decimal value
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed

        self.image = pygame.Surface((ai_settings.bullet_width, ai_settings.bullet_height))
        self.image.fill(color=self.color)

    def update(self, elapsed):
        """Move the bullet up the screen"""
        # Update the decimal position of the bullet
        self.y -= self.speed_factor * elapsed

        # Update the rect position
        self.rect.y = self.y


class AlienBullet(Bullet):
    def __init__(self, ai_settings, ship):
        super().__init__(ai_settings, ship)


class BulletManager:
    def __init__(self):
        self._bullets = Group()

    def add(self, new_bullet):
        self._bullets.add(new_bullet)

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