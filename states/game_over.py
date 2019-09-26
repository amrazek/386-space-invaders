import pygame
from states.game_state import GameState
import config


class GameOver(GameState):
    def __init__(self, input_state, previous_state):
        super().__init__(input_state)

        self.previous_state = previous_state

        # create a square 1/4 screen dimensions
        self.dialog_rect = pygame.Rect(0, 0, config.screen_width // 4, config.screen_height // 4)
        self.dialog = pygame.Surface((self.dialog_rect.width, self.dialog_rect.height))

        # fill with dialog color
        self.dialog.fill(color=(0, 200, 0))

        # create game over text
        font = pygame.font.SysFont("", 48)
        font_surf = font.render("Game Over", True, config.text_color)

        # blit game over text, centered, onto dialog
        blit_rect = font_surf.get_rect()
        blit_rect.center = (self.dialog_rect.width // 2, self.dialog_rect.height // 2)

        self.dialog.blit(font_surf, dest=blit_rect)
        self.dialog_rect.center = config.screen_rect.center

    def update(self, elapsed):
        pass  # todo: check for button? key?

    def draw(self, screen):
        self.previous_state.draw(screen)
        screen.blilt(self.dialog, self.dialog_rect)

