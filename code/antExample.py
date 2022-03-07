"""
class antExample

this is the most basic version of ants
"""
from math import sqrt
from random import randint
from pyAmakCore.classes.agent import Agent
from color import Color

import paho.mqtt.client as mqtt
import json

client = mqtt.Client()
client.connect('192.168.43.200', 1883, 60)


class AntExampleV1(Agent):
    int_to_color = {
        0: Color.BLUE,
        1: Color.BLACK,
        2: Color.RED,
        3: Color.YELLOW,
        4: Color.GREEN
    }

    color_to_int = {
        Color.BLUE: 0,
        Color.BLACK: 1,
        Color.RED: 2,
        Color.YELLOW: 3,
        Color.GREEN: 4
    }

    def __init__(self,
                 amas: 'antHillExample',
                 startX: float,
                 startY: float
                 ) -> None:
        super().__init__(amas)
        self._dx = startX
        self._dy = startY
        self._color = Color.BLACK
        self.majority_color = Color.BLACK

    def get_color(self):
        return self._color

    def get_dx(self):
        return self._dx

    def get_dy(self):
        return self._dy

    def make_random_move(self):
        self._dx += (randint(-1, 1) * self.get_environment().coef_deplacement)
        self._dy += (randint(-1, 1) * self.get_environment().coef_deplacement)

        if self._dx < self.get_environment().xmin:
            self._dx = self.get_environment().xmin

        if self._dx > self.get_environment().xmax:
            self._dx = self.get_environment().xmax

        if self._dy < self.get_environment().ymin:
            self._dy = self.get_environment().ymin

        if self._dy > self.get_environment().ymax:
            self._dy = self.get_environment().ymax

        self.publish_state()

    def on_perceive(self) -> None:
        self.reset_neighbour()
        for agent in self.get_amas().get_agents():
            length = sqrt(pow(self._dx - agent.get_dx(), 2) +
                          pow(self._dy - agent.get_dy(), 2))
            if length < self.get_environment().field_of_view and self != agent:
                self.add_neighbour(agent)
        self.find_the_majority_color()

        self.publish_state()

    def on_act(self) -> None:
        # couleur
        if self.majority_color != self._color:
            self._color = self.majority_color
        elif randint(1, 1000) <= 4:
            self._color = AntExampleV1.int_to_color.get(randint(0, 4))

        # déplacement
        self.make_random_move()

        self.publish_state()

    def find_the_majority_color(self) -> Color:
        couleurs_voisin = [0, 0, 0, 0, 0]
        for agent in self.get_neighbour():
            couleurs_voisin[AntExampleV1.color_to_int.get(
                agent.get_color())] += 1

        self.majority_color = AntExampleV1.int_to_color.get(
            couleurs_voisin.index(max(couleurs_voisin)))

    def publish_state(self):
        for index, agent in enumerate(self.get_amas().get_agents()):
            client.publish(f'topic/agent_state/{index+1}',
                           json.dumps({'Agent': index+1, 'x': agent.get_dx(), 'y': agent.get_dy()}))
