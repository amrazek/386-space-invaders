from animated_sprite import AnimatedSprite
import sprite_atlas
import config


class Alien(AnimatedSprite):
    """A class to represent a single alien in the fleet"""

    def __init__(self, ai_settings):
        """Initialize the alien and set its starting position"""
        super().__init__(sprite_atlas.alien, sprite_atlas.alien_animation_rate)
        self.ai_settings = ai_settings

        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen
        self.rect.x, self.rect.y = self.rect.width, self.rect.height

        # store the alien's exact position
        self.x = float(self.rect.x)

    def update(self, elapsed):
        super().update()

        """Move the alien right or left."""
        self.x += (self.ai_settings.alien_speed * self.ai_settings.fleet_direction * elapsed)
        self.rect.x = self.x

    def check_edges(self):
        """Return true if alien is at edge of screen."""
        if self.rect.right >= config.screen_width:
            return True
        elif self.rect.left <= 0:
            return True
