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

        self.font = pygame.font.SysFont(None, 48)
        self.high_scores = [_Score("abc", x * 100) for x in reversed(range(10))]

        # create high score text
        self.high_score_image = self.font.render("High Scores", True, config.text_color)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.center = config.screen_rect.center
        self.high_score_rect.top = 50

        self.score_group = pygame.sprite.Group()

        self._update_high_score_list()

    def update(self, elapsed):
        pass

    def draw(self, screen):
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
        surf = pygame.Surface((available_width, max(i.get_height() for i in images))).convert_alpha(
            pygame.display.get_surface())
        surf.fill(color=(0, 255, 0, 128))

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

    def update(self, elapsed):
        raise NotImplementedError

    def draw(self, screen):
        raise NotImplementedError

    @property
    def finished(self):
        raise NotImplementedError

    def get_next(self):
        raise NotImplementedError
