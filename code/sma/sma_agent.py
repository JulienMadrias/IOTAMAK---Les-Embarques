from pyAmakCore.classes.agent import Agent
from state import State
from random import randint


class SimpleAgent(Agent):
    def __init__(self, id2, amas, left, right) -> None:
        super().__init__(amas)
        self.__state = State.THINK
        self.__hungerDuration = 0
        self.__eatenPastas = 0
        self.__id2 = id2
        self.__left = left
        self.__right = right

    def id(self):
        return self.__id2

    def on_perceive(self) -> None:
        pass

    def on_decide(self) -> None:
        pass

    def on_act(self) -> None:
        pass

    def compute_criticality(self):
        if self.__state == State.HUNGRY:
            return self.__hungerDuration
        return -1

    def get_state(self):
        return self.__state

    def set_state(self, state):
        self.__state = state

    def get_Left_Fork(self):
        if self.__left is not None:
            return self.__left

    def get_Right_Fork(self):
        if self.__right is not None:
            return self.__right
