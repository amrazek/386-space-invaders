import pygame


class AnimatedSprite(pygame.sprite.Sprite):
    """Class that represents a sequence of images. Frames must be square. """
    def __init__(self, sprite_sheet, animation_rate):
        super().__init__()

        self._sprite_sheet = sprite_sheet

        rect = sprite_sheet.get_rect()

        # all frames are square, so height, height intended
        width, height = rect.height, rect.height
        self.rect = pygame.Rect(0, 0, width, height)

        num_frames = rect.width // width

        self._frames = [pygame.Rect(i * width, 0, width, height) for i in range(num_frames)]
        self._frame_count = len(self._frames)

        self._current_frame = 0
        self._last_tick = pygame.time.get_ticks()
        self._ticks_per_frame = round(1000.0 / num_frames * (1.0 / animation_rate))

        self.image = self._sprite_sheet.subsurface(self._frames[self._current_frame])

    def update(self, elapsed):
        this_tick = pygame.time.get_ticks()
        elapsed = this_tick - self._last_tick

        if elapsed > self._ticks_per_frame:
            self._last_tick = this_tick
            self.__set_frame(self._current_frame + 1)
            self.image = self._sprite_sheet.subsurface(self._frames[self._current_frame])

    def __set_frame(self, frame):
        assert frame >= 0
        self._current_frame = frame % self._frame_count

