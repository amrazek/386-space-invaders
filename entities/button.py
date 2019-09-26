import pygame.font
import config


class Button:
    def __init__(self, input_state, msg):
        """Initialize button attributes."""
        self.input_state = input_state

        # Set the dimensions and properties of teh button
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Build the button's rect object and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = config.screen_rect.center

        self.msg_image = None
        self.msg_image_rect = None

        self._pressed = False

        # The button message needs to be prepped only once
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button."""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    @property
    def pressed(self):
        return self._pressed

    def update(self):
        if self.input_state.left_down:
            if self.rect.collidepoint(self.input_state.mouse_pos):
                self._pressed = True
                return

        self._pressed = False

    def draw_button(self, screen):
        # Draw blank button and then draw message
        screen.fill(self.button_color, self.rect)
        screen.blit(self.msg_image, self.msg_image_rect)
