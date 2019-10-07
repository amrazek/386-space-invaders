from typing import NamedTuple
import pygame
from states.game_state import GameState
from session_stats import SessionStats
from animation import StaticAnimation
import config


class _Score(NamedTuple):
    name: str
    score: int


class HighScore(GameState):
    """Displays game high scores"""

    def __init__(self, input_state, game_stats: SessionStats):
        super().__init__(input_state)

        self.stats = game_stats
        self.font = pygame.font.SysFont(None, 48)
        self.high_scores = [_Score("abc", x * 100) for x in reversed(range(10))]

        # create high score text
        self.high_score_image = self.font.render("High Scores", True, config.text_color)
        self.high_score_image = self.high_score_image.convert_alpha(pygame.display.get_surface())
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.center = config.screen_rect.center
        self.high_score_rect.top = 50

        self.score_group = pygame.sprite.Group()
        self._update_high_score_list()

    def update(self, elapsed):
        pass

    def draw(self, screen):
        screen.fill(config.bg_color)
        screen.blit(self.high_score_image, self.high_score_rect)
        self.score_group.draw(screen)

    @property
    def finished(self):
        return False

    def get_next(self):
        raise NotImplementedError

    def _update_high_score_list(self):
        high_score_rect = pygame.Rect(0, 0, config.screen_width // 3, self.high_score_rect.height)
        high_score_rect.top = config.screen_height // 8
        high_score_rect.centerx = config.screen_width // 2
        self.score_group.empty()

        score_counter = 1

        rect = None

        for score in self.high_scores:
            image = self._render_high_score(config.screen_width // 2, score_counter, score)
            rect = rect or image.get_rect()
            rect.top = high_score_rect.bottom + 10 + (score_counter - 1) * (rect.height + 6)

            sprite = StaticAnimation(image)
            sprite.rect = rect.copy()
            sprite.rect.centerx = config.screen_rect.centerx
            self.score_group.add(sprite)
            score_counter += 1

    def _render_high_score(self, available_width, place, high_score: _Score):
        place_image = self.font.render(str(place), True, config.text_color)
        score_image = self.font.render(str(high_score.score), True, config.text_color)
        player_image = self.font.render(high_score.name, True, config.text_color)

        images = [place_image, score_image, player_image]
        offset = available_width // len(images)
        surf = pygame.Surface((available_width, max(i.get_height() for i in images)))
        surf = surf.convert_alpha(pygame.display.get_surface())
        surf.fill(color=(0, 255, 0, 0))

        r = place_image.get_rect()
        r.width = offset

        for i in range(len(images)):
            r.left = i * offset
            r.width = images[i].get_width()
            surf.blit(images[i], r)

        return surf


class EnterHighScore(GameState):
    """Allows player to enter a new high score"""
    def __init__(self, input_state, game_stats: SessionStats):
        super().__init__(input_state)

        self.stats = game_stats
        self.font = pygame.font.SysFont(None, 48)
        self.prompt_group = pygame.sprite.Group()

        new_high_score = self.font.render("New high score!", True, config.text_color)
        new_high_score = StaticAnimation(new_high_score)
        new_high_score.rect.centerx = config.screen_rect.centerx
        new_high_score.rect.top = 50
        self.prompt_group.add(new_high_score)

        self.entered_name_image = None
        self.entered_name_rect = None
        self.entered_name = ""

        # todo: is current score better than lowest high score?

        self._update_name_image()
        self.entered_name_rect.centerx = new_high_score.rect.centerx
        self.entered_name_rect.top = new_high_score.rect.bottom + 10

        self.done = False

    def update(self, elapsed):
        if self.done:
            return

        self.prompt_group.update(elapsed)

        # check for any new key inputs
        for key_code in self.input_state.key_codes:
            if key_code == pygame.K_BACKSPACE or key_code == pygame.K_KP_ENTER:
                self.entered_name = self.entered_name[:-1]
                self._update_name_image()
            elif key_code == pygame.K_RETURN:
                if len(self.entered_name) == 3:
                    print("accept this name: {}".format(self.entered_name))
                    self.done = True
                else:
                    print("name denied: need 3 letters")  # todo: error sound?
            elif str.isalnum(pygame.key.name(key_code)) and len(self.entered_name) < 3:
                letter = pygame.key.name(key_code)
                self.entered_name += letter
                self._update_name_image()

            the_key = pygame.key.name(key_code)

        self.input_state.key_codes.clear()

    def draw(self, screen):
        screen.fill(config.bg_color)
        self.prompt_group.draw(screen)
        screen.blit(self.entered_name_image, self.entered_name_rect)

    @property
    def finished(self):
        return self.done

    def get_next(self):
        return HighScore(self.input_state, self.stats)

    def _update_name_image(self):
        self.entered_name_image = self.font.render("Enter Name: " + self.entered_name, True, config.text_color)
        self.entered_name_rect = self.entered_name_rect or self.entered_name_image.get_rect()
