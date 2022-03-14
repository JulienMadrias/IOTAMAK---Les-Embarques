from pyAmakCore.classes.amas import Amas

class SimpleAmas(Amas):
    def __init__(self, env, execution_policy):
        super().__init__(env, execution_policy)

    def on_initialization(self) -> None:
        return super().on_initialization()

    def on_initial_agents_creation(self) -> None:
        return super().on_initial_agents_creation()
    