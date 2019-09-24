class GameStats:
    """Track statistics for Space Invaders."""

    def __init__(self, ai_settings):
        """Initialize statistics."""
        self.ai_settings = ai_settings

        # initialize values in init to keep PEP8 happy
        self.ships_left = self.score = self.level = 0

        self.reset_stats()

        # Start Alien Invasion in an inactive state
        self.game_active = False

        # High score should never be reset
        self.high_score = 0

    def reset_stats(self):
        """Initialize statistics that can change during the game"""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
