import pygame.font
from pygame.sprite import Group
from entities.ship import Ship
import config


class Scoreboard:
    """A class to report scoring information"""

    def __init__(self, ai_settings):
        """Initialize score-keeping attributes."""

        self.ai_settings = ai_settings

        # Font settings for scoring information
        self.text_color = (230, 230, 230)
        self.font = pygame.font.SysFont(None, 48)

        # initialize variables to make PEP happy
        self.score_image = self.score_rect = None
        self.high_score_image = self.high_score_rect = None
        self.level_image = self.level_rect = None
        self.ships = None

        # Prepare the initial score image
        self.set_score(0)
        self.set_level(0)
        self.set_ships(0)

    def set_score(self, score):
        """ Turn the score into a rendered image."""
        rounded_score = int(round(score, -1))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color)

        # Display the score at the top left of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.left = config.screen_rect.left + 20
        self.score_rect.top = 20

    def set_level(self, level):
        """Turn the level into a rendered image."""
        self.level_image = self.font.render(str(level), True, self.text_color)

        # Position the level below the score
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def set_ships(self, ships_left):
        """Show how many ships are left."""
        self.ships = Group()
        for ship_number in range(ships_left):
            ship = Ship(self.ai_settings)
            ship.rect.x = config.screen_width - (ship_number + 1) * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def draw(self, screen):
        """Draw the scores and ships to the screen."""
        screen.blit(self.score_image, self.score_rect)
        screen.blit(self.level_image, self.level_rect)

        # Draw ships
        self.ships.draw(screen)
