import pygame
from pygame.sprite import Sprite
import game_functions as gf


class Alien(Sprite):
    """A class to represent a single alien in the fleet"""

    def __init__(self, ai_settings, screen):
        """Initialize the alien and set its starting position"""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the alien image and set its rect attribute
        self.image = pygame.image.load('images/alien.bmp')
        gf.set_color_key_from_pixel(self.image, (0, 0))

        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen
        self.rect.x, self.rect.y = self.rect.width, self.rect.height

        # store the alien's exact position
        self.x = float(self.rect.x)

    def draw_me(self):
        """Draw the alien at its current location"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """Move the alien right or left."""
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        """Return true if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
