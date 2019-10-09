import random
import copy
import math
import pygame
from pygame import Vector2
from pygame import Color
import config


class _Star:
    position: Vector2
    velocity: Vector2
    twinkle_time: float
    radius: float
    color: Color

    def __init__(self, position, velocity, twinkle_time, radius):
        self.position = position
        self.velocity = velocity
        self.twinkle_time = twinkle_time
        self.radius = radius
        self.color = Color('black')
        self.update(0.)

    def update(self, elapsed):
        self.position += self.velocity * elapsed

        # wrap around screen
        if self.velocity.x < 0. and self.position.x < -self.radius:
            self.position.x = config.screen_width + self.radius
        elif self.velocity.x > 0. and self.position.x > self.radius + config.screen_width:
            self.position.x = -self.radius

        if self.velocity.y < 0. and self.position.y < -self.radius:
            self.position.y = config.screen_height + self.radius
        elif self.velocity.y > 0. and self.position.y > self.radius + config.screen_height:
            self.position.y = -self.radius

        # calculate new color
        self.twinkle_time += elapsed

        while self.twinkle_time > Starfield.TWINKLE_DURATION > 0.:
            self.twinkle_time -= Starfield.TWINKLE_DURATION

        # use cosine wave to determine how much color variation to add/remove
        ratio = math.cos(math.pi * self.twinkle_time / Starfield.TWINKLE_DURATION)
        variation = Starfield.COLOR_VARIATION

        self.color = copy.deepcopy(Starfield.COLOR)
        self.color.r = max(0, min(255, int(self.color.r + (ratio * variation[0]))))
        self.color.g = max(0, min(255, int(self.color.g + (ratio * variation[1]))))
        self.color.b = max(0, min(255, int(self.color.b + (ratio * variation[2]))))

    def draw(self, screen):
        # the star itself
        pygame.draw.circle(screen, self.color, (int(self.position.x), int(self.position.y)), self.radius)

        # trailing line
        line_color = copy.copy(self.color)
        line_color.a = 50


class Starfield:
    COUNT = 100
    MIN_SPEED = 50
    MAX_SPEED = 100  # speed of closest (largest) stars
    MIN_SIZE = 1
    MAX_SIZE = 4
    TRAIL_RATIO = 5   # stars will have a trail of length [this ratio of their speed]
    COLOR = pygame.Color('white')
    COLOR.r, COLOR.g, COLOR.b = 200, 200, 200

    COLOR_VARIATION = (25, 25, 25)  # stars will vary their color +- this amount over twinkle duration
    TWINKLE_DURATION = 2.0  # stars will go min color -> max color -> min color in this many seconds

    def __init__(self):
        # randomly generate some stars
        self.stars = [self._create_star() for _ in range(Starfield.COUNT)]

    @staticmethod
    def _create_star():
        # choose a location at random
        x, y = random.randrange(config.screen_width), random.randrange(config.screen_height)

        # choose a size
        size = random.randrange(Starfield.MIN_SIZE, Starfield.MAX_SIZE)

        # compute speed based on this size
        # small stars travel more slowly
        delta_speed = Starfield.MAX_SPEED - Starfield.MIN_SPEED
        # speed_variation = delta_speed * (size - Starfield.MIN_SIZE) / (Starfield.MAX_SIZE - Starfield.MIN_SIZE)
        speed = Starfield.MIN_SPEED + random.uniform(0., delta_speed)

        # set velocity
        velocity = Vector2()
        velocity.x, velocity.y = -1., 0.
        velocity = velocity * speed

        position = Vector2()
        position.x, position.y = x, y

        return _Star(position, velocity, random.uniform(0, Starfield.TWINKLE_DURATION), size)

    def update(self, elapsed):
        for star in self.stars:
            star.update(elapsed)

    def draw(self, screen):
        for star in self.stars:
            star.draw(screen)
