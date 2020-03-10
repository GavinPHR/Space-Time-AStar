#!/usr/bin/env python3
'''
Author: Haoran Peng
Email: gavinsweden@gmail.com
'''
from typing import Tuple, List, Dict
import numpy as np
from scipy.spatial import KDTree

from neighbour_table import NeighbourTable
from grid import Grid
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

        # Make the grid according to the grid size
        self.grid = Grid(grid_size, np_static_obstacles)
        # Make a lookup table for looking up neighbours of a grid
        self.neighbour_table = NeighbourTable(self.grid.grid)

    


if __name__ == '__main__':
    grid_size = 1
    robot_radius = 2
    start = (3, 10)
    goal = (15, 20)
    static_obstacles = [(5, 15), (10, 20)]
    dynamic_obstacles = {0: [(5, 16)], 1: [(5, 17)], 2: [(5, 18), (11, 20)]}
    planner = Planner(grid_size, robot_radius, start, goal, static_obstacles, dynamic_obstacles)
    print(planner.neighbour_table.lookup(planner.grid.snap_to_grid([10,15])))