import pygame
import sprite_atlas
from states.run_game import RunGame
from input_state import InputState
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
    elapsed = 0.0
    last_tick = pygame.time.get_ticks()

    while not input_state.quit and not game_state is None:
        input_state.do_events()
        game_state.update(elapsed)
        game_state.draw(screen)
        pygame.display.flip()

        new_tick = pygame.time.get_ticks()
        elapsed = (new_tick - last_tick) / 1000.0
        last_tick = new_tick

        if game_state.finished:
            game_state = game_state.get_next()


run_game()
