#! /usr/bin/python

import numpy as np

GENERATIONS=100 # Number of generations
POPULATION=30 # Size of population
MUTATIONS=10 # Percent mutation rate

class DrillPattern(object):
    """
    Class for computing order of drilling paths
    Input: numpy array of 2D points
    Output:
    """

    def __init__(self, points):
        """
        Perform validation on input
        """
        return

    def shuffle_p(ar, p=100):
        """
        Shuffle an array along first axis changing
        only p percent of the array.
        """
        # Calculate the number of elements to shuffle
        array_len = len(ar)
        num = array_len*p//100

        if num == 0:
            return ar

        # Randomly select a subarray to randomly shuffle
        r_indices = np.random.choice(range(array_len), num, False)
        subar = np.array([[]])
        for r_i in r_indices:
            subar = np.append([[subar]], [[np.copy(ar[r_i])]])

        subar = np.reshape(subar, (num,2))

        # Generate new array with p percent randomized
        # Collect the indices of each subarray element in the original array
        i_order = [] # initial order
        for el in subar:
            # Find its index
            i = np.asarray(np.where(ar == el)).T[0][0]
            i_order += [i]
        i_order = np.sort(np.array(i_order))

        # Traverse original array, replacing any shuffled elements
        shuffled_ar = np.copy(ar)
        for i in range(num):
            if i in i_order:
                shuffled_ar[i_order[i]] = subar[i]
        return shuffled_ar

    def path_length(path):
        """
        Returns the path length (Euclidean distance)
        Ignores difference between start and end position
        """
        length = 0
        for i in range(1,len(path)-1):
            length += np.sqrt(
                    (path(i)[0]-path(i+1)[0])**2 + (path(i)[1]-path(i+1)[1])**2)

    def shortest_path(path_array, population=POPULATION):
        """
        Returns the shortest path (Euclidean distance)
        Ignores difference between start and end position
        """
        shortest_length = np.inf
        for i in range(1,population):
            path = path_array[i]
            length = path_length(path)
            if length < shortest_length:
                shortest_length = length
                shortest_path = path
        return shortest_path

    def calculate_path(generations=GENERATIONS,
            population=POPULATION, mutations=MUTATIONS):
        """
        Uses evolutionary algorithm to find best path
        to drill all holes (least total time, least total distance)
        """
        # Start by choosing a path in the same order as the points are given
        path = points

        # Iterate over generations
        while generations > 0:

            # 1. Reproduction
            # Create number of copies of current path based on population size
            path_set = []
            for i in population:
                path_set += [path]

            # 2. Mutation
            # Mutate according to mutation rate
            for j in population:
                mutated_path_set = shuffle_p(path_set[j], mutations)

            # 3. Selection
            # Select the shortest path (in case of tie, pick first)
            path = shortest_path(mutated_path_set)
        return path
