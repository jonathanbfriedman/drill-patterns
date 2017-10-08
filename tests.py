#! /usr/bin/python

import unittest
import numpy as np

from drill import DrillPattern

class TestDrillPatternMethods(unittest.TestCase):

    def test_shuffle_p_no_shuffle(self):
        # if p = 0, no shuffling should take place
        array = np.array([[1,2],[3,4],[5,6]])
        shuffled = DrillPattern.shuffle_p(array, 0)
        self.assertTrue(np.array_equal(shuffled, array))

    def test_shuffle_p_50_percent_shuffle(self):
        # if p = 50, then half of all elements should change
        array = np.array([[1,2],[3,4],[5,6],[7,8]])
        array_len = len(array)
        shuffled = DrillPattern.shuffle_p(array, 50)

        # Count how many elements are the same
        count = 0
        for i in range(array_len):
            if np.array_equal(array[i], shuffled[i]):
                count += 1

        # Assert that at least half the elements remain unchanged
        # (a shuffle could result in no changes)
        self.assertTrue(count >= array_len//2)

    def test_shuffle_p_bug(self):
        # Test to debug issue with elements being copied twice
        # after shuffling
        array = np.array([[1,1],[2,2],[1,2],[2,1]])
        shuffled = DrillPattern.shuffle_p(array, 75)
        for el in array:
            self.assertIn(el.tolist(), shuffled.tolist())

    def test_path_length(self):
        # Path is three sides of a square of size 1
        path = np.array([[1,1],[1,2],[2,2],[2,1]])
        length = DrillPattern.path_length(path)
        self.assertEqual(length, 3)

    def test_shortest_path(self):
        # Points are four vertices of a square of size 1
        path1 = np.array([[1,1],[1,2],[2,2],[2,1]])
        path2 = np.array([[1,1],[2,2],[1,2],[2,1]])

        length1 = DrillPattern.path_length(path1)
        length2 = DrillPattern.path_length(path2)
        self.assertTrue(length1 < length2)

    def test_calculate_path(self):
        # Points are four vertices of a square of size 1
        # Shortest path_length should be 3
        path = np.array([[1,1],[2,2],[1,2],[2,1]])
        dp = DrillPattern(path)
        optimal_path = dp.calculate_path()
        length1 = DrillPattern.path_length(path)
        length2 = DrillPattern.path_length(optimal_path)
        self.assertTrue(length2 < length1)

if __name__ == '__main__':
        unittest.main()
