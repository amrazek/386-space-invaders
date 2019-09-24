import pygame
from pygame.sprite import Sprite
import config


class Ship(Sprite):
    def __init__(self, ai_settings):
        """Initialize ship and set its starting position"""
        super().__init__()

        self.ai_settings = ai_settings

        # load the ship image and get its rect
        self.image = pygame.image.load("images/ship.bmp")

        self.rect = self.image.get_rect()
        self.screen_rect = pygame.Rect(0, 0, config.screen_width, config.screen_height)

        # start each new ship at the bottom center of the screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # store a decimal for the ship's position
        self.center = float(self.rect.centerx)

        self.destroyed = False

    def update(self, input_state, elapsed):
        # update ship's position, not its rect
        if input_state.left ^ input_state.right:
            if input_state.right and self.rect.right < self.screen_rect.right:
                self.center += self.ai_settings.ship_speed * elapsed

            if input_state.left and self.rect.left > 0:
                self.center -= self.ai_settings.ship_speed * elapsed

        # Update rect object from self.center.y
        self.rect.centerx = self.center

    def center_ship(self):
        """Center the ship on the screen"""
        self.center = self.screen_rect.centerx

    def hit(self):
        self.destroyed = True