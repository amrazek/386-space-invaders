import pygame
from pygame.sprite import Group
from alien import Alien
import config


class AlienFleet:
    def __init__(self, ai_settings, ship):
        self.ai_settings = ai_settings
        self.ship = ship
        self.aliens = Group()
        self.__create_new_fleet()

    def update(self, elapsed):
        # Check if the fleet is at an edge, and then update the positions of all aliens in the fleet
        self.__check_fleet_edges()
        self.aliens.update(elapsed)

        # Look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self.ship.hit()

        # Look for aliens hitting the bottom of the screen
        self.__check_aliens_bottom()

    def draw(self, screen):
        self.aliens.draw(screen)

    def __create_new_fleet(self):
        """Create a full fleet of aliens"""
        # Create an alien and find the number of aliens in a row.
        alien = Alien(self.ai_settings)
        number_aliens_x = self.__get_number_aliens_x(alien.rect.width)
        number_rows = self.__get_number_rows(alien.rect.height)

        self.aliens.empty()

        # Create the first row of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self.__create_alien(alien_number, row_number)

    def __check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self.change_fleet_direction()
                break

    def change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.ai_settings.fleet_drop_speed
        self.ai_settings.fleet_direction *= -1

    @staticmethod
    def __get_number_aliens_x(alien_width):
        """Determine the number of aliens that fit in a row"""
        available_space_x = config.screen_width - 2 * alien_width
        number_aliens_x = int(available_space_x / alien_width)

        return number_aliens_x

    def __get_number_rows(self, alien_height):
        """Determine the number of rows of aliens that fit on the screen"""
        available_space_y = (config.screen_height - alien_height - 2 * self.ship.rect.height)
        number_rows = int(available_space_y / alien_height)

        return number_rows

    def __create_alien(self, alien_number, row_number):
        """Create an alien and place it in the row"""
        alien = Alien(self.ai_settings)

        alien_width = alien.rect.width
        alien.x = alien_width + alien_width * alien_number

        alien.rect.y = alien.rect.height + alien.rect.height * row_number
        alien.rect.x = alien.x

        self.aliens.add(alien)

    def __check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= config.screen_height:
                # Treat this the same as if the ship got hit
                self.ship.hit()
                break
