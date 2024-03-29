from pygame import Color
from pygame import Rect
from typing import NamedTuple


class BulletStats(NamedTuple):
    width: int
    height: int
    speed: float
    color: Color

    @property
    def size(self):
        return self.width, self.height


class AlienStats(NamedTuple):
    sprite_name: str
    points: int


# Screen settings
screen_width = 1000
screen_height = 600
bg_color = (0, 0, 0)
text_color = (255, 255, 255)
green_color = (0, 240, 0)
screen_rect = Rect(0, 0, screen_width, screen_height)
transparent_color = (255, 0, 255)

# Atlas
atlas = None

# ship settings
ship_limit = 3  # player has this many extra lives. Next death after this will result in game over

# bullet settings
default_player_bullet = BulletStats(
    width=30,
    height=15,
    speed=350.0,
    color=Color('white'))

bullets_per_second = 7.5

# alien bullet settings
default_alien_bullet = BulletStats(
    width=6,
    height=12,
    speed=-50.0,
    color=Color('green'))

# Alien settings
fleet_drop_speed = 5

alien_stats = [
    AlienStats(sprite_name="alien1", points=10),
    AlienStats(sprite_name="alien2", points=15),
    AlienStats(sprite_name="alien3", points=20)
]

ufo_stats = AlienStats(sprite_name="ufo", points=500)  # ufo worth **up to** this many points (random)
ufo_min_delay = 15.  # ufo won't show up again for at least this many seconds
ufo_max_delay = 50.  # a ufo will definitely appear at worst, every this many seconds

fleet_shots_per_second = 0.5    # base rate: completely healthy fleet fires this many bullets per second
fleet_max_shots_per_second = 2  # theoretical rate: a destroyed fleet would fire this many times per second


# Bunker settings
bunker_tile_size = 32
bunker_count = 3
bunker_offset_from_ship = 1  # multiplier to ship height to position bunkers: this is number of ship lengths "above"
bunker_color = (0, 255, 0)
bunker_fragment_health = 3  # how many hits a bunker can take

# How quickly the game speeds up
speedup_scale = 1.1

# How quickly alien point values increase
score_scale = 1.5
