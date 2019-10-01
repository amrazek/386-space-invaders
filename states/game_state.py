from abc import abstractmethod


class GameState:
    """Base class for all game states"""
    def __init__(self, input_state):
        self.input_state = input_state

    @abstractmethod
    def update(self, elapsed):
        raise NotImplementedError

    @abstractmethod
    def draw(self, screen):
        raise NotImplementedError

    @property
    @abstractmethod
    def finished(self):
        raise NotImplementedError

    @abstractmethod
    def get_next(self):
        raise NotImplementedError
