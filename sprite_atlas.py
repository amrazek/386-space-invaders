import pygame

alien = None
alien_animation_rate = 1.0


def load_atlas():
    global alien

    alien = pygame.image.load("images/alien1.bmp")
    set_color_key_from_pixel(alien, (0, 0))


def set_color_key_from_pixel(image, coord):
    color = image.get_at(coord)

    image.set_colorkey(color, pygame.RLEACCEL)
