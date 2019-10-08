import random
import pygame
from pygame.sprite import Sprite
import config


class BunkerFragment(Sprite):
    def __init__(self, surf, center_position):
        super().__init__()

        self.image = surf
        self.rect = surf.get_rect()
        self.rect.center = center_position
        self.health = config.bunker_fragment_health

        # note: since some fragments are not entirely filled, we need to get number of actual pixels
        # that are not transparent and use that to determine dissolve parameters
        color_key_color = surf.get_colorkey()

        assert color_key_color is not None

        transparent_num_pixels = pygame.transform.threshold(None, surf, color_key_color, set_behavior=0,
                                                            inverse_set=True)

        num_pixels = surf.get_width() * surf.get_height() - transparent_num_pixels

        self._num_pixels_per_dissolve = num_pixels // self.health if self.health > 0 else num_pixels

    @property
    def dead(self):
        return self.health == 0

    def damage(self):
        self.health -= 1

        # apply damage effect to this section
        if self.health <= 0:
            self.image.set_alpha(0)
            return

        pixels = pygame.PixelArray(self.image)  # will lock surface, if required

        num_pixels = self._num_pixels_per_dissolve
        transparent_color = self.image.get_colorkey()
        w, h = self.image.get_width(), self.image.get_height()
        mapped_transparent_color = self.image.map_rgb(transparent_color)

        while num_pixels > 0:
            # randomly choose a location
            x, y = random.randrange(0, w), random.randrange(0, h)

            # make sure that pixel isn't already transparent
            current_color = pixels[x, y]

            if current_color == transparent_color:
                continue

            pixels[x, y] = mapped_transparent_color
            num_pixels -= 1

        pixels.close()


class Bunker:
    def __init__(self, center_position, player_bullets, enemy_bullets):
        super().__init__()

        #img = generate_bunker_surface()
        img = config.atlas.load_static("bunker").image

        fragments = Bunker._create_bunker_fragments(img, center_position)
        self._fragments = pygame.sprite.Group(fragments)
        self._bullets = [player_bullets, enemy_bullets]

    def update(self, elapsed):
        self._fragments.update(elapsed)

        # check for collisions with any bullets
        for bullet_mgr in self._bullets:
            collisions = pygame.sprite.groupcollide(self._fragments, bullet_mgr, False, True)

            for pair in collisions.items():
                fragment = pair[0]
                bullets = pair[1]  # a list of hits

                for _ in bullets:
                    fragment.damage()

                    if fragment.dead:
                        break

            if len(collisions) > 0:
                # remove any dead fragments
                for fragment in self._fragments.copy():
                    if fragment.dead:
                        self._fragments.remove(fragment)

    def draw(self, screen):
        self._fragments.draw(screen)

    @staticmethod
    def create_bunkers(count, ship, player_bullets, enemy_bullets):
        # create [count] evenly-spaced bunkers
        spacing = config.screen_width // (count + 1)
        bottom = config.screen_height - int(ship.rect.height * config.bunker_offset_from_ship)

        return [Bunker((center, bottom - config.bunker_tile_size * 2), player_bullets, enemy_bullets)
                for center in range(spacing, config.screen_width, spacing)]

    @classmethod
    def _create_bunker_fragments(cls, surf, bunker_center):
        fragments = []

        src_rect = pygame.Rect(0, 0, config.bunker_tile_size, config.bunker_tile_size)
        dest_rect = src_rect.copy()

        for x in range(0, surf.get_rect().width, config.bunker_tile_size):
            for y in range(0, surf.get_rect().height, config.bunker_tile_size):
                slice_surf = pygame.Surface(src_rect.size)
                slice_surf.fill(config.transparent_color)
                slice_surf.blit(surf, dest_rect, src_rect)

                # avoid creating blank slices by making sure the tile has some content
                threshold = pygame.transform.threshold(None, slice_surf, surf.get_colorkey(), set_behavior=0)
                slice_surf.set_colorkey(config.transparent_color)

                if threshold < dest_rect.width * dest_rect.height * 0.5:  # less than 50% transparent
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
