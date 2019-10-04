from states.game_state import GameState
from states.game_over import GameOver
from entities.scoreboard import Scoreboard
from entities.bullet import BulletManager
from session_stats import SessionStats
from entities.alien_fleet import AlienFleet
from entities.ship import Ship
from entities.bunker import Bunker
import config


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

        self.game_over = GameOver(input_state, self)

    def update(self, elapsed):
        self.ship.update(self.input_state, elapsed)
        self.fleet.update(elapsed)

        self.player_bullets.update(elapsed)
        self.alien_bullets.update(elapsed)

        for bunker in self.bunkers:
            bunker.update(elapsed)

        if self.input_state.fire:
            self.ship.fire()

    def draw(self, screen):
        screen.fill(color=(0, 0, 50))
        screen.blit(self.ship.image, self.ship.rect)

        self.player_bullets.draw(screen)
        self.alien_bullets.draw(screen)

        for bunker in self.bunkers:
            bunker.draw(screen)

        self.fleet.draw(screen)
        self.scoreboard.draw(screen)

    @property
    def finished(self):
        return self.stats.ships_left == 0

    def get_next(self):
        return self.game_over

    def _player_destroyed(self):
        if self.stats.player_alive:
            print("Player was destroyed")

            # Reduce player lives
            self.stats.decrease_lives()

            # create a new fleet
            self.fleet.create_new_fleet()

            # reset player position and state
            self.ship.center_ship()

        else:  # no ships left
            pass  # done TODO: prepare transition to next state

        self.scoreboard.set_dirty()

    def _on_alien_killed(self, alien):
        self.stats.increase_score(self.stats.alien_points)
        self.scoreboard.set_dirty()

    def _on_fleet_destroyed(self):
        # advance to next level
        self.stats.increase_level()

        # clear all bullets
        self.player_bullets.clear()
        self.alien_bullets.clear()

        # reset scoreboard
        self.scoreboard.set_dirty()
