from pygame.sprite import Sprite


class AnimatedSprite(Sprite):
    """Class that represents an animation"""
    def __init__(self, frames, duration):
        super().__init__()

        assert duration >= 0.0
        assert len(frames) > 0

        self._frames = frames
        self._frame_count = len(self._frames)
        self.duration = duration

        self._current_frame = 0
        self._accumulator = 0.0

        self.image = self._frames[0]
        self.rect = self._frames[0].get_rect()

    def update(self, elapsed):
        self._accumulator += elapsed

        while self._accumulator >= self._time_per_frame:
            self._accumulator -= self._time_per_frame
            self._current_frame = (self._current_frame + 1) % self._frame_count
            self.image = self._frames[self._current_frame]

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, value):
        assert value >= 0
        self._duration = value
        self._time_per_frame = self.duration / float(self._frame_count)
