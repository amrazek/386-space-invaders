import pygame
from .game_state import GameState
from .player_death import PlayerDeath
from entities.scoreboard import Scoreboard
from entities.bullet import BulletManager
from session_stats import SessionStats
from alien_fleet import AlienFleet
from entities.ship import Ship
from entities.bunker import Bunker
import config
import sounds


class RunGame(GameState):
    """Manages actual game play, until the player loses."""
    def __init__(self, input_state):
        super().__init__(input_state)

        self.stats = SessionStats()

        self.player_bullets = BulletManager(self.stats.player_bullet)
        self.alien_bullets = BulletManager(self.stats.alien_bullet)

        self.ship = Ship(self.stats, self.player_bullets)

        self.scoreboard = Scoreboard(self.stats)
        self.fleet = AlienFleet(self.stats, self.ship, self.player_bullets, self.alien_bullets,
                                on_clear_callback=self._on_fleet_destroyed,
                                on_kill_callback=self._on_alien_killed,
                                on_player_collision_callback=self._player_destroyed)

        self.bunkers = Bunker.create_bunkers(config.bunker_count, self.ship, self.player_bullets, self.alien_bullets)
        self.next_state = None

        self.bg_music = sounds.bg_music_names[0]

    def update(self, elapsed):
        self.ship.update(self.input_state, elapsed)
        self.fleet.update(elapsed)

        self.player_bullets.update(elapsed)
        self.alien_bullets.update(elapsed)

        for bunker in self.bunkers:
            bunker.update(elapsed)

        if self.input_state.fire:
            self.ship.fire()

    def draw(self, screen, draw_ship=True):
        screen.fill(color=config.bg_color)

        if draw_ship:
            screen.blit(self.ship.image, self.ship.rect)

        self.player_bullets.draw(screen)
        self.alien_bullets.draw(screen)

        for bunker in self.bunkers:
            bunker.draw(screen)

        self.fleet.draw(screen)
        self.scoreboard.draw(screen)

    @property
    def finished(self):
        return self.get_next() is not None

    def get_next(self):
        return self.next_state

    def start(self):
        sounds.play_music(self.bg_music)

    def _player_destroyed(self):
        self.next_state = self.next_state or PlayerDeath(self.input_state, self)

    def _on_alien_killed(self, alien):
        self.stats.increase_score(alien.alien_stats.points)
        self.scoreboard.set_dirty()

        # update music
        next_music = self.bg_music
        num_variations = len(sounds.bg_music_names)

        # 0 - 0.33 -> 2
        # 0.33 -> 0.66 -> 1
        # 0.66 -> 1 = 0

        for i in range(num_variations):
            # 2 1 0
            if self.fleet.alive_ratio < 1. / (i + 1):
                next_music = sounds.bg_music_names[i]

        if next_music != self.bg_music:
            # change music track
            sounds.play_music(next_music)
            print("now playing ", next_music, " because fleet ratio is ", self.fleet.alive_ratio)
            self.bg_music = next_music

            if self.fleet.alive_ratio < 0.33:
                pygame.mixer_music.set_volume(1.0)  # play music loudly for almost-dead fleet

    def _on_fleet_destroyed(self):
        # advance to next level
        self.stats.increase_level()

        # clear all bullets
        self.player_bullets.empty()
        self.alien_bullets.empty()

        # reset scoreboard
        self.scoreboard.set_dirty()
