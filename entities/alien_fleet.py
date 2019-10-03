import pygame
from pygame.sprite import Group
from entities.alien import Alien
import sprite_atlas
import config


class AlienFleet:
    def __init__(self, stats, ship, alien_bullets, on_clear_callback, on_kill_callback):
        self.stats = stats
        self.ship = ship
        self.alien_bullets = alien_bullets
        self.on_clear = on_clear_callback
        self.on_kill = on_kill_callback
        self.aliens = Group()
        self.create_new_fleet()

        # temp
        self.bullet_elapsed = 0.0

    def update(self, elapsed, player_bullets, alien_bullets):
        # Check if the fleet is at an edge, and then update the positions of all aliens in the fleet
        self.__check_fleet_edges()
        self.aliens.update(elapsed)

        # Look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self.ship.hit()

        # Look for aliens hitting the bottom of the screen
        self.__check_aliens_bottom()

        # Look for player bullet->alien collisions
        self.__check_bullet_alien_collisions(player_bullets)

        # todo: fix case where aliens spawn outside screen
        for alien in self.aliens:
            if alien.rect.right > config.screen_width:
                print("warning: alien spawned outside screen at {}".format(alien.rect.right))
                break

        # *** temp  ***
        self.bullet_elapsed += elapsed

        if self.bullet_elapsed > 1.0:
            self.bullet_elapsed -= 1.0
            # temp: create bullet from every alien
            for alien in self.aliens:
                alien_bullets.create(alien)

    def draw(self, screen):
        self.aliens.draw(screen)

    def create_new_fleet(self):
        """Create a full fleet of aliens"""
        # Create an alien and find the number of aliens in a row.
        alien = Alien(self.stats, 0)
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
            alien.rect.y += config.fleet_drop_speed
        self.stats.fleet_direction *= -1

    @staticmethod
    def __get_number_aliens_x(alien_width):
        """Determine the number of aliens that fit in a row"""
        available_space_x = config.screen_width - 2 * alien_width
        number_aliens_x = int(available_space_x / alien_width)

        return number_aliens_x

    def __get_number_rows(self, alien_height):
        """Determine the number of rows of aliens that fit on the screen"""
        available_space_y = (config.screen_height - alien_height - 4 * self.ship.rect.height)
        number_rows = int(available_space_y / alien_height)

        return number_rows

    def __create_alien(self, alien_number, row_number):
        """Create an alien and place it in the row"""
        num_types = len(sprite_atlas.aliens)
        alien = Alien(self.stats, alien_number % num_types)

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

    def __check_bullet_alien_collisions(self, bullets):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided
        collisions = pygame.sprite.groupcollide(bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                for an_alien in aliens:
                    self.on_kill(an_alien)

        if len(self.aliens) == 0:
            # If the entire fleet is destroyed, start a new level
            self.on_clear()
            self.create_new_fleet()
