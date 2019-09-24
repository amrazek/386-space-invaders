class Settings:
    """A class to store all settings for the game"""

    def __init__(self):
        """Initialize the game's settings"""

        # ship settings
        self.ship_limit = 3

        # bullet settings
        self.bullet_width = 3000
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 3

        # Alien settings
        self.fleet_drop_speed = 30

        # How quickly the game speeds up
        self.speedup_scale = 1.1

        # How quickly alien point values increase
        self.score_scale = 1.5

        """Initialize settings that change throughout the game"""
        self.ship_speed = 450       # pixels per second
        self.bullet_speed = 600
        self.alien_speed = 100
        self.bullets_per_second = 5

        # fleet_direction of 1 represents right; -1 represents left
        self.fleet_direction = 1

        # Scoring
        self.alien_points = 50

    def increase_speed(self):
        """Increase speed settings."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.bullets_per_second *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
