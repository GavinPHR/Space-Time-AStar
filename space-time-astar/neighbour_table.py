#!/usr/bin/env python3
'''
Author: Haoran Peng
Email: gavinsweden@gmail.com
'''
import numpy as np

class NeighbourTable:

    def __init__(self, grid: np.ndarray):
        dimy, dimx = len(grid), len(grid[0])
        table = dict()
        for i in range(dimy):
            for j in range(dimx):
                neighbours = []
                for dx, dy in (1, 0), (-1, 0), (0, 1), (0, -1):
                    y, x = i + dy, j + dx,
                    if x >= 0 and x < dimx and y >= 0 and y < dimy:
                        neighbours.append([y, x])
                table[self.hash(grid[i][j])] = np.array(neighbours)
        self.table = table

    def lookup(self, position: np.ndarray) -> np.ndarray:
        return self.table[self.hash(position)]

    @staticmethod
    def hash(grid_pos: np.ndarray) -> int:
        concat = str(grid_pos[0]) + str(grid_pos[1])
        return int(concat)