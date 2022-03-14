from pyAmakCore.classes.environment import Environment

class SimpleEnvironment(Environment):
    def __init__(self, seed_int: int = None) -> None:
        super().__init__()