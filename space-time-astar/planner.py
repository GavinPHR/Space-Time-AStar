#!/usr/bin/env python3
'''
Author: Haoran Peng
Email: gavinsweden@gmail.com
'''
from typing import Tuple, List, Dict
from collections import defaultdict
import heapq
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
        # Function to hash a position
        self.hash = NeighbourTable.hash

    '''
    Used to calculate distance between two points
    Also an admissible and consistent heuristic for A*
    '''
    @staticmethod
    def h(start: np.ndarray, goal: np.ndarray) -> int:
        return int(np.linalg.norm(start-goal, 1))  # L2 norm

    '''
    Check whether the nearest static obstacle is within radius
    '''
    def safe_static(self, grid_pos: np.ndarray) -> bool:
        return self.h(grid_pos, self.static_obstacles.query(grid_pos)) > self.robot_radius

    '''
    Assume dynamic obstacles are agents with same radius, distance needs to be 2*radius
    '''
    def safe_dynamic(self, grid_pos: np.ndarray, time: int) -> bool:
        return all(self.h(grid_pos, obstacle) > 2*self.robot_radius
                   for obstacle in self.dynamic_obstacles.setdefault(time, []))

    '''
    Reconstruct path from A* search result
    '''
    def reconstruct_path(self, came_from: Dict[int, np.ndarray], current: np.ndarray):
        total_path = [current]
        while self.hash(current) in came_from.keys():
            current = came_from[self.hash(current)]
            total_path.append(current)
        return total_path[::-1]

    '''
    Space-Time A*
    '''
    def plan(self):
        # Standard A* setup, no surprise here
        '''
        need to implement heap here
        '''
        open_set = []
        came_from = dict()
        g_score = defaultdict(lambda: float('inf'))
        g_score[self.hash(self.start)] = 0
        f_score = defaultdict(lambda: float('inf'))
        f_score[self.hash(self.start)] = self.h(self.start, self.goal)

        while open_set:


if __name__ == '__main__':
    grid_size = 1
    robot_radius = 2
    start = (3, 10)
    goal = (15, 20)
    static_obstacles = [(5, 15), (10, 20)]
    dynamic_obstacles = {0: [(5, 16)], 1: [(5, 17)], 2: [(5, 18), (11, 20)]}
    planner = Planner(grid_size, robot_radius, start, goal, static_obstacles, dynamic_obstacles)
    print(planner.neighbour_table.lookup(planner.grid.snap_to_grid([10,15])))