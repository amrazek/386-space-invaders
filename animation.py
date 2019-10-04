class Animation:
    duration: float
    frames: []

    def __init__(self, frames, duration):
        assert len(frames) > 0
        assert duration >= 0

        self.frames = frames
        self.frame_count = len(frames)
        self.duration = duration
        self.current_frame_index = 0
        self.accumulator = 0.0
        self.current = frames[0]

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
            self.current = self.frames[self.current_frame_index]

    @property
    def image(self):
        return self.current
