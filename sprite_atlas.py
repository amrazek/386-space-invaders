import os
import copy
import pygame
from animation import Animation
from animation import StaticAnimation
import config


def load_atlas():
    atlas = SpriteAtlas(os.path.join('images', 'atlas.png'))

    atlas.initialize_static("ship", color_key=config.transparent_color, generate_mask=True)
    atlas.initialize_static("player_bullet", color_key=config.transparent_color, generate_mask=True)
    atlas.initialize_animation("alien1", 64, 64, 5, color_key=config.transparent_color)
    atlas.initialize_animation("alien2", 64, 64, 1, color_key=config.transparent_color)

    frames = generate_alien_bullet_frames(config.default_alien_bullet.size, config.default_alien_bullet.color)

    atlas.initialize_animation_from_frames("alien_bullet", frames, 0.5, generate_masks=True)
    config.atlas = atlas


def generate_alien_bullet_frames(wh, color):
    num_vertical_zigzags = 5

    previous_location = (0, 0)

    frames = []

    for start_side in [True, False]:
        left_side = start_side

        surf = pygame.Surface(wh)
        surf.set_colorkey(config.transparent_color)

        for y in range(0, surf.get_height(), surf.get_height() // num_vertical_zigzags):
            next_location = (0 if left_side else surf.get_width(), y)
            pygame.draw.aaline(surf, color, previous_location, next_location)
            previous_location = next_location
            left_side = not left_side

        frames.append(surf)

    return frames


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
        self._sprite_rects = {}

        for line in file:
            # of the form: name = left top width height
            name, rect_str = [s.strip() for s in line.split('=')]
            rect = self._get_rect_from_str(rect_str)

            # add sprite to dictionary
            self._sprite_rects[name] = rect

        self.animations = {}
        self.statics = {}  # statics aren't initialized to anything by default so user can specify color key if wanted

    def initialize_animation(self, name, frame_width, frame_height, duration, color_key=None, generate_masks=False):
        if name in self.animations:
            return self.animations[name]

        # grab rect for this name
        if name not in self._sprite_rects:
            raise SpriteNotFoundException(name)

        rect = self._sprite_rects[name]

        frame_height = frame_height or frame_width

        if rect.width % frame_width != 0 or rect.height % frame_height != 0:
            raise InvalidDimensionsException(name, rect, (frame_width, frame_height))

        frames = [self.atlas.subsurface(
            pygame.Rect(x, y, frame_width, frame_height))
            for x in range(rect.x, rect.x + rect.width, frame_width)
            for y in range(rect.y, rect.y + rect.height, frame_height)]

        if color_key is not None:
            # cannot use per-pixel alpha values in this case
            converted = [s.convert() for s in frames]
            frames = converted

            for f in frames:
                f.set_colorkey(color_key)

        masks = [pygame.mask.from_threshold(surf, color_key or config.transparent_color) for surf in frames]\
            if generate_masks else None

        animation = Animation(frames, duration, masks)

        self.animations[name] = animation

    def initialize_static(self, name, color_key=None, generate_mask=False):
        rect = self._fetch(name, self._sprite_rects)

        surf = self.atlas.subsurface(rect)

        if color_key is not None:
            surf = surf.convert()
            surf.set_colorkey(color_key)

        mask = pygame.mask.from_threshold(surf, color_key or config.transparent_color) if generate_mask else None
        self.statics[name] = StaticAnimation(surf, mask)

    def initialize_static_from_surface(self, name, surf, generate_mask=False):
        mask = pygame.mask.from_threshold(surf, surf.get_colorkey()) if generate_mask else None
        self.statics[name] = StaticAnimation(surf, mask)

    def initialize_animation_from_frames(self, name, frames, duration, generate_masks=False):
        assert len(frames) > 0

        masks = [pygame.mask.from_threshold(surf,
                                            frames[0].get_colorkey() or config.transparent_color)
                 for surf in frames] if generate_masks else None

        self.animations[name] = Animation(frames, duration, masks)

    def load_static(self, name):
        return copy.copy(self._fetch(name, self.statics))

    def load_animation(self, name):
        return copy.copy(self._fetch(name, self.animations))

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
