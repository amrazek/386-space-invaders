from states.game_state import GameState
from states.game_over import GameOver
from settings import Settings
from entities.scoreboard import Scoreboard
from entities.bullet import BulletManager
from game_stats import GameStats
from entities.alien_fleet import AlienFleet
from entities.ship import Ship


class RunGame(GameState):
    """Manages actual game play, until the player loses."""
    def __init__(self, input_state):
        super().__init__(input_state)
        self.ai_settings = Settings()
        self.ship = Ship(self.ai_settings)

        self.fleet = AlienFleet(self.ai_settings, self.ship,
                                on_clear_callback=self.__on_fleet_destroyed,
                                on_kill_callback=self.__on_alien_killed)

        self.scoreboard = Scoreboard(self.ai_settings)
        self.stats = GameStats(self.ai_settings, self.scoreboard)

        self.bullets = BulletManager()
        self.game_over = GameOver(input_state, self)

    def update(self, elapsed):
        self.ship.update(self.input_state, elapsed)
        self.fleet.update(elapsed, self.bullets)
        self.bullets.update(elapsed)

        if self.ship.destroyed:
            self.__player_destroyed()

        if self.input_state.fire:
            self.ship.fire(self.bullets)

    def draw(self, screen):
        screen.fill(color=(0, 0, 50))
        screen.blit(self.ship.image, self.ship.rect)
        self.bullets.draw(screen)
        self.fleet.draw(screen)
        self.scoreboard.draw(screen)

    @property
    def finished(self):
        return self.stats.ships_left == 0

    def get_next(self):
        return self.game_over

    def __player_destroyed(self):
        if self.stats.player_alive:
            # Reduce player lives
            self.stats.decrease_lives()

            # create a new fleet
            self.fleet.create_new_fleet()

            # reset player position and state
            self.ship.center_ship()
            self.ship.destroyed = False

        else:  # no ships left
            pass  # done

    def __on_alien_killed(self, alien):
        self.stats.increase_score(self.ai_settings.alien_points)

    def __on_fleet_destroyed(self):
        # advance to next level
        self.stats.increase_level()

        # clear all bullets
        self.bullets.clear()
