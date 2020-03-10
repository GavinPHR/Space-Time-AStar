#!/usr/bin/env python3
'''
Author: Haoran Peng
Email: gavinsweden@gmail.com
'''
from typing import Tuple, List, Dict
import numpy as np
from scipy.spatial import KDTree
from copy import deepcopy


# static obstacles must include the boundary
# kd-tree faster with more obst (>30), slow if less: kd for static, brute for dynamic
# indexing consisten with opencv
class Planner:

    def __init__(self, grid_size: int,
                       robot_radius: int,
                       start: Tuple[int, int],
                       goal: Tuple[int, int],
                       static_obstacles: List[Tuple[int, int]],
                       dynamic_obstacles: Dict[int, List[Tuple[int, int]]]):
        self.grid_size = grid_size
        self.robot_radius = robot_radius
        self.start = np.array(start)
        self.goal = np.array(goal)
        np_static_obstacles = np.array(static_obstacles)
        self.static_obstacles = KDTree(np_static_obstacles)
        self.dynamic_obstacles = dict((k, np.array(v)) for k, v in dynamic_obstacles.items())

        self.minx, self.maxx, self.miny, self.maxy = self.calculate_boundaries(np_static_obstacles)
        self.grid = self.make_grid(grid_size, self.minx, self.maxx, self.miny, self.maxy)


    @staticmethod
    def calculate_boundaries(static_obstacles: np.ndarray) -> Tuple[int, int, int, int]:
        min_ = np.min(static_obstacles, axis=0)
        max_ = np.max(static_obstacles, axis=0)
        return min_[0], max_[0], min_[1], max_[1]

    @staticmethod
    def make_grid(grid_size: int, minx: int, maxx: int, miny: int, maxy: int) -> np.ndarray:
        # Calculate the size of the sides
        x_size = (maxx - minx)//grid_size
        y_size = (maxy - miny)//grid_size
        # Initialize the grid, assuming grid is 2D
        grid = np.zeros([y_size, x_size, 2])
        # Fill the grid in
        y = miny - grid_size//2
        for i in range(y_size):
            y += grid_size
            x = minx - grid_size//2
            for j in range(x_size):
                x += grid_size
                grid[i][j] = np.array([y, x])
        return grid

    

if __name__ == '__main__':
    grid_size = 1
    robot_radius = 2
    start = (3, 10)
    goal = (15, 20)
    static_obstacles = [(5, 15), (10, 20)]
    dynamic_obstacles = {0: [(5, 16)], 1: [(5, 17)], 2: [(5, 18), (11, 20)]}
    planner = Planner(grid_size, robot_radius, start, goal, static_obstacles, dynamic_obstacles)
    print(planner.grid)