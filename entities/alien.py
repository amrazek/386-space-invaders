from pygame.sprite import Sprite
import config


class Alien(Sprite):
    """A class to represent a single alien in the fleet"""

    def __init__(self, stats, animation):
        super().__init__()

        """Initialize the alien and set its starting position"""
        self.animation = animation
        self.stats = stats

        # store the alien's exact position
        self.position = 0.0

        self.image = animation.current
        self.rect = self.image.get_rect()

    def update(self, elapsed):
        """Move the alien right or left."""
        movement_amt = self.stats.alien_speed * self.stats.fleet_direction * elapsed

        self.position += movement_amt

        self.rect.x = self.position

        """Update alien animation"""
        self.animation.update(elapsed)
        self.image = self.animation.current

    def check_edges(self):
        """Return true if alien is at edge of screen."""
        if self.rect.right >= config.screen_width and self.stats.fleet_direction > 0:
            return True
        elif self.rect.left <= 0 and self.stats.fleet_direction < 0:
            return True
