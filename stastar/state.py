#!/usr/bin/env python3
'''
Author: Haoran Peng
Email: gavinsweden@gmail.com
'''
import numpy as np

class State:

    def __init__(self, pos: np.ndarray, time: int, g_score: int, h_score: int):
        self.pos = pos
        self.time = time
        self.g_score = g_score
        self.f_score = g_score + h_score

    def __hash__(self) -> int:
        concat = str(self.pos[0]) + str(self.pos[1]) + '0' + str(self.time)
        return int(concat)

    def pos_equal_to(self, pos: np.ndarray) -> bool:
        return np.array_equal(self.pos, pos)

    def __lt__(self, other: 'State') -> bool:
        return self.f_score < other.f_score

    def __eq__(self, other: 'State') -> bool:
        return self.__hash__() == other.__hash__()

    def __str__(self):
        return 'State(pos=[' + str(self.pos[0]) + ', ' + str(self.pos[1]) + '], ' \
               + 'time=' + str(self.time) + ', fscore=' + str(self.f_score) + ')'

    def __repr__(self):
        return self.__str__()
