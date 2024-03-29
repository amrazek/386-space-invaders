import pygame
from pygame.sprite import Group
import config
from .game_state import GameState
from states.ready import Ready
from .high_score import HighScore
from animation import StaticAnimation
from starfield import Starfield
import sounds


class Menu(GameState):
    TitleSize = 64
    MenuItemSize = 32
    MenuItemSpacing = 16

    def __init__(self, input_state, starfield=None):
        super().__init__(input_state)
        self.font = pygame.font.SysFont(None, Menu.TitleSize)
        self.starfield = starfield or Starfield()
        self.title = Group()
        # create "Space Invaders" logo

        # green "SPACE"
        space_title = StaticAnimation(self.font.render("SPACE", True, config.green_color))
        space_title.rect.centerx = config.screen_rect.centerx
        space_title.rect.centery = config.screen_height // 8

        # white "INVADERS"
        self.font = pygame.font.SysFont(None, Menu.TitleSize // 2)
        invaders_title = StaticAnimation(self.font.render("INVADERS", True, pygame.Color('white')))
        invaders_title.rect.left = space_title.rect.left + space_title.rect.width // 8
        invaders_title.rect.top = space_title.rect.bottom + 10

        self.title.add(space_title, invaders_title)

        last_y = config.screen_height - config.screen_height // 3
        self.options = Group()
        self.font = pygame.font.SysFont(None, Menu.MenuItemSize)

        # create options
        for option in [("Play Space Invaders", self._play_game),
                       ("High Scores", self._view_high_scores),
                       ("Quit", self._quit)]:
            option_sprite = StaticAnimation(self.font.render(option[0], True, config.text_color))
            option_sprite.callback = option[1]

            option_sprite.rect.centerx = config.screen_width // 2
            option_sprite.rect.top = last_y

            last_y = option_sprite.rect.bottom + Menu.MenuItemSpacing
            self.options.add(option_sprite)

        # create a small sprite to use as menu item selector
        left_selector = config.atlas.load_static("selector")

        # need to flip the arrow...
        right_selector = StaticAnimation(pygame.transform.flip(left_selector.image, True, False))
        right_selector.rect.left = config.screen_width

        self.selectors = Group(left_selector, right_selector)

        # point values for aliens
        self.aliens = Group()

        y_pos = invaders_title.rect.bottom + 50

        for alien_stats in config.alien_stats:
            alien = config.atlas.load_animation(alien_stats.sprite_name).frames[0]
            spr = self._create_point_sprite(alien, alien_stats.points, y_pos)
            self.aliens.add(spr)
            y_pos = spr.rect.bottom + 10

        ufo = config.atlas.load_animation("ufo").frames[0]
        spr = self._create_point_sprite(ufo, "???", y_pos)

        self.aliens.add(spr)

        # finish creating state values
        self.next_state = None
        self._set_selected(0)

        pygame.mouse.set_visible(True)
        sounds.play_music(sounds.menu_music_name)

    def update(self, elapsed):
        self.starfield.update(elapsed)
        self.options.update(elapsed)
        self.selectors.update(elapsed)
        self.aliens.update(elapsed)

        # handle selected item
        if not self._handle_mouse_clicks():
            self._handle_arrow_keys()

    def draw(self, screen):
        screen.fill(config.bg_color)

        self.starfield.draw(screen)
        self.title.draw(screen)

        self.aliens.draw(screen)
        self.options.draw(screen)
        self.selectors.draw(screen)

    @property
    def finished(self):
        return self.next_state is not None

    def get_next(self):
        return self.next_state

    def _play_game(self):
        self.next_state = Ready(self.input_state)

    def _view_high_scores(self):
        self.next_state = HighScore(self.input_state, self.starfield)

    def _quit(self):
        self.input_state.quit = True

    def _handle_arrow_keys(self):
        for key_code in self.input_state.key_codes:
            if key_code == pygame.K_RETURN or key_code == pygame.K_KP_ENTER:
                self.options.sprites()[self.selected_index].callback()

        if self.input_state.up and self.input_state.down:
            return  # both up and down at once, just do nothing

        if self.input_state.up:
            self._set_selected(self.selected_index - 1)
            self.input_state.up = False  # don't allow repeating
        elif self.input_state.down:
            self._set_selected(self.selected_index + 1)
            self.input_state.down = False

    def _handle_mouse_clicks(self):
        idx = 0

        for option in self.options.sprites():
            if option.rect.collidepoint(self.input_state.mouse_pos):
                # highlight this option
                self._set_selected(idx)

                if self.input_state.left_down:
                    option.callback()
                    self.input_state.left_down = False

                return True

            idx += 1

    def _set_selected(self, idx):
        while idx < 0:
            idx += len(self.options.sprites())

        idx = idx % len(self.options.sprites())

        if hasattr(self, "selected_index") and idx != self.selected_index:
            sounds.play("select")

        self.selected_index = idx

        # align selectors to current option
        for selector in self.selectors.sprites():
            option_rect = self.options.sprites()[idx].rect

            selector.rect.centery = option_rect.centery

            if selector.rect.x < config.screen_width // 2:
                # must be left selector
                selector.rect.right = option_rect.left - 6
            else:
                # right selector
                selector.rect.left = option_rect.right + 6

    def _create_point_sprite(self, alien_surf, point_value, top_coord):
        point_value = self.font.render("{} Points".format(point_value), True, config.text_color)
        alien_rect = alien_surf.get_rect()

        surf = pygame.Surface((alien_rect.width + point_value.get_width() + 20,
                               max(alien_rect.height, point_value.get_height())))
        surf = surf.convert_alpha(pygame.display.get_surface())  # want 32 bit surface for per-pixel alpha
        surf.fill((0, 0, 0, 0))  # fill with transparent, note no color key

        # center alien rect vertically
        alien_rect.centery = surf.get_height() // 2
        surf.blit(alien_surf, alien_rect)

        r = point_value.get_rect()
        r.left = alien_rect.width + 20
        r.centery = alien_rect.centery
        surf.blit(point_value, r)

        sprite = StaticAnimation(surf)

        sprite.rect.top = top_coord
        sprite.rect.centerx = config.screen_rect.centerx

        return sprite
