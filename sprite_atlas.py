import os
import copy
import random
import math
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

    # alien bullet frames
    frames = generate_alien_bullet_frames(config.default_alien_bullet.size, config.default_alien_bullet.color)
    atlas.initialize_animation_from_frames("alien_bullet", frames, 0.5, generate_masks=True)

    # explosion frames for ship
    frames = generate_explosion_frames(atlas.load_static("ship").image, 16, .5, 1.25, 15.5, 4.0)
    atlas.initialize_animation_from_frames("ship_explosion", frames, .5)

    # explosion frames for aliens
    keys = atlas.animations.keys()
    alien_keys = [k for k in atlas.animations.keys() if k.startswith("alien")]

    for key in [k for k in atlas.animations.keys() if k.startswith("alien")]:
        frames = generate_explosion_frames(atlas.load_animation(key).image, 4, .25, 1.25, 6.5)
        atlas.initialize_animation_from_frames(key + "_explosion", frames, 1.0)

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


def generate_explosion_frames(from_surf, num_frames, duration, min_velocity, max_velocity, scale_multiplier=1.):
    frames = []
    original_pixels = pygame.PixelArray(from_surf)

    class Pixel:
        color: pygame.Color
        position: pygame.Vector2
        velocity: pygame.Vector2

        def __init__(self, x, y, color, velocity):
            self.position = pygame.Vector2()
            self.position.x, self.position.y = x, y
            self.color = color
            self.velocity = velocity

    def random_angle():
        return random.uniform(0, 2.0 * math.pi)

    def random_velocity():
        velocity = random.uniform(0, max_velocity - min_velocity) + min_velocity
        v = pygame.Vector2()
        a = random_angle()

        v.x = math.cos(a) * velocity
        v.y = math.sin(a) * velocity

        return v

    frame_pixels = [Pixel(
        color=from_surf.unmap_rgb(original_pixels[x, y]),
        x=float(x),
        y=float(y),
        velocity=random_velocity())
        for x in range(from_surf.get_width()) for y in range(from_surf.get_height())]

    frame_rect = pygame.Rect(0, 0, from_surf.get_width(), from_surf.get_height())
    frame_rect.width = int(frame_rect.width * scale_multiplier)
    frame_rect.height = int(frame_rect.height * scale_multiplier)

    # if the original surface had an alpha color, we should set those pixels to invisible to begin with
    if from_surf.get_colorkey is not None:
        for pixel in frame_pixels:
            x, y = int(pixel.position.x), int(pixel.position.y)

            if from_surf.unmap_rgb(original_pixels[x, y]) == from_surf.get_colorkey():
                pixel.color = pygame.Color(255, 0, 255, 0)

    elapsed = 0.0

    frame_offset_x = frame_rect.width // 2 - from_surf.get_width() // 2
    frame_offset_y = frame_rect.height // 2 - from_surf.get_height() // 2

    for frame_index in range(num_frames):

        # update pixel positions and alpha
        for pixel in frame_pixels:
            pixel.position += pixel.velocity * elapsed
            alpha = int(255 - 255 * (elapsed / duration)) if pixel.color.a > 0 else 0
            pixel.color.a = alpha

        elapsed += duration / float(num_frames)

        # generate this surface, with per-pixel alpha
        surf = pygame.Surface(frame_rect.size).convert_alpha(pygame.display.get_surface())
        surf.fill((0, 0, 0, 0))  # fill with transparent
        p = pygame.PixelArray(surf)

        for idx in range(len(frame_pixels)):
            x_coord = int(frame_pixels[idx].position.x) + frame_offset_x
            y_coord = int(frame_pixels[idx].position.y) + frame_offset_y

            if 0 <= x_coord < surf.get_width() and 0 <= y_coord < surf.get_height():
                p[x_coord, y_coord] = surf.map_rgb(frame_pixels[idx].color)

        p.close()
        frames.append(surf)

    original_pixels.close()

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

        masks = [pygame.mask.from_threshold(surf, color_key or config.transparent_color) for surf in frames] \
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
