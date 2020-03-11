#!/usr/bin/env python3
'''
Author: Haoran Peng
Email: gavinsweden@gmail.com
'''
import numpy as np

class NeighbourTable:
    #             Current  Right    Left    Down     Up
    # directions = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]
    # Uncomment the line below for 9 directions, this might slow things down a lot
    directions = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]

    def __init__(self, grid: np.ndarray):
        dimy, dimx = len(grid), len(grid[0])
        table = dict()
        for i in range(dimy):
            for j in range(dimx):
                neighbours = []
                for dx, dy in self.directions:
                    y, x = i + dy, j + dx,
                    if x >= 0 and x < dimx and y >= 0 and y < dimy:
                        neighbours.append(grid[y][x])
                table[self.hash(grid[i][j])] = np.array(neighbours)
        self.table = table

    def lookup(self, position: np.ndarray) -> np.ndarray:
        return self.table[self.hash(position)]

    @staticmethod
    def hash(grid_pos: np.ndarray) -> int:
        concat = str(grid_pos[0]) + str(grid_pos[1])
        return concat

if __name__ == '__main__':
    grid = np.array([[[15,5],[15,6],[15,7],[15,8],[15,9]],
            [[16,5],[16,6],[16,7],[16,8],[16,9]],
            [[17,5],[17,6],[17,7],[17,8],[17,9]],
            [[18,5],[18,6],[18,7],[18,8],[18,9]],
            [[19,5],[19,6],[19,7],[19,8],[19,9]]])
    nt = NeighbourTable(grid)
    print(nt.lookup(np.array([16,7])))