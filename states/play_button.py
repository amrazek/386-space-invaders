import pygame
import states
from entities.button import Button


class PlayButton(states.game_state.GameState):
    """This game state is simply the initial "Play Game" button from Alien Invaders"""
    def __init__(self, input_state):
        super().__init__(input_state)

        self._game = states.run_game.RunGame(input_state)
        self._button = Button(input_state, "Play Game!")
        pygame.mouse.set_visible(True)

    def update(self, elapsed):
        self._button.update()

    def draw(self, screen):
        self._game.draw(screen)
        self._button.draw_button(screen)

    @property
    def finished(self):
        return self._button.pressed

    def get_next(self):
        pygame.mouse.set_visible(False)
        return self._game  # allow the game to run
