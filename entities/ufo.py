import random
from pygame.sprite import Sprite
import config


class Ufo(Sprite):
    def __init__(self, session_stats, animation):
        super().__init__()
        self.animation = animation
        self.session_stats = session_stats
        self.rect = self.animation.rect
        self.image = self.animation.image

        start = random.choice([(-self.rect.width * 0.5, 1.), (config.screen_width + self.rect.width * 0.5, -1.)])
        self.position = start[0]
        self.speed = session_stats.alien_speed * start[1]

        self.rect.centerx = int(self.position)

    def update(self, elapsed):
        self.animation.update(elapsed)
        self.image = self.animation.image

        # update position
        self.position += self.speed * elapsed
        self.rect.centerx = int(self.position)
