import pygame
from pygame.sprite import Sprite
import config


def generate_bunker_surface():
    tile_size = config.bunker_tile_size

    wh = (tile_size * 3, tile_size * 2)

    surf = pygame.Surface(wh)

    bkg = pygame.Color('black')
    surf.fill(bkg)
    surf.set_colorkey(bkg)

    # fill bottom two-thirds of bunker
    r = surf.get_rect()
    r.height -= tile_size
    r.bottom = surf.get_height()
    surf.fill(config.bunker_color, r)

    # fill top tile between the two "legs"
    surf.fill(config.bunker_color, pygame.Rect(tile_size, 0, tile_size, tile_size))

    # left circle to create rounded "left shoulder"
    r.width, r.height = tile_size * 2, tile_size * 2
    r.center = (tile_size, tile_size)
    pygame.draw.circle(surf, config.bunker_color, r.center, tile_size)

    # right circle
    r.center = (surf.get_width() - tile_size, r.centery)
    pygame.draw.circle(surf, config.bunker_color, r.center, tile_size)

    # clip out the bottom square which is not part of the bunker
    r.width, r.height = tile_size, tile_size
    r.left, r.bottom = tile_size, surf.get_height()

    surf.fill(bkg, r)

    return surf.convert()


class BunkerFragment(Sprite):
    def __init__(self, surf, center_position):
        super().__init__()

        self.image = surf
        self.rect = surf.get_rect()
        self.rect.center = center_position


class Bunker:
    def __init__(self, center_position):
        super().__init__()

        img = generate_bunker_surface()

        self._fragments = pygame.sprite.Group(Bunker._create_bunker_fragments(img, center_position))

    def update(self, elapsed):
        self._fragments.update(elapsed)

    def draw(self, screen):
        self._fragments.draw(screen)

    @staticmethod
    def create_bunkers(count, ship):
        # create [count] evenly-spaced bunkers
        spacing = config.screen_width // (count + 1)
        bottom = config.screen_height - int(ship.rect.height * config.bunker_offset_from_ship)

        return [Bunker((center, bottom - config.bunker_tile_size * 2))
                for center in range(spacing, config.screen_width, spacing)]

    @classmethod
    def _create_bunker_fragments(cls, surf, bunker_center):
        fragments = []

        src_rect = pygame.Rect(0, 0, config.bunker_tile_size, config.bunker_tile_size)
        dest_rect = src_rect.copy()

        for x in range(0, surf.get_rect().width, config.bunker_tile_size):
            for y in range(0, surf.get_rect().height, config.bunker_tile_size):
                slice_surf = pygame.Surface(src_rect.size)
                slice_surf.blit(surf, dest_rect, src_rect)
                slice_surf.set_colorkey(config.transparent_color)

                # avoid creating blank slices by making sure the tile has some content
                threshold = pygame.transform.threshold(None, slice_surf, config.transparent_color, set_behavior=0)

                if threshold < dest_rect.width * dest_rect.height:
                    r = src_rect.copy()
                    r.left -= surf.get_width() // 2
                    r.top -= surf.get_height() // 2

                    r.left += bunker_center[0]
                    r.top += bunker_center[1]

                    fragment = BunkerFragment(slice_surf, r.center)
                    fragments.append(fragment)

                src_rect.left += config.bunker_tile_size

                if src_rect.left >= surf.get_width():
                    src_rect.left = 0
                    src_rect.top += config.bunker_tile_size

        return fragments
