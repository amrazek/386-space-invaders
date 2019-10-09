from states.game_state import GameState
from states.high_score import EnterHighScore
import config
import util
import sounds


class GameOver(GameState):
    DURATION = 1.0

    def __init__(self, input_state, previous_state):
        super().__init__(input_state)

        sounds.silence()
        self.previous_state = previous_state

        font_size = 48
        self.dialog = util.create_dialog("Game Over", (0, 0, 0), (0, 200, 0), (0, 0, 0), font_size,
                                         config.screen_width // 4, font_size * 2)
        self.dialog_rect = self.dialog.get_rect()
        self.dialog_rect.center = config.screen_rect.center
        self.elapsed = 0.0

    def update(self, elapsed):
        self.elapsed += elapsed

    def draw(self, screen):
        self.previous_state.draw(screen, draw_ship=False)
        screen.blit(self.dialog, self.dialog_rect)

    @property
    def finished(self):
        return self.elapsed > GameOver.DURATION

    def get_next(self):
        return EnterHighScore(self.input_state, self.previous_state.stats)
