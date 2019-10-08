from typing import NamedTuple
from typing import Callable
import os
import pygame
from pygame.sprite import Group
import config
from states.game_state import GameState
from animation import StaticAnimation


class _MenuOption(NamedTuple):
    text: str
    callback: Callable


class Menu(GameState):
    def __init__(self, input_state):
        super().__init__(input_state)
        self.sprites = Group()
        self.font = pygame.font.SysFont(None, 48)

        # create "Space Invaders" logo
        logo = self.font.render("Space Invaders", True, config.text_color)
        self.sprites.add(logo)

        frame = pygame.Surface(200, 40)

        # create menu options
        opts = StaticAnimation(frame)

    def update(self, elapsed):
        self.sprites.update(elapsed)

    def draw(self, screen):
        screen.fill((255, 0, 255))

        self.sprites.draw(screen)

    @property
    def finished(self):
        return False

    def get_next(self):
        raise NotImplementedError