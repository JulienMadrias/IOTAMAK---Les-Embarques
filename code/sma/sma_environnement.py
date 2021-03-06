from pyAmakCore.classes.environment import Environment
from fork import Fork


class SimpleEnvironment(Environment):
    def __init__(self):
        self._forks = []
        super().__init__()

    def on_initialization(self):
        for _ in range(10):
            self._forks.append(Fork())

    def get_forks(self):
        """
        Return forks
        """
        return self._forks
