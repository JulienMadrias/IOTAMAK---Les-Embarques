from pyAmakCore.classes.agent import Agent

class SimpleAgent(Agent):
    def __init__(self, amas: 'Amas') -> None:
        super().__init__(amas)

    def on_perceive(self) -> None:
        pass

    def on_decide(self) -> None:
        pass

    def on_act(self) -> None:
        pass