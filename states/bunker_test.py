import random
from PIL import Image
import pygame
from states.game_state import GameState
import config
from entities.bunker import generate_bunker_surface





class BunkerTest(GameState):
    def __init__(self, input_state):
        super().__init__(input_state)

        self.bunker = pygame.Surface((256, 256), depth=16)
        self.bunker_rect = self.bunker.get_rect()
        self.bunker_rect.center = config.screen_rect.center
        self.bunker_rect.top = config.screen_rect.top

        # fill bunker with green
        # self.bunker.fill((0, 255, 0))
        # self.bunker = self.bunker.convert_alpha()
        self.bunker = generate_bunker_surface()

        self.bunker_pil = self.bunker.copy()
        self.bunker_pil_rect = self.bunker_rect.copy()
        self.bunker_pil_rect.bottom = config.screen_rect.bottom

        # states
        self.did_damage = False

    @property
    def finished(self):
        return False

    def get_next(self):
        return None

    def update(self, elapsed):
        if self.input_state.fire:
            if not self.did_damage:
                self.did_damage = True
                #self.damage_bunker()
                self.damage_bunker_pil()
        else:
            self.did_damage = False

    def draw(self, screen):
        screen.fill((0, 0, 0))

        # non-pil rect

        screen.blit(self.bunker, self.bunker_rect)

        # pil rect
        screen.blit(self.bunker_pil, self.bunker_pil_rect)

    # def damage_bunker(self):
    #     #self.bunker.fill(color=(0, 0, 255))
    #
    #     # project requirements say to use PIL rather than SDL surface/pygame functions? why?
    #     from pygame import PixelArray
    #
    #     pixels = PixelArray(self.bunker)
    #
    #     num_random_pixels = self.bunker_rect.width * self.bunker_rect.height // 2
    #
    #     while num_random_pixels > 0:
    #         # select a pixel at random
    #         pix_x = random.randrange(0, self.rect.width)
    #         pix_y = random.randrange(0, self.rect.height)
    #
    #         color = self.bunker.unmap_rgb(pixels[pix_x, pix_y])
    #         if color.a > 0:
    #             color.a = 0
    #             pixels[pix_x, pix_y] = self.bunker.map_rgb(color)
    #             num_random_pixels -= 1


        # for col in range(self.rect.width):
        #     for row in range(self.rect.height):
        #         new_color = self.bunker.unmap_rgb(pixels[col, row])
        #         new_color.a = max(new_color.a - 10, 0)
        #         pixels[col, row] = self.bunker.map_rgb(new_color)
        #         #pixels[col, row] = self.bunker.map_rgb(pygame.Color(0, 0, 0, 0))

        #pixels.close()

    def damage_bunker_pil(self):
        img_bytes = pygame.image.tostring(self.bunker_pil, "RGBA", False)
        img = Image.frombytes("RGBA", (self.bunker_rect.width, self.bunker_rect.height), img_bytes)

        nonpil_pixels = pygame.PixelArray(self.bunker)

        #rotated = img.rotate(45)

        for x in range(self.bunker_rect.width // 2):
            for y in range(self.bunker_rect.height // 2):
                # edit pil image
                cur = img.getpixel((x, y))
                cur = (cur[0], cur[1], cur[2], max(0, cur[3] - 10))
                img.putpixel((x, y), cur)

                # edit non-pil image
                cur = self.bunker.unmap_rgb(nonpil_pixels[x, y])
                cur.a = max(0, cur.a - 10)
                nonpil_pixels[x, y] = self.bunker.map_rgb(cur)

        img_bytes = img.tobytes("raw")

        self.bunker_pil = pygame.image.fromstring(img_bytes, (self.bunker_rect.width, self.bunker_rect.height), "RGBA")
        nonpil_pixels.close()
