from .game_state import GameState
from .game_over import GameOver
from animation import OneShotAnimation
import config


class PlayerDeath(GameState):
    """This class temporarily takes over when the player dies, playing an animation of their death"""

    def __init__(self, input_state, running_game):
        super().__init__(input_state)

        self.explosion = OneShotAnimation.from_animation(animation=config.atlas.load_animation("ship_explosion"),
                                                         on_complete_callback=self.explosion_callback)
        self.explosion.rect.center = running_game.ship.rect.center

        self.running_game = running_game
        self.next_state = None

    def update(self, elapsed):
        self.running_game.update(0.)
        self.explosion.update(elapsed)

    def draw(self, screen):
        self.running_game.draw(screen, draw_ship=False)
        screen.blit(self.explosion.image, self.explosion.rect)

    @property
    def finished(self):
        return self.next_state is not None

    def get_next(self):
        return self.next_state

    def explosion_callback(self):
        if self.running_game.stats.ships_left > 0:

            # Reduce player lives
            self.running_game.stats.decrease_lives()

            # reset player position and state
            self.running_game.ship.center_ship()

            # clear all bullets
            self.running_game.player_bullets.empty()
            self.running_game.alien_bullets.empty()

            self.running_game.next_state = None  # clear next state so game continues
            self.next_state = self.running_game
        else:
            self.next_state = GameOver(self.input_state, self.running_game)

        self.running_game.scoreboard.set_dirty()
