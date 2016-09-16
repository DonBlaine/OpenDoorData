import unittest

from application.occupancy_prediction import set_occupancy_category

class Testing(unittest.TestCase):
    def test_set_occupancy_category(self):
        self.assertEqual(set_occupancy_category(0, 5), (0, "empty", False))
        self.assertEqual(set_occupancy_category(1, 5), (0.25, "moderate", True))
        self.assertEqual(set_occupancy_category(2, 5), (0.5, "moderate", True))
        self.assertEqual(set_occupancy_category(3, 5), (0.5, "moderate", True))
        self.assertEqual(set_occupancy_category(4, 5), (0.75, "full", True))
        self.assertEqual(set_occupancy_category(5, 5), (1.0, "full", True))
        self.assertEqual(set_occupancy_category(6, 5), (1.0, "full", True))


if __name__ == '__main__':
    unittest.main()