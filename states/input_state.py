import sys
import pygame


class InputState:
    def __init__(self):
        self.left, self.right, self.fire = False, False, False
        self.quit = False

        self.left_down = False
        self.mouse_pos = (0, 0)

        self.key_actions = {
            pygame.K_ESCAPE: self.__quit,
            pygame.K_LEFT: self.__left,
            pygame.K_RIGHT: self.__right,
            pygame.K_SPACE: self.__fire
        }

        self.keys = []

    def __quit(self, state):
        self.quit = state

    def __left(self, state):
        self.left = state

    def __right(self, state):
        self.right = state

    def __fire(self, state):
        self.fire = state

    def do_events(self):
        self.keys.clear()
        self.mouse_pos = pygame.mouse.get_pos()

        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            else:
                if evt.type == pygame.KEYDOWN or evt.type == pygame.KEYUP:
                    state = True if evt.type == pygame.KEYDOWN else False

                    if state:
                        self._handle_text_entry(evt.key)

                    if evt.key in self.key_actions:
                        action = self.key_actions[evt.key]

                        if action is not None:
                            action(state)

                elif evt.type == pygame.MOUSEBUTTONDOWN:
                    self.left_down = True
                elif evt.type == pygame.MOUSEBUTTONUP:
                    self.left_down = False

    def _handle_text_entry(self, key):
        alpha = pygame.K_a <= key <= pygame.K_z
        digit = not alpha and pygame.K_0 <= key <= pygame.K_9

        if alpha or digit or key == pygame.K_SPACE:
            upper = pygame.key.get_mods() & pygame.KMOD_SHIFT
            key = key & ~0x20 if alpha and (pygame.key.get_mods() & pygame.KMOD_SHIFT) else key

            self.keys.append(chr(key))
