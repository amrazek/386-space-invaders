import pygame
from pygame.sprite import Sprite, Group
from config import BulletStats
import config


def generate_alien_bullet(wh, color):
    surf = pygame.Surface(wh)
    surf.set_colorkey(config.transparent_color)

    num_vertical_zigzags = 5
    left_side = True
    previous_location = (0, 0)

    for y in range(0, surf.get_height(), surf.get_height() // num_vertical_zigzags):
        next_location = (0 if left_side else surf.get_width(), y)
        pygame.draw.aaline(surf, color, previous_location, next_location)
        previous_location = next_location
        left_side = not left_side

    return surf


class Bullet(Sprite):
    """A class to manage bullets fired from the ship"""

    def __init__(self, bullet_stats: BulletStats, top_left_pos):
        """Create a bullet object at the ship's current position"""
        super().__init__()

        # Create a bullet rect at (0, 0) and then set correct position
        self.rect = pygame.Rect(0, 0, bullet_stats.width, bullet_stats.height)
        self.rect.center = top_left_pos

        # Store the bullet's position as a decimal value
        self.y = float(self.rect.y)

        self.color = bullet_stats.color
        self.speed = bullet_stats.speed

        self.image = pygame.Surface(self.rect.size)
        self.image.fill(color=self.color)

        # temp
        self.image = generate_alien_bullet((bullet_stats.width, bullet_stats.height), bullet_stats.color)

    def update(self, elapsed):
        """Move the bullet up the screen"""
        # Update the decimal position of the bullet
        self.y -= self.speed * elapsed

        # Update the rect position
        self.rect.y = self.y


class BulletManager:
    def __init__(self, bullet_stats: BulletStats):
        self._bullets = Group()
        self._bullet_stats = bullet_stats

    def create(self, spawn_entity):
        # spawn the bullet at the center of the spawner, aligned such that it is just about
        # to leave the spawner's rect
        bullet_size = self._bullet_stats.size

        location = (spawn_entity.rect.centerx,
                    spawn_entity.rect.top if self._bullet_stats.speed > 0 else spawn_entity.rect.bottom - bullet_size[1])

        bullet = Bullet(self._bullet_stats, location)
        self._bullets.add(bullet)

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
