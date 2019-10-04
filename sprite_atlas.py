import os
import copy
import pygame
from animated_sprite import AnimatedSprite


def load_atlas():
    atlas = SpriteAtlas(os.path.join('images', 'atlas.png'))

    atlas.initialize_static("ship")
    atlas.initialize_animation("alien1", 64, 64, 5)
    atlas.initialize_animation("alien2", 64, 64, 1)


class SpriteAtlasException(Exception):
    def __init__(self, name):
        super().__init__()
        self.name = name


class SpriteNotFoundException(SpriteAtlasException):
    def __init__(self, sprite_name):
        super().__init__(sprite_name)


class InvalidDimensionsException(SpriteAtlasException):
    def __init__(self, name, rect, wh):
        super().__init__(name)
        self.rect = rect
        self.dimensions = wh


class SpriteAtlas:
    def __init__(self, atlas_path):
        # locate atlas descriptor
        basename = os.path.splitext(atlas_path)[0]
        atlas_descriptor = basename + '.txt'

        if not os.path.exists(atlas_descriptor) or not os.path.exists(atlas_path):
            raise FileNotFoundError

        self.atlas = pygame.image.load(atlas_path)

        if not self.atlas:
            raise RuntimeError

        file = open(atlas_descriptor, 'r')

        if not file:
            raise RuntimeError

        # use the descriptor file to load subsurfaces
        self._sprites = {}

        for line in file:
            # of the form: name = left top width height
            name, rect_str = [s.strip() for s in line.split('=')]
            rect = self._get_rect_from_str(rect_str)

            # add sprite to dictionary
            self._sprites[name] = rect

        self._animations = {}
        self._statics = {}  # statics aren't initialized to anything by default so user can specify color key if wanted

    def initialize_animation(self, name, frame_width, frame_height, duration, color_key=None):
        if name in self._animations:
            return self._animations[name]

        # grab rect for this name
        if name not in self._sprites:
            raise SpriteNotFoundException(name)

        rect = self._sprites[name]

        frame_height = frame_height or frame_width

        if rect.width % frame_width != 0 or rect.height % frame_height != 0:
            raise InvalidDimensionsException(name, rect, (frame_width, frame_height))

        frames = [self.atlas.subsurface(
            pygame.Rect(x, y, frame_width, frame_height))
            for x in range(0, rect.width, frame_width)
            for y in range(0, rect.height, frame_height)]

        if color_key is not None:
            for f in frames:
                f.set_colorkey(color_key)

        sprite = AnimatedSprite(frames, duration)
        self._animations[name] = sprite

    def initialize_static(self, name, color_key=None):
        rect = self._fetch(name, self._sprites)

        sprite = self.atlas.subsurface(rect)

        if color_key is not None:
            sprite.set_colorkey(color_key)

        self._statics[name] = sprite

    def load_static(self, name):
        return copy.copy(self._fetch(name, self._statics))

    def load_animation(self, name):
        return copy.copy(self._fetch(name, self._animations))

    @staticmethod
    def _fetch(name, location):
        if name not in location:
            raise SpriteNotFoundException(name)
        return location[name]

    @staticmethod
    def _get_rect_from_str(rect_str):
        r = pygame.Rect(0, 0, 0, 0)

        r.left, r.top, r.width, r.height = [int(x) for x in rect_str.split(' ')]

        return r
