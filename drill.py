#! /usr/bin/python

import numpy as np

GENERATIONS=10 # Number of generations
POPULATION=10 # Size of population
MUTATIONS=100 # Percent mutation rate

INIT_ERROR_MSG="Class must be initialized with 2D array of points."

def shuffle_p(ar, p=100):
    """
    Shuffle an array along first axis changing
    only p percent of the array.
    """
    # Calculate the number of elements to shuffle
    array_len = len(ar)
    num = array_len*p/100

    # Return original array in case of no change
    if num == 0:
        return ar

    # Randomly choose pairs of indices to shuffle
    r_indices = np.random.choice(np.arange(array_len), [int(num/2),2], False)

    shuffled_ar = np.copy(ar)

    # Iterate over indices of points to shuffle and use matrix multiplication to swap
    # points in original array
    for r_i in r_indices:
        identity = np.identity(array_len)
        identity[r_i,:] = identity[r_i[::-1],:]
        shuffled_ar = np.dot(identity,shuffled_ar)

    return shuffled_ar

def path_length(path):
    """
    Returns the path length (Euclidean distance) along an array of 2D points.
    Ignores difference between start and end position
    """
    length = 0
    for i in range(len(path)-1):
        length += np.sqrt(
                (path[i][0]-path[i+1][0])**2 + (path[i][1]-path[i+1][1])**2)
    return length

def shortest_path(path_array):
    """
    Returns the shortest path (Euclidean distance)
    Ignores difference between start and end position
    """
    shortest_length = np.inf
    array_size = len(path_array)
    shortest_path = np.array([])
    for i in range(array_size):
        path = path_array[i]
        length = path_length(path)
        if length < shortest_length:
            shortest_length = length
            shortest_path = path
    return shortest_path


class DrillPattern(object):
    """
    Class for computing order of drilling paths
    Input: numpy array of 2D points
    Output:
    """

    def __init__(self, path):
        """
        Perform validation on input
        """
        try:
            path = np.array(path)
        except ValueError as err:
            print(INIT_ERROR_MSG)
            raise err

        # Check that the input is a 2D array with 2 columns
        shape = path.shape
        if len(shape) == 2:
            if shape[1] == 2:
                self.path = path
                return

        # Else raise an error
        print(INIT_ERROR_MSG)
        raise ValueError

    def calculate_path(self, generations=GENERATIONS,
            population=POPULATION, mutations=MUTATIONS):
        """
        Uses evolutionary algorithm to find best path
        to drill all holes (least total time, least total distance)
        """
        # Start by choosing a path in the same order as the points are given
        path = self.path

        # Iterate over generations
        optimal_path = path
        while generations > 0:
            # 1. Reproduction
            # Create number of copies of current path based on population size
            path_set = []
            for i in range(population):
                path_set += [optimal_path]

            # 2. Mutation
            # Mutate according to mutation rate
            mutated_path_set = []
            for j in range(population-1):
                mutated_path_set += [shuffle_p(path_set[j], mutations)]

            # Keep the optimal path from the last generation to prevent devolution
            np.append(mutated_path_set, optimal_path)

            # 3. Selection
            # Select the shortest path (in case of tie, pick first)
            optimal_path = shortest_path(mutated_path_set)
            generations = generations - 1
        return optimal_path
