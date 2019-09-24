import sys
import pygame


class InputState:
    def __init__(self):
        self.left, self.right, self.fire = False, False, False
        self.quit = False

        self.left_click = False
        self.mouse_pos = (0, 0)

        self.key_actions = {
            pygame.K_q: self.__quit,
            pygame.K_LEFT: self.__left,
            pygame.K_RIGHT: self.__right,
            pygame.K_SPACE: self.__fire
        }

    def __quit(self, state):
        self.quit = state

    def __left(self, state):
        self.left = state

    def __right(self, state):
        self.right = state

    def __fire(self, state):
        self.fire = state

    def do_events(self):
        self.mouse_pos = pygame.mouse.get_pos()

        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            else:
                if (evt.type == pygame.KEYDOWN or evt.type == pygame.KEYUP) and evt.key in self.key_actions:
                    state = True if evt.type == pygame.KEYDOWN else False

                    action = self.key_actions[evt.key]

                    if action is not None:
                        action(state)

                elif evt.type == pygame.MOUSEBUTTONDOWN:
                    self.left_click = True
                elif evt.type == pygame.MOUSEBUTTONUP:
                    self.left_click = False
