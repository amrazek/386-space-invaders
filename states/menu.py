import pygame
from pygame.sprite import Group
import config
from .game_state import GameState
from states.run_game import RunGame
from .high_score import HighScore
from animation import StaticAnimation


class Menu(GameState):
    MenuItemSize = 32
    MenuItemSpacing = 16

    def __init__(self, input_state):
        super().__init__(input_state)
        font = pygame.font.SysFont(None, 48)

        # create "Space Invaders" logo
        self.title = StaticAnimation(font.render("Space Invaders", True, config.text_color))
        self.title.rect.centerx = config.screen_rect.centerx
        self.title.rect.centery = config.screen_height // 8

        last_y = config.screen_height - config.screen_height // 3
        self.options = Group()
        font = pygame.font.SysFont(None, Menu.MenuItemSize)

        # create options
        for option in [("Play Space Invaders", self._play_game),
                       ("High Scores", self._view_high_scores),
                       ("Quit", self._quit)]:
            option_sprite = StaticAnimation(font.render(option[0], True, config.text_color))
            option_sprite.callback = option[1]

            option_sprite.rect.centerx = self.title.rect.centerx
            option_sprite.rect.top = last_y

            last_y = option_sprite.rect.bottom + Menu.MenuItemSpacing
            self.options.add(option_sprite)

        # create a small sprite to use as menu item selector

        left_selector = config.atlas.load_static("selector")

        # need to flip the arrow...
        right_selector = StaticAnimation(pygame.transform.flip(left_selector.image, True, False))
        right_selector.rect.left = config.screen_width

        self.selectors = Group(left_selector, right_selector)

        # finish creating state values
        self.next_state = None
        self._set_selected(0)

    def update(self, elapsed):
        self.options.update(elapsed)
        self.selectors.update(elapsed)

        # handle selected item
        self._handle_arrow_keys()
        self._handle_mouse_clicks()

    def draw(self, screen):
        screen.fill(config.bg_color)

        screen.blit(self.title.image, self.title.rect)
        self.options.draw(screen)
        self.selectors.draw(screen)

    @property
    def finished(self):
        return self.next_state is not None

    def get_next(self):
        return self.next_state

    def _play_game(self):
        self.next_state = RunGame(self.input_state)

    def _view_high_scores(self):
        self.next_state = HighScore(self.input_state)

    def _quit(self):
        self.input_state.quit = True

    def _handle_arrow_keys(self):
        for key_code in self.input_state.key_codes:
            if key_code == pygame.K_RETURN or key_code == pygame.K_KP_ENTER:
                self.options.sprites()[self.selected_index].callback()

        if self.input_state.up and self.input_state.down:
            return  # both up and down at once, just do nothing

        if self.input_state.up:
            self._set_selected(self.selected_index - 1)
            self.input_state.up = False  # don't allow repeating
        elif self.input_state.down:
            self._set_selected(self.selected_index + 1)
            self.input_state.down = False

    def _handle_mouse_clicks(self):
        idx = 0

        for option in self.options.sprites():
            if option.rect.collidepoint(self.input_state.mouse_pos):
                # highlight this option
                self._set_selected(idx)

                if self.input_state.left_down:
                    option.callback()

                break

            idx += 1

    def _set_selected(self, idx):
        while idx < 0:
            idx += len(self.options.sprites())

        idx = idx % len(self.options.sprites())

        self.selected_index = idx

        # align selectors to current option
        for selector in self.selectors.sprites():
            option_rect = self.options.sprites()[idx].rect

            selector.rect.centery = option_rect.centery

            if selector.rect.x < config.screen_width // 2:
                # must be left selector
                selector.rect.right = option_rect.left - 6
            else:
                # right selector
                selector.rect.left = option_rect.right + 6
