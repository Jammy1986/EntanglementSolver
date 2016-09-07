import unittest
from Part1_BruteForce.bruteforce import *


class MyTestCase(unittest.TestCase):
    def test_wrap_prevents_number_over_12(self):
        self.assertEqual(0, wrap_to_legal_range(12))
        self.assertEqual(1, wrap_to_legal_range(13))

    def test_wrap_prevents_number_under_0(self):
        self.assertEqual(11, wrap_to_legal_range(-1))
        self.assertEqual(10, wrap_to_legal_range(-2))

    def test_wrap_returns_number_if_no_change_required(self):
        self.assertEqual(5, wrap_to_legal_range(5))

    def test_partner_returns_correct_matches(self):
        self.assertEqual(1, partner(0, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]))
        self.assertEqual(1, partner(11, [2, 10, 8, 3, 5, 7, 9, 6, 11, 1, 0, 4]))

    def test_partners_returns_correct_matches(self):
        self.assertEqual([1, 3, 5, 7, 9, 11], partners(0, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]))
        self.assertEqual([11, 10, 7, 8, 6, 4], partners(7, [8, 1, 0, 2, 3, 6, 7, 11, 9, 10, 4, 5]))

    def test_map_creation(self):
        test_map = create_map(3)
        self.assertIsNone(test_map.get(Hex(0, 0, 0), None))
        self.assertListEqual([], test_map.get(Hex(0, -1, 1), None))
        self.assertListEqual([], test_map.get(Hex(0, -3, 3), None))
        self.assertIsNone(test_map.get(Hex(0, -4, 4), None))
        self.assertIsNone(test_map.get(Hex(10, 0, -10), None))

    def test_map_storage(self):
        test_map = create_map(3)
        test_map[hex_neighbor(Hex(0, 0, 0), 0)] = ["Up"]
        test_map[hex_neighbor(hex_neighbor(Hex(0, 0, 0), 0), 0)] = ["DoubleUp"]
        test_map[hex_neighbor(hex_neighbor(hex_neighbor(Hex(0, 0, 0), 0), 0), 1)] = ["DoubleUpAndRight"]

        self.assertEqual(["Up"], test_map.get(Hex(0, -1, 1)))
        self.assertEqual(["DoubleUp"], test_map.get(Hex(0, -2, 2)))
        self.assertEqual(["DoubleUpAndRight"], test_map.get(Hex(1, -3, 2)))

    def test_next_cell_position(self):
        self.assertEqual(0, next_cell_position(7))

    def test_single_tile_follow_path(self):
        test_map = create_map(3)
        test_map[Hex(0, -1, 1)] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

        score, current_location, current_hex = follow_path(test_map, 7, Hex(0, -1, 1))

        self.assertEqual(1, score)
        self.assertEqual(1, current_location)
        self.assertEqual(Hex(0, 0, 0), current_hex)

    def test_multiple_tile_follow_path(self):
        test_map = create_map(3)
        test_map[Hex(0, -1, 1)] = [1, 10, 3, 8, 0, 2, 4, 6, 5, 9, 7, 11]
        test_map[Hex(-1, -1, 2)] = [2, 4, 9, 11, 3, 10, 5, 6, 7, 8, 0, 1]
        test_map[Hex(0, -2, 2)] = [0, 10, 1, 5, 2, 8, 3, 11, 4, 7, 6, 9]

        score, current_location, current_hex = follow_path(test_map, 7, Hex(0, -1, 1))

        self.assertEqual(15, score)
        self.assertEqual(1, current_location)
        self.assertEqual(Hex(-1, 0, 1), current_hex)

    def test_brute_force(self):
        test_map = create_map(1)
        test_map[hex_direction(0)] = [0, 8, 1, 2, 3, 11, 4, 9, 5, 7, 6, 10]
        test_map[hex_direction(1)] = [0, 6, 1, 8, 2, 3, 4, 9, 5, 11, 7, 10]
        test_map[hex_direction(2)] = [0, 8, 1, 5, 2, 10, 3, 11, 4, 6, 7, 9]
        test_map[hex_direction(3)] = [0, 4, 1, 7, 2, 5, 3, 11, 6, 10, 8, 9]
        test_map[hex_direction(4)] = [0, 8, 1, 4, 2, 10, 3, 5, 6, 7, 9, 11]
        current_tile = [0, 4, 1, 11, 2, 7, 3, 9, 5, 6, 8, 10]
        swap_tile = [0, 2, 1, 8, 3, 4, 5, 11, 6, 7, 9, 10]
        tile_stack = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], [0, 10, 11, 2, 6, 7, 8, 4, 3, 9, 5, 1]]

        highest_score, best_placement = brute_force(test_map, hex_direction(5), 6, current_tile, swap_tile, tile_stack)

        self.assertEqual(6, highest_score)
        self.assertEqual(best_placement, [(1, "normal")])

    def test_longer_brute_force(self):
        test_map = create_map(1)
        current_tile = [0, 8, 1, 2, 3, 11, 4, 9, 5, 7, 6, 10]
        swap_tile = [0, 2, 1, 8, 3, 4, 5, 11, 6, 7, 9, 10]
        tile_stack = [[0, 6, 1, 8, 2, 3, 4, 9, 5, 11, 7, 10], [0, 8, 1, 5, 2, 10, 3, 11, 4, 6, 7, 9], [0, 4, 1, 7, 2, 5, 3, 11, 6, 10, 8, 9], [0, 8, 1, 4, 2, 10, 3, 5, 6, 7, 9, 11], [0, 4, 1, 11, 2, 7, 3, 9, 5, 6, 8, 10], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]]

        highest_score, best_placement = brute_force(test_map, hex_direction(0), 7, current_tile, swap_tile, tile_stack)
        print(highest_score)
        print(best_placement)


if __name__ == '__main__':
    unittest.main()
