import pygame
from states.game_state import GameState
from states.high_score import EnterHighScore
import config
import sounds


class GameOver(GameState):
    DURATION = 1.0

    def __init__(self, input_state, previous_state):
        super().__init__(input_state)

        sounds.silence()
        self.previous_state = previous_state

        # create game over text
        font = pygame.font.SysFont("", 48)
        font_surf = font.render("Game Over", True, config.text_color)

        # create a square 1/4 screen dimensions
        self.dialog_rect = pygame.Rect(0, 0, config.screen_width // 4, font_surf.get_rect().height * 2)
        self.dialog = pygame.Surface((self.dialog_rect.width, self.dialog_rect.height))

        # fill with dialog color
        self.dialog.fill(color=(0, 200, 0))

        # create black border to set dialog apart more
        border_rect = self.dialog.get_rect()
        border_rect.left = border_rect.top = 5
        border_rect.width, border_rect.height = border_rect.width - 10, border_rect.height - 10

        pygame.draw.rect(self.dialog, (0, 0, 0), border_rect, 5)

        # blit game over text, centered, onto dialog
        blit_rect = font_surf.get_rect()
        blit_rect.center = (self.dialog_rect.width // 2, self.dialog_rect.height // 2)

        self.dialog.blit(font_surf, dest=blit_rect)
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
