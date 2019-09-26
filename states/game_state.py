class GameState:
    """Base class for all game states"""
    def __init__(self, input_state):
        self.input_state = input_state

    def update(self, elapsed):
        raise NotImplementedError

    def draw(self, screen):
        raise NotImplementedError

    @property
    def finished(self):
        raise NotImplementedError

    def get_next(self):
        raise NotImplementedError
