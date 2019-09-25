class GameState:
    """Base class for all game states"""
    def __init__(self, input_state):
        self.input_state = input_state

    def update(self, elapsed):
        pass

    def draw(self, screen):
        pass

    @property
    def finished(self):
        return True

    def get_next(self):
        return None