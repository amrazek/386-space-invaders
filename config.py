from pygame import Rect

# Screen settings
screen_width = 1000
screen_height = 600
bg_color = (0, 0, 0)
text_color = (255, 255, 255)
screen_rect = Rect(0, 0, screen_width, screen_height)

# ship settings
ship_limit = 3

# bullet settings
bullet_width = 3000
bullet_height = 15
bullet_color = 60, 60, 60
bullets_allowed = 3

# Alien settings
fleet_drop_speed = 30
initial_point_value = 50

# How quickly the game speeds up
speedup_scale = 1.1

# How quickly alien point values increase
score_scale = 1.5
