import config
from copy import deepcopy


class SessionStats:
    """Track per-session statistics for Space Invaders."""

    def __init__(self):
        """Initialize statistics."""
        self.ship_speed = 450       # pixels per second
        self.alien_speed = 100
        self.bullets_per_second = 5

        # fleet_direction of 1 represents right; -1 represents left
        self.fleet_direction = 1

        # Scoring
        self.alien_stats = deepcopy(config.alien_stats)
        self.ufo_stats = deepcopy(config.ufo_stats)

        # initial values
        self.level, self.score = 0, 0
        self.ships_left = config.ship_limit

        self.player_bullet = deepcopy(config.default_player_bullet)
        self.alien_bullet = deepcopy(config.default_alien_bullet)

    def set_level(self, level):
        self.level = level

    def set_ships_left(self, ships_left):
        self.ships_left = ships_left

    def set_score(self, score):
        self.score = score

    @property
    def player_alive(self):
        return self.ships_left >= 0

    def decrease_lives(self):
        self.set_ships_left(self.ships_left - 1)

    def increase_score(self, amt):
        self.set_score(self.score + amt)

    def increase_level(self):
        self.set_level(self.level + 1)
        self.__increase_speed()

    def __increase_speed(self):
        """Increase speed settings."""
        self.ship_speed *= config.speedup_scale
        self.player_bullet.speed *= config.speedup_scale
        self.alien_bullet.speed *= config.speedup_scale
        self.bullets_per_second *= config.speedup_scale
        self.alien_speed *= config.speedup_scale

        for stats in self.alien_stats:
            stats.points = int(stats.points * config.score_scale)

        self.ufo_stats.points = int(self.ufo_stats.points * config.score_scale)

        # todo: increase alien bullet speed, drop rate, etc?
