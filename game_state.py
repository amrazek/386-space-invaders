from settings import Settings
from ship import Ship
from alien import Alien
from bullet import Bullet
from input_state import InputState


class GameState:
    def __init__(self, input_state):
        self.input_state = input_state

    def update(self, elapsed):
        pass

    def render(self, screen):
        pass

    @staticmethod
    def create_initial(input_state):
        return PlayGame(input_state)


class PlayGame(GameState):
    """Manages actual game play, until the player loses."""
    def __init__(self, input_state):
        super().__init__(input_state)
        self.ai_settings = Settings()
        self.ship = Ship(self.ai_settings)

    def update(self, elapsed):
        self.ship.update(self.input_state, elapsed)

    def render(self, screen):
        screen.fill(color=(0, 0, 50))
        screen.blit(self.ship.image, self.ship.rect)
