class Animation:
    duration: float
    frames: []

    def __init__(self, frames, duration, masks=None):
        assert len(frames) > 0
        assert duration >= 0
        assert not masks or (masks and len(masks) == len(frames))

        self.frames = frames
        self.frame_count = len(frames)
        self.duration = duration
        self.current_frame_index = 0
        self.accumulator = 0.0
        self.current_frame = frames[0]
        self.masks = masks
        self.current_mask = self.masks[0] if self.masks else None

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, value):
        assert value >= 0
        self._duration = value
        self._time_per_frame = self.duration / float(self.frame_count)

    def update(self, elapsed):
        self.accumulator += elapsed

        while self.accumulator >= self._time_per_frame:
            self.accumulator -= self._time_per_frame
            self.current_frame_index = (self.current_frame_index + 1) % self.frame_count
            self.current_frame = self.frames[self.current_frame_index]
            self.current_mask = self.masks[self.current_frame_index] if self.masks else None

    @property
    def image(self):
        return self.current_frame

    @property
    def mask(self):
        return self.current_mask
