from agent import Agent
from random import randint
from state import State


class SimpleAgent(Agent):
    def __init__(self, id2, left, right) -> None:
        super().__init__(id2)
        self.__state = State.THINK
        self.__hungerDuration = 0
        self.__eatenPastas = 0
        self.__id2 = id2
        self.__left = left
        self.__right = right

    def id(self):
        return self.__id2

    def get_hunger_duration(self):
        return self.__hungerDuration

    def get_eaten_pastas(self):
        return self.__eatenPastas

    def on_perceive(self) -> None:
        print('')

    def on_decide(self) -> None:
        print('')

    def on_act(self):
        next_state = self.__state
        if self.__state == State.EATING:
            self.__eatenPastas += 1
            if randint(0, 101) > 50:
                self.__left.release
                self.__right.release
                next_state = State.THINK
        else:
            if self.__state == State.HUNGRY:
                self.__hungerDuration += 1
                if self.get_most_critical_neighbor(True) == self:
                    self.__left.try_take(self)
                    self.__right.try_take(self)
                    if self.__left.owned(self) and self.__right.owned(self):
                        next_state = State.EATING
                else:
                    self.__left.release(self)
                    self.__right.release(self)
            else:
                if self.__state == State.THINK:
                    if randint(0, 101) > 50:
                        self.__hungerDuration = 0
                        next_state = State.HUNGRY
        self.__state = next_state

    def compute_criticality(self):
        if self.__state == State.HUNGRY:
            return self.__hungerDuration
        return -1

    def get_state(self):
        return self.__state.value

    def get_Left_Fork(self):
        if self.__left is not None:
            return self.__left

    def get_Right_Fork(self):
        if self.__right is not None:
            return self.__right

    def subscribe(self, agent_id, client):
        client.subscribe("topic/sma/agent_"+str(agent_id))

    def unsubscribe(self, agent_id, client):
        client.unsubscribe("topic/sma/agent_"+str(agent_id))
