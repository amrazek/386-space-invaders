import pygame.font
from pygame.sprite import Group
from entities.ship import Ship
import config


class Scoreboard:
    """A class to report scoring information"""

    def __init__(self, stats):
        """Initialize score-keeping attributes."""

        self.stats = stats

        # Font settings for scoring information
        self.text_color = (230, 230, 230)
        self.font = pygame.font.SysFont(None, 48)

        # initialize variables to make PEP happy
        self.score_image = self.score_rect = None
        self.high_score_image = self.high_score_rect = None
        self.level_image = self.level_rect = None
        self.ships = None

        self._dirty = True

    def __refresh_score(self):
        """ Turn the score into a rendered image."""
        rounded_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color)

        # Display the score at the top left of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.left = config.screen_rect.left + 20
        self.score_rect.top = 20

    def __refresh_level(self):
        """Turn the level into a rendered image."""
        self.level_image = self.font.render(str(self.stats.level), True, self.text_color)

        # Position the level below the score
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def __refresh_ships(self):
        """Show how many ships are left."""
        self.ships = Group()

        temp = []

        for ship_number in range(self.stats.ships_left):
            ship = config.atlas.load_static("ship_no_engines")
            ship.rect.x = config.screen_width - (ship_number + 1) * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)
            temp.append(ship)

    def set_dirty(self):
        self._dirty = True

    def draw(self, screen):
        if self._dirty:
            self.__refresh_score()
            self.__refresh_level()
            self.__refresh_ships()

            self._dirty = False

        """Draw the scores and ships to the screen."""
        screen.blit(self.score_image, self.score_rect)
        screen.blit(self.level_image, self.level_rect)

        # Draw ships
        self.ships.draw(screen)
