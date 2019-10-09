import os
import pygame
from states.menu import Menu
from states.input_state import InputState
from timer import game_timer
from sprite_atlas import load_atlas
import config
import sounds


def run_game():
    if pygame.mixer:
        pygame.mixer.pre_init(22050, -16, 2, 1024)

    # initialize PyGame and create screen surface
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()

    screen = pygame.display.set_mode((config.screen_width, config.screen_height))
    pygame.display.set_caption("Space Invaders")

    # load all animated sprite images needed for the game
    load_atlas()

    # load sounds
    sounds.load_sounds()

    # init game
    input_state = InputState()
    game_state = Menu(input_state)

    # start main loop for the game
    while not input_state.quit and game_state is not None:
        input_state.do_events()
        game_state.update(game_timer.elapsed)
        game_state.draw(screen)
        pygame.display.flip()

        game_timer.update()

        if game_state.finished:
            game_state = game_state.get_next()
            game_timer.reset()


run_game()
