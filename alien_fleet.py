import pygame
from pygame.sprite import Group
from entities.alien import Alien
from entities.bullet import Bullet
from animation import OneShotAnimation
import config


class AlienFleet:
    def __init__(self, stats, ship, player_bullets, alien_bullets,
                 on_clear_callback, on_kill_callback, on_player_collision_callback):
        self.stats = stats
        self.ship = ship
        self.player_bullets = player_bullets
        self.alien_bullets = alien_bullets
        self.on_clear = on_clear_callback
        self.on_kill = on_kill_callback
        self.on_player_collision = on_player_collision_callback

        self.aliens = Group()

        self.explosions = Group()
        self.create_new_fleet()

        # temp
        self.bullet_elapsed = 999.0

    def update(self, elapsed):
        # Check if the fleet is at an edge, and then update the positions of all aliens in the fleet
        self.__check_fleet_edges()
        self.aliens.update(elapsed)
        self.explosions.update(elapsed)

        # Look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self.on_player_collision()

        # Look for aliens hitting the bottom of the screen
        self._check_aliens_bottom()

        # Look for player bullet->alien collisions
        self._check_bullet_alien_collisions(self.player_bullets)

        # Look for alien bullet->ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.alien_bullets):
            self.on_player_collision()

        # todo: fix case where aliens spawn outside screen
        for alien in self.aliens:
            if alien.rect.right > config.screen_width:
                print("warning: alien spawned outside screen at {}".format(alien.rect.right))
                break

        # *** temp  ***
        self.bullet_elapsed += elapsed

        # if self.bullet_elapsed > 1.0:
        #     self._fire_alien_bullet(None)

    def draw(self, screen):
        self.aliens.draw(screen)
        self.explosions.draw(screen)

    def create_new_fleet(self):
        """Create a full fleet of aliens"""
        # Create an alien and find the number of aliens in a row.
        alien = Alien(self.stats, config.atlas.load_animation(self.stats.alien_stats[0].sprite_name))

        number_aliens_x = self._get_number_aliens_x(alien.rect.width)
        number_rows = self._get_number_rows(alien.rect.height)

        self.aliens.empty()
        self.explosions.empty()
        self.alien_bullets.empty()

        # Create the first row of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

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
    def _get_number_aliens_x(alien_width):
        """Determine the number of aliens that fit in a row"""
        available_space_x = config.screen_width - 2 * alien_width
        number_aliens_x = int(available_space_x / alien_width)

        return number_aliens_x

    def _get_number_rows(self, alien_height):
        """Determine the number of rows of aliens that fit on the screen"""
        available_space_y = (config.screen_height - alien_height - 4 * self.ship.rect.height)
        number_rows = int(available_space_y / alien_height)

        return number_rows

    def _create_alien(self, alien_number, row_number):
        """Create an alien and place it in the row"""
        num_types = len(config.alien_stats)
        alien_stats = self.stats.alien_stats[alien_number % num_types]

        alien = Alien(self.stats, config.atlas.load_animation(alien_stats.sprite_name))

        alien_width = alien.rect.width
        alien.rect.x = alien_width + alien_width * alien_number
        alien.rect.y = alien.rect.height + alien.rect.height * row_number
        alien.position = alien.rect.x
        alien.alien_stats = alien_stats

        self.aliens.add(alien)

    def _create_alien_explosion(self, alien):
        """Create an alien explosion located where this alien is"""
        explosion_animation = config.atlas.load_animation(alien.alien_stats.sprite_name + "_explosion")
        explosion = OneShotAnimation.from_animation(explosion_animation)

        # a little closure to automatically remove explosion when it's done running
        def die_on_finish():
            self.explosions.remove(explosion)

        explosion.on_complete = die_on_finish
        explosion.rect.center = alien.rect.center

        self.explosions.add(explosion)

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= config.screen_height:
                # Treat this the same as if the ship got hit
                self.on_player_collision()
                break

    def _check_bullet_alien_collisions(self, bullets):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided
        collisions = pygame.sprite.groupcollide(bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                for an_alien in aliens:
                    self._create_alien_explosion(an_alien)
                    self.on_kill(an_alien)

        if len(self.aliens) == 0:
            # If the entire fleet is destroyed, start a new level
            self.on_clear()
            self.create_new_fleet()

    def _fire_alien_bullet(self, alien):
        self.bullet_elapsed = 0.0

        # *** temp  ***

        # temp: create bullet from every alien
        for alien in self.aliens:
            # create new animation for this bullet
            bullet_anim = config.atlas.load_animation("alien_bullet")

            # calculate bullet center position
            # it should align with the BOTTOM of the alien
            r = pygame.Rect(0, 0, bullet_anim.width, bullet_anim.height)
            r.bottom = alien.rect.bottom
            r.centerx = alien.rect.centerx

            bullet = Bullet(self.stats.alien_bullet, r.center, bullet_anim)

            self.alien_bullets.add(bullet)
