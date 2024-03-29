import os
from typing import NamedTuple
import pygame
from states.game_state import GameState
from session_stats import SessionStats
from animation import StaticAnimation
from starfield import Starfield
import config
import sounds


class _Score(NamedTuple):
    name: str
    score: int


class HighScore(GameState):
    """Displays game high scores"""
    HIGH_SCORE_FILE = 'high_scores.txt'

    def __init__(self, input_state, starfield=None):
        super().__init__(input_state)

        self.font = pygame.font.SysFont(None, 48)
        self.high_scores = []
        self.starfield = starfield or Starfield()

        self._load_high_scores()

        # create high score text
        self.high_score_image = self.font.render("High Scores", True, config.text_color)
        self.high_score_image = self.high_score_image.convert_alpha(pygame.display.get_surface())
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.center = config.screen_rect.center
        self.high_score_rect.top = 50

        self.score_group = pygame.sprite.Group()
        self._update_high_score_list()

        self.done = False

    def update(self, elapsed):
        if any(self.input_state.key_codes) or self.input_state.left_down or self.input_state.quit:
            self.done = True
            self.input_state.key_codes.clear()
            self.input_state.left_down = False
            self.input_state.quit = False  # escape to main menu rather than just exiting

        self.starfield.update(elapsed)

    def draw(self, screen):
        screen.fill(config.bg_color)
        self.starfield.draw(screen)
        screen.blit(self.high_score_image, self.high_score_rect)
        self.score_group.draw(screen)

    @property
    def finished(self):
        return self.done

    def get_next(self):
        import states.menu
        return states.menu.Menu(self.input_state, self.starfield)

    def _update_high_score_list(self):
        high_score_rect = pygame.Rect(0, 0, config.screen_width // 3, self.high_score_rect.height)
        high_score_rect.top = config.screen_height // 8
        high_score_rect.centerx = config.screen_width // 2
        self.score_group.empty()

        # pad score list out to 10, if necessary
        padded_list = [_Score("???", -1) for _ in range(10 - len(self.high_scores))]
        self.high_scores += padded_list

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
        score_image = self.font.render(str(high_score.score) if high_score.score > 0 else "???",
                                       True, config.text_color)
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

    def is_new_high_score(self, score):
        return len(self.high_scores) < 10 or any(score > hs.score for hs in self.high_scores) and score > 0

    def insert_high_score(self, name, score):
        assert self.is_new_high_score(score)

        self.high_scores.append(_Score(name, score))
        self.high_scores = self._sort_scores(self.high_scores)
        self._update_high_score_list()

    @staticmethod
    def _sort_scores(scores):
        return sorted(scores, key=lambda hs: hs.score, reverse=True)[:10]  # keep top 10 scores

    def _load_high_scores(self):
        """Loads high scores from disk"""
        scores = []

        path = os.path.join('data', HighScore.HIGH_SCORE_FILE)
        if os.path.exists(path) and os.path.isfile(path):
            file = open(path, 'rt')

            for entry in file:
                split = entry.split(',')

                if len(split) == 2 and split[1].strip().isnumeric():
                    scores.append(_Score(split[0], int(split[1])))

            file.close()

        # sort greatest to least, and max of 10
        self.high_scores = self._sort_scores(scores)

    def save_high_scores(self):
        """Saves high scores to disk"""
        if not os.path.exists('data'):
            os.mkdir('data')

        path = os.path.join('data', HighScore.HIGH_SCORE_FILE)
        file = open(path, 'wt')

        for score in self.high_scores:
            file.write("{},{}\n".format(score.name, str(score.score)))

        file.close()


class EnterHighScore(GameState):
    MAX_LEN = 12

    """Allows player to enter a new high score"""
    def __init__(self, input_state, game_stats: SessionStats, starfield=None):
        super().__init__(input_state)

        self.stats = game_stats
        self.font = pygame.font.SysFont(None, 48)
        self.prompt_group = pygame.sprite.Group()
        self.high_score_state = HighScore(self.input_state)
        self.starfield = starfield or Starfield()

        new_high_score = self.font.render("New high score!", True, config.text_color)
        new_high_score = StaticAnimation(new_high_score)
        new_high_score.rect.centerx = config.screen_rect.centerx
        new_high_score.rect.top = 50
        self.prompt_group.add(new_high_score)

        self.entered_name_image = None
        self.entered_name_rect = None
        self.entered_name = ""

        self._update_name_image()
        self.entered_name_rect.centerx = new_high_score.rect.centerx
        self.entered_name_rect.top = new_high_score.rect.bottom + 10

        # if this is not a new high score, this state will just transition directly to displaying the
        # high score list
        self.done = not self.high_score_state.is_new_high_score(game_stats.score)

    def update(self, elapsed):
        if self.done:
            return

        self.prompt_group.update(elapsed)
        self.starfield.update(elapsed)

        # check for any new key inputs
        for key_code in self.input_state.key_codes:
            if key_code == pygame.K_BACKSPACE:
                self.entered_name = self.entered_name[:-1]
                self._update_name_image()
                sounds.play("back")
            elif key_code == pygame.K_RETURN or key_code == pygame.K_KP_ENTER:
                if len(self.entered_name) > 0:
                    self.done = True
                    self.high_score_state.insert_high_score(self.entered_name, self.stats.score)
                    self.high_score_state.save_high_scores()
                    sounds.play("accept")
                else:
                    sounds.play("wrong")
            elif len(self.entered_name) < EnterHighScore.MAX_LEN and self._is_accepted_key_code(key_code):
                letter = chr(key_code)
                self.entered_name += letter
                self._update_name_image()
                sounds.play("type")

        # allow player to skip by pressing escape
        if self.input_state.quit:
            self.done = True
            self.input_state.quit = False

    def draw(self, screen):
        screen.fill(config.bg_color)
        self.starfield.draw(screen)
        self.prompt_group.draw(screen)
        screen.blit(self.entered_name_image, self.entered_name_rect)

    @staticmethod
    def _is_accepted_key_code(kc):
        kc = chr(kc)
        return 'a' <= kc <= 'z' or 'A' <= kc <= 'Z' or '0' <= kc <= '9'

    @property
    def finished(self):
        return self.done

    def get_next(self):
        return self.high_score_state

    def _update_name_image(self):
        self.entered_name_image = self.font.render("Enter Name: " + self.entered_name.ljust(EnterHighScore.MAX_LEN, '_')
                                                   , True,
                                                   config.text_color)
        self.entered_name_rect = self.entered_name_rect or self.entered_name_image.get_rect()
