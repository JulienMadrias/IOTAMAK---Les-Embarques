from pyAmakCore.classes.amas import Amas
from sma_agent import SimpleAgent
from sma_environnement import SimpleEnvironment
import numpy as np
import pickle


class SimpleAmas(Amas):
    def __init__(self, execution_policy):
        super().__init__(SimpleEnvironment(), execution_policy)

    def on_initialization(self) -> None:
        return super().on_initialization()

    def on_initial_agents_creation(self):
        ps = []
        for i in range(9):
            ps.append(SimpleAgent(i, self, self.get_environment().get_forks()[i],
                                  self.get_environment().get_forks()[i + 1]))

        ps.append(
            SimpleAgent(9, self, self.get_environment().get_forks()[9], self.get_environment().get_forks()[0]))

        for j in range(len(ps) - 1):
            ps[j + 1].add_neighbour(ps[j])
            ps[j].add_neighbour(ps[j + 1])

        ps[0].add_neighbour(ps[len(ps) - 1])
        ps[len(ps) - 1].add_neighbour(ps[0])
        self.add_agents(ps)

        # distribute agents
        # if we have 10 agents and 2 connected raspberry, we'll have 5 on each
        # let's assume we have 2 rasp
        nb_raspberry = 2

        to_send = [list(elt) for elt in np.array_split(ps, nb_raspberry)]

        # serialisation
        # for i, elt in enumerate(to_send):
        #     with open(f'rasp_{i}', 'wb') as f:
        #         pickle.dump(elt, f)

        # deserialisation
        with open('rasp_0', 'rb') as f:
            r = pickle.load(f)
            for el in r:
                print(el._SimpleAgent__state)
