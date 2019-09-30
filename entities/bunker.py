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

    # fill bottoms of legs and center
    color = (0, 255, 0)
    r = pygame.Rect(0, 0, tile_size, tile_size)

    # bottom left
    r.left, r.bottom = 0, wh[1]
    surf.fill(color, r)

    # bottom right
    r.right = wh[0]
    surf.fill(color, r)

    # middle brace
    r.top = 0
    r.left = config.bunker_tile_size
    surf.fill(color, r)

    # left and right arcs. we'll borrow another surface drawn with a circle to make this easy
    circle = pygame.Surface((tile_size * 2, tile_size * 2))
    circle.fill(bkg)
    pygame.draw.circle(circle, color, circle.get_rect().center, tile_size)

    # left arc
    circle_rect = pygame.Rect(0, 0, tile_size, tile_size)
    r.left, r.top = 0, 0
    surf.blit(circle, r, circle_rect)

    # right arc
    r.right = surf.get_rect().width
    circle_rect.right = tile_size * 2
    surf.blit(circle, r, circle_rect)

    return surf


class Bunker(Sprite):
    def __init__(self, center_position):
        super().__init__()

        self.image = generate_bunker_surface()
        self.rect = self.image.get_rect()
        self.rect.center = center_position

    @staticmethod
    def create_bunkers(count, ship):
        # create [count] evenly-spaced bunkers
        spacing = config.screen_width // (count + 1)
        bottom = config.screen_height - int(ship.rect.height * config.bunker_offset_from_ship)

        return [Bunker((center, bottom - config.bunker_tile_size * 2))
                for center in range(spacing, config.screen_width, spacing)]

    @classmethod
    def _slice_bunker_surf(cls, surf):
        slices = pygame.sprite.Group()

        for x in range(0, surf.get_rect().width, config.bunker_tile_size):
            for y in range(0, surf.get_rect().height, config.bunker_tile_size):




