import config
from config import BulletStats
from config import AlienStats
from copy import deepcopy


class SessionStats:
    """Track per-session statistics for Space Invaders."""

    def __init__(self):
        """Initialize statistics."""
        self.ship_speed = 450       # pixels per second
        self.alien_speed = 100
        self.bullets_per_second = config.bullets_per_second

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

        self.fleet_shots_per_second = config.fleet_shots_per_second
        self.fleet_max_shots_per_second = config.fleet_max_shots_per_second

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
        self.alien_speed *= config.speedup_scale

        # improve player bullet speed
        self.player_bullet = BulletStats(self.player_bullet.width,
                                         self.player_bullet.height,
                                         self.player_bullet.speed * config.speedup_scale,
                                         self.player_bullet.color)
        self.bullets_per_second *= config.speedup_scale

        # improve enemy bullet speed
        self.alien_bullet = BulletStats(self.alien_bullet.width,
                                        self.alien_bullet.height,
                                        self.alien_bullet.speed * config.speedup_scale,
                                        self.alien_bullet.color)

        # improve alien stats
        self.alien_stats = [AlienStats(
            sprite_name=alien.sprite_name,
            points=int(alien.points * config.score_scale)
        ) for alien in self.alien_stats]

        self.ufo_stats = AlienStats(self.ufo_stats.sprite_name, int(self.ufo_stats.points * config.score_scale))

        # improve fleet rate of fire
        self.fleet_shots_per_second *= config.speedup_scale
        self.fleet_max_shots_per_second *= config.speedup_scale
