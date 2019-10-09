import random
import copy
import pygame
from pygame.sprite import Group
from entities.alien import Alien
from entities.ufo import Ufo
from entities.bullet import Bullet
from animation import OneShotAnimation
import config
import sounds


class AlienFleet:
    def __init__(self, session_stats, ship, player_bullets, alien_bullets,
                 on_clear_callback, on_kill_callback, on_player_collision_callback):
        self.session_stats = session_stats
        self.ship = ship
        self.player_bullets = player_bullets
        self.alien_bullets = alien_bullets
        self.on_clear = on_clear_callback
        self.on_kill = on_kill_callback
        self.on_player_collision = on_player_collision_callback

        self.aliens = Group()
        self.ufos = Group()

        self.explosions = Group()
        self.create_new_fleet()

        self.max_aliens = len(self.aliens)
        self.next_ufo_appearance = random.uniform(config.ufo_min_delay, config.ufo_max_delay)

        self.next_shot_timer = 1. / session_stats.fleet_shots_per_second

        self.font = pygame.font.SysFont(None, 24)

        # if this is the first level, hard-code the appearance of a UFO so it's clear that requirement was met
        if self.session_stats.level == 0:
            self.next_ufo_appearance = 5.0

    def update(self, elapsed):
        # Check if the fleet is at an edge, and then update the positions of all aliens in the fleet
        self._check_fleet_edges()
        self._check_ufo_offscreen()
        self.aliens.update(elapsed)
        self.ufos.update(elapsed)
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

        # spawn new ufo, if needed
        self.next_ufo_appearance -= elapsed
        if self.next_ufo_appearance < 0:
            self._spawn_ufo()

        # is it time to fire another bullet?
        self.next_shot_timer -= elapsed
        self._update_shooting()

    def draw(self, screen):
        self.aliens.draw(screen)
        self.ufos.draw(screen)
        self.explosions.draw(screen)

    def create_new_fleet(self):
        """Create a full fleet of aliens"""
        # Create an alien and find the number of aliens in a row.
        alien = Alien(self.session_stats, config.atlas.load_animation(self.session_stats.alien_stats[0].sprite_name))

        number_aliens_x = self._get_number_aliens_x(alien.rect.width)
        number_rows = self._get_number_rows(alien.rect.height)

        self.aliens.empty()
        self.ufos.empty()
        self.explosions.empty()
        self.alien_bullets.empty()

        sounds.silence()

        # Create the first row of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self.change_fleet_direction()
                break

    def change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += config.fleet_drop_speed
        self.session_stats.fleet_direction *= -1

    @staticmethod
    def _get_number_aliens_x(alien_width):
        """Determine the number of aliens that fit in a row"""
        available_space_x = config.screen_width - 2 * alien_width
        number_aliens_x = int(available_space_x / alien_width)

        return number_aliens_x

    def _get_number_rows(self, alien_height):
        """Determine the number of rows of aliens that fit on the screen"""
        available_space_y = (config.screen_height - alien_height - 8 * self.ship.rect.height)
        number_rows = int(available_space_y / alien_height)

        return number_rows

    def _create_alien(self, alien_number, row_number):
        """Create an alien and place it in the row"""
        num_types = len(config.alien_stats)
        alien_stats = self.session_stats.alien_stats[alien_number % num_types]

        alien = Alien(self.session_stats, config.atlas.load_animation(alien_stats.sprite_name))

        alien_width = alien.rect.width
        alien.rect.x = alien_width + alien_width * alien_number
        alien.rect.y = alien.rect.height * 2 + alien.rect.height * row_number
        alien.position = alien.rect.x
        alien.alien_stats = alien_stats

        self.aliens.add(alien)

    def _create_alien_explosion(self, alien, as_points=False):
        """Create an alien explosion located where this alien is"""
        if not as_points:
            explosion_animation = config.atlas.load_animation(alien.alien_stats.sprite_name + "_explosion")
            explosion = OneShotAnimation.from_animation(explosion_animation)
        else:
            score_str = "{:,}".format(alien.alien_stats.points)
            surf = self.font.render(score_str, True, config.green_color)
            explosion = OneShotAnimation(surf, 0.5)

        # a little closure to automatically remove explosion when it's done running
        def die_on_finish():
            self.explosions.remove(explosion)

        explosion.on_complete = die_on_finish
        explosion.rect.center = alien.rect.center

        self.explosions.add(explosion)
        sounds.play("explosion1.wav")

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

        # remove any bullets and UFOs that have collided
        collisions = pygame.sprite.groupcollide(bullets, self.ufos, True, True)

        if collisions:
            for ufos in collisions.values():
                for ufo in ufos:
                    self._create_alien_explosion(ufo, True)
                    self.on_kill(ufo)

        if len(self.aliens) == 0 and len(self.ufos) == 0:
            # If the entire fleet is destroyed, start a new level
            self.on_clear()
            self.create_new_fleet()

    def _check_ufo_offscreen(self):
        ufos = copy.copy(self.ufos.sprites())

        for ufo in ufos:
            # if ufo has moved off-screen, delete it without explosion or points
            if ufo.speed < 0.0 and ufo.rect.right < 0:
                self.ufos.remove(ufo)
            elif ufo.speed > 0.0 and ufo.rect.left > config.screen_width:
                self.ufos.remove(ufo)

        if len(self.ufos) == 0:
            sounds.fade_out("ufo", 250)

    def _fire_alien_bullet(self, alien):
        self.bullet_elapsed = 0.0

        # create new animation for this bullet
        bullet_anim = config.atlas.load_animation("alien_bullet")

        # calculate bullet center position
        # it should align with the BOTTOM of the alien
        r = pygame.Rect(0, 0, bullet_anim.width, bullet_anim.height)
        r.bottom = alien.rect.bottom
        r.centerx = alien.rect.centerx

        bullet = Bullet(self.session_stats.alien_bullet, r.center, bullet_anim)

        self.alien_bullets.add(bullet)
        sounds.play("laser2")

    def _spawn_ufo(self):
        self.next_ufo_appearance = random.uniform(config.ufo_min_delay, config.ufo_max_delay)

        ufo = Ufo(self.session_stats, config.atlas.load_animation("ufo"))

        rounded_score = int(round(random.randrange(self.session_stats.ufo_stats.points), -1))
        ufo.alien_stats = config.AlienStats("ufo", rounded_score)

        self.ufos.add(ufo)
        if not sounds.is_playing("ufo"):
            sounds.fade_in("ufo", 250, True)

    def _update_shooting(self):

        if self.next_shot_timer < 0.:
            num_aliens_alive = len(self.aliens)

            if num_aliens_alive == 0:
                return

            # calculate how long till next shot
            delta = self.session_stats.fleet_max_shots_per_second - self.session_stats.fleet_shots_per_second
            alive_ratio = num_aliens_alive / self.max_aliens
            shots_per_second = (1. - alive_ratio) * delta + self.session_stats.fleet_shots_per_second

            self.next_shot_timer = 1. / shots_per_second

            # select an alien to fire this bullet
            alien = random.choice(self.aliens.sprites())
            self._fire_alien_bullet(alien)

    @property
    def alive_ratio(self):
        return len(self.aliens) / self.max_aliens
