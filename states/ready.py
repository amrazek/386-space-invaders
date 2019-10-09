import pygame
from .game_state import GameState
from .run_game import RunGame
from animation import StaticAnimation
import config
import util


class Ready(GameState):
    """This state contains a button that begins the game"""

    def __init__(self, input_state):
        super().__init__(input_state)
        self.next_state = None
        self.game = RunGame(self.input_state)

        dialog_surf = util.create_dialog("Click to Begin!", config.text_color, config.green_color, (0, 0, 0), 48,
                                         config.screen_width // 4, 64)

        dialog_surf_mo = util.create_dialog("Begin!", (0, 0, 0), config.text_color, (0, 0, 0), 48,
                                            dialog_surf.get_width(), dialog_surf.get_height())

        self.dialog = StaticAnimation([dialog_surf, dialog_surf_mo])
        self.dialog.rect.center = config.screen_rect.center

    def update(self, elapsed):
        # look for mouseover and mouse click
        if self.dialog.rect.collidepoint(self.input_state.mouse_pos):
            self.dialog.frame = 1  # moused over

            if self.input_state.left_down:
                # click!
                self.input_state.left_down = False
                self.next_state = self.game
                pygame.mouse.set_visible(False)
                self.game.start()  # mainly to start music appropriately
        else:
            self.dialog.frame = 0  # not moused over

        # look for escape, in case player wants to go back to main menu instead
        if self.input_state.quit:
            self.input_state.quit = False

            import states.menu

            self.next_state = states.menu.Menu(self.input_state)

    def draw(self, screen):
        screen.fill(config.transparent_color)
        self.game.draw(screen)

        # draw button
        screen.blit(self.dialog.image, self.dialog.rect)

    @property
    def finished(self):
        return self.next_state is not None

    def get_next(self):
        return self.next_state
