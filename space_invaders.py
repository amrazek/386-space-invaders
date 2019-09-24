import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
import game_functions as gf
import sprite_atlas
from game_state import GameState, PlayGame
from input_state import InputState
import config


def run_game():
    # initialize PyGame and create screen surface
    pygame.init()
    #ai_settings = Settings()
    screen = pygame.display.set_mode((config.screen_width, config.screen_height))

    pygame.display.set_caption("Space Invaders")

    # load all animated sprite images needed for the game
    sprite_atlas.load_atlas()

    # init game
    input_state = InputState()
    game_state = GameState.create_initial(input_state)

    # Make the play button
    #play_button = Button(screen, "Play")

    # Create an instance to store game statistics and create a scoreboard
    #stats = GameStats(ai_settings)
    #sb = Scoreboard(ai_settings, screen, stats)

    # Make a ship, a group of bullets, and a group of aliens
    #ship = Ship(ai_settings, screen)
    #bullets = Group()
    #aliens = Group()

    # Create the fleet of aliens
    #gf.create_fleet(ai_settings, screen, ship, aliens)

    # start main loop for the game
    elapsed = 0.0
    last_tick = pygame.time.get_ticks()

    while not input_state.quit:
        input_state.do_events()
        game_state.update(elapsed)
        game_state.render(screen)
        pygame.display.flip()

        new_tick = pygame.time.get_ticks()
        elapsed = (new_tick - last_tick) / 1000.0
        last_tick = new_tick

        # gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)
        #
        # if stats.game_active:
        #     ship.update()
        #     gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
        #     gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets)
        #
        # gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)


run_game()
