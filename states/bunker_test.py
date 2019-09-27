import random
from PIL import Image
import pygame
from states.game_state import GameState
import config


class BunkerTest(GameState):
    def __init__(self, input_state):
        super().__init__(input_state)

        self.bunker = pygame.Surface((256, 256), depth=16)
        self.rect = self.bunker.get_rect()
        self.rect.center = config.screen_rect.center

        # fill bunker with green
        self.bunker.fill((0, 255, 0))
        self.bunker = self.bunker.convert_alpha()

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
                self.damage_bunker_pil()
        else:
            #self.did_damage = False
            pass

    def draw(self, screen):
        screen.fill((255, 0, 0))

        screen.blit(self.bunker, self.rect)

    def damage_bunker(self):
        #self.bunker.fill(color=(0, 0, 255))

        # project requirements say to use PIL rather than SDL surface/pygame functions? why?
        from pygame import PixelArray

        pixels = PixelArray(self.bunker)

        num_random_pixels = self.rect.width * self.rect.height // 2

        while num_random_pixels > 0:
            # select a pixel at random
            pix_x = random.randrange(0, self.rect.width)
            pix_y = random.randrange(0, self.rect.height)

            color = self.bunker.unmap_rgb(pixels[pix_x, pix_y])
            if color.a > 0:
                color.a = 0
                pixels[pix_x, pix_y] = self.bunker.map_rgb(color)
                num_random_pixels -= 1


        # for col in range(self.rect.width):
        #     for row in range(self.rect.height):
        #         new_color = self.bunker.unmap_rgb(pixels[col, row])
        #         new_color.a = max(new_color.a - 10, 0)
        #         pixels[col, row] = self.bunker.map_rgb(new_color)
        #         #pixels[col, row] = self.bunker.map_rgb(pygame.Color(0, 0, 0, 0))

        pixels.close()

    def damage_bunker_pil(self):
        img_bytes = pygame.image.tostring(self.bunker, "RGBA", False)
        img = Image.frombytes("RGBA", (self.rect.width, self.rect.height), img_bytes)

        rotated = img.rotate(45)

        img_bytes = rotated.tobytes("raw")

        self.bunker = pygame.image.fromstring(img_bytes, (self.rect.width, self.rect.height), "RGBA")
