import os
import pygame

alien_images = ["alien1.bmp", "alien2.bmp"]

aliens = []
alien_animation_rate = 1.0


def load_atlas():
    global aliens

    aliens = [load_image(name) for name in alien_images]


def load_image(name, ck_pixel=(0,0)):
    path = os.path.join("images", name)

    img = pygame.image.load(path)
    set_color_key_from_pixel(img, ck_pixel)

    return img


def set_color_key_from_pixel(image, coord):
    color = image.get_at(coord)

    image.set_colorkey(color, pygame.RLEACCEL)
