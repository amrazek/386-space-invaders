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
        self.width = frames[0].get_width()
        self.height = frames[0].get_height()

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
            self.next_frame()

    @property
    def frame(self):
        return self.current_frame_index

    @frame.setter
    def frame(self, idx):
        assert 0 <= idx < self.frame_count
        self.current_frame_index = idx
        self.current_frame = self.frames[idx]

    def next_frame(self):
        cur = self.frame + 1

        self.frame = cur if cur < self.frame_count else 0
        self.current_mask = self.masks[self.frame] if self.masks else None

    @property
    def image(self):
        return self.current_frame

    @property
    def mask(self):
        return self.current_mask


class StaticAnimation(Animation):
    def __init__(self, frames, mask=None):
        # quietly convert parameters to lists if needed. This allows this class to be a truly static "animation"
        # (such that frames are manipulated manually) or actually just a one-frame not-actually-animated thing, which
        # can be interchangeably used anywhere Animation is
        if not isinstance(frames, list):
            frames = [frames]
        if mask is not None and not isinstance(mask, list):
            mask = [mask]

        super().__init__(frames, 0.0, mask)

    def update(self, elapsed):
        pass
