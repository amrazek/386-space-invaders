import pygame
import sprite_atlas
from states.run_game import RunGame
from states.input_state import InputState
from timer import Timer
import config


def run_game():
    # initialize PyGame and create screen surface
    pygame.init()

    screen = pygame.display.set_mode((config.screen_width, config.screen_height))
    pygame.display.set_caption("Space Invaders")

    # load all animated sprite images needed for the game
    sprite_atlas.load_atlas()

    # init game
    input_state = InputState()
    game_state = RunGame(input_state)

    # start main loop for the game
    timer = Timer()

    while not input_state.quit and game_state is not None:
        input_state.do_events()
        game_state.update(timer.elapsed)
        game_state.draw(screen)
        pygame.display.flip()

        timer.update()

        if game_state.finished:
            game_state = game_state.get_next()


run_game()
