#!/usr/bin/env python3
'''
Author: Haoran Peng
Email: gavinsweden@gmail.com
'''
from typing import Tuple, List, Dict
from heapq import heappush, heappop
import numpy as np
from scipy.spatial import KDTree

from .neighbour_table import NeighbourTable
from .grid import Grid
from .state import State


# static obstacles must include the boundary
# kd-tree faster with more obst (>30), slow if less: kd for static, brute for dynamic
# indexing consisten with opencv
class Planner:

    def __init__(self, grid_size: int,
                       robot_radius: int,
                       start: Tuple[int, int],
                       goal: Tuple[int, int],
                       static_obstacles: List[Tuple[int, int]],
                       dynamic_obstacles: Dict[int, List[Tuple[int, int]]],
                       max_iter:int = 10000,
                       debug = False):
        self.grid_size = grid_size
        self.robot_radius = robot_radius
        np_static_obstacles = np.array(static_obstacles)
        self.static_obstacles = KDTree(np_static_obstacles)
        self.dynamic_obstacles = dict((k, np.array(v)) for k, v in dynamic_obstacles.items())

        # Make the grid according to the grid size
        self.grid = Grid(grid_size, np_static_obstacles)
        # Make a lookup table for looking up neighbours of a grid
        self.neighbour_table = NeighbourTable(self.grid.grid)

        self.start = self.grid.snap_to_grid(np.array(start))
        self.goal = self.grid.snap_to_grid(np.array(goal))
        self.max_iter = max_iter
        self.debug = debug

    '''
    An admissible and consistent heuristic for A*
    '''
    @staticmethod
    def h(start: np.ndarray, goal: np.ndarray) -> int:
        return int(np.linalg.norm(start-goal, 1))  # L1 norm

    @staticmethod
    def l2(start: np.ndarray, goal: np.ndarray) -> int:
        return int(np.linalg.norm(start-goal, 2))  # L2 norm

    '''
    Check whether the nearest static obstacle is within radius
    '''
    def safe_static(self, grid_pos: np.ndarray) -> bool:
        return self.l2(grid_pos, self.static_obstacles.query(grid_pos)) > self.robot_radius

    '''
    Assume dynamic obstacles are agents with same radius, distance needs to be 2*radius
    '''
    def safe_dynamic(self, grid_pos: np.ndarray, time: int) -> bool:
        return all(self.l2(grid_pos, obstacle) > 2*self.robot_radius
                   for obstacle in self.dynamic_obstacles.setdefault(time, []))

    '''
    Space-Time A*
    '''
    def plan(self) -> np.ndarray:
        # Initialize the start state
        s = State(self.start, 0, 0, self.h(self.start, self.goal))

        open_set = [s]
        closed_set = set()

        # Keep track of parent nodes for reconstruction
        came_from = dict()

        iter_ = 0
        while open_set and iter_ < self.max_iter:
            iter_ += 1
            current_state = open_set[0]  # Smallest element in min-heap
            if current_state.pos_equal_to(self.goal):
                if self.debug:
                    print('Path found after {0} iterations'.format(iter_))
                return self.reconstruct_path(came_from, current_state)

            closed_set.add(heappop(open_set))
            epoch = current_state.time + 1
            for neighbour in self.neighbour_table.lookup(current_state.pos):
                neighbour_state = State(neighbour, epoch, current_state.g_score + 1, self.h(neighbour, self.goal))
                # Check if visited
                if neighbour_state in closed_set:
                    continue

                # Avoid obstacles
                if not self.safe_static(neighbour) or not self.safe_dynamic(neighbour, epoch):
                    continue

                # Add to open set
                if neighbour_state not in open_set:
                    came_from[neighbour_state] = current_state
                    heappush(open_set, neighbour_state)

        if self.debug:
            print('Open set is empty, no path found.')
        return None

    '''
    Reconstruct path from A* search result
    '''
    def reconstruct_path(self, came_from: Dict[State, State], current: State) -> np.ndarray:
        total_path = [current.pos]
        while current in came_from.keys():
            current = came_from[current]
            total_path.append(current.pos)
        return np.array(total_path[::-1])



