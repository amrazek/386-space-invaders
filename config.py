from pygame import Color
from pygame import Rect
from typing import NamedTuple
from sprite_atlas import load_atlas


class BulletStats(NamedTuple):
    width: int
    height: int
    speed: float
    color: Color

    @property
    def size(self):
        return self.width, self.height


# Screen settings
screen_width = 1000
screen_height = 600
bg_color = (0, 0, 0)
text_color = (255, 255, 255)
screen_rect = Rect(0, 0, screen_width, screen_height)
transparent_color = (255, 0, 255)

# Atlas
atlas = None

# ship settings
ship_limit = 3

# bullet settings
default_player_bullet = BulletStats(
    width=30,
    height=15,
    speed=300.0,
    color=Color('white'))

bullets_allowed = 3

# alien bullet settings
default_alien_bullet = BulletStats(
    width=6,
    height=12,
    speed=-60.0,
    color=Color(0, 255, 0))

# Alien settings
fleet_drop_speed = 0
initial_point_value = 50

# Bunker settings
bunker_tile_size = 32
bunker_count = 3
bunker_offset_from_ship = 1  # multiplier to ship height
bunker_color = (0, 255, 0)
bunker_fragment_health = 3

# How quickly the game speeds up
speedup_scale = 1.1

# How quickly alien point values increase
score_scale = 1.5
