import pygame
from pygame.sprite import Sprite
from entities.bullet import Bullet
import config


class Ship(Sprite):
    def __init__(self, stats, bullet_manager):
        """Initialize ship and set its starting position"""
        super().__init__()

        self.stats = stats
        self.bullet_manager = bullet_manager

        # load the ship image and get its rect
        self.animation = config.atlas.load_animation("ship")
        self.image = self.animation.image
        self.rect = self.image.get_rect()
        self.screen_rect = config.screen_rect

        # start each new ship at the bottom center of the screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # store a decimal for the ship's position
        self.center = float(self.rect.centerx)

        self.last_shot = 0
        self.min_time_between_shots = 1. / stats.bullets_per_second
        self.wait_time_to_shoot = 0.0

    def update(self, input_state, elapsed):
        # update ship's position, not its rect
        if input_state.left ^ input_state.right:
            if input_state.right and self.rect.right < self.screen_rect.right:
                self.center += self.stats.ship_speed * elapsed

            if input_state.left and self.rect.left > 0:
                self.center -= self.stats.ship_speed * elapsed

        # Update rect object from self.center.y
        self.rect.centerx = self.center

        # update ship animation
        self.animation.update(elapsed)
        self.image = self.animation.image

        # update passing time
        self.wait_time_to_shoot -= elapsed

    def center_ship(self):
        """Center the ship on the screen"""
        self.center = self.screen_rect.centerx

    def fire(self):
        if self.wait_time_to_shoot > 0.:
            return

        self.wait_time_to_shoot = self.min_time_between_shots

        bullet_anim = config.atlas.load_static("player_bullet")
        r = pygame.Rect(0, 0, bullet_anim.width, bullet_anim.height)
        r.top = self.rect.top
        r.centerx = self.rect.centerx

        bullet = Bullet(self.stats.player_bullet, r.center, bullet_anim)

        self.bullet_manager.add(bullet)
