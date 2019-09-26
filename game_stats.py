class GameStats:
    """Track statistics for Space Invaders."""

    def __init__(self, ai_settings, scoreboard):
        """Initialize statistics."""
        self.ai_settings = ai_settings
        self.scoreboard = scoreboard

        # Start Alien Invasion in an inactive state
        self.game_active = False

        # init values to make PEP8 happy
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1

        # init scoreboard
        self.set_score(self.score)
        self.set_level(self.level)
        self.set_ships_left(self.ships_left)

    def set_level(self, level):
        self.level = level
        self.scoreboard.set_level(level)

    def set_ships_left(self, ships_left):
        self.ships_left = ships_left
        self.scoreboard.set_ships(ships_left)

    def set_score(self, score):
        self.score = score
        self.scoreboard.set_score(score)

    @property
    def player_alive(self):
        return self.ships_left > 0

    def decrease_lives(self):
        self.set_ships_left(self.ships_left - 1)

    def increase_score(self, amt):
        self.set_score(self.score + amt)

    def increase_level(self):
        self.set_level(self.level + 1)
        self.ai_settings.increase_speed()