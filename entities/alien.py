from animated_sprite import AnimatedSprite
import sprite_atlas
import config


class Alien(AnimatedSprite):
    """A class to represent a single alien in the fleet"""

    def __init__(self, stats, alien_type):
        """Initialize the alien and set its starting position"""
        super().__init__(sprite_atlas.aliens[alien_type], sprite_atlas.alien_animation_rate)
        self.stats = stats

        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen
        self.rect.x, self.rect.y = self.rect.width, self.rect.height

        # store the alien's exact position
        self.x = float(self.rect.x)

    def update(self, elapsed):
        super().update(elapsed)

        """Move the alien right or left."""
        movement_amt = self.stats.alien_speed * self.stats.fleet_direction * elapsed

        self.x += movement_amt

        self.rect.x = self.x

    def check_edges(self):
        """Return true if alien is at edge of screen."""
        if self.rect.right >= config.screen_width and self.stats.fleet_direction > 0:
            return True
        elif self.rect.left <= 0 and self.stats.fleet_direction < 0:
            return True
