# backend/tests/test_elo_system.py

import unittest
from services.game_service import calculate_new_elo


class TestEloCalculation(unittest.TestCase):
    def test_equal_ratings_win(self):
        rating1, rating2 = 1000, 1000
        new_rating1, new_rating2 = calculate_new_elo(rating1, rating2, 1)
        self.assertEqual(new_rating1, 1015)
        self.assertEqual(new_rating2, 985)

    def test_equal_ratings_draw(self):
        rating1, rating2 = 1000, 1000
        new_rating1, new_rating2 = calculate_new_elo(rating1, rating2, 0.5)
        self.assertEqual(new_rating1, 1000)
        self.assertEqual(new_rating2, 1000)

    def test_higher_rating_wins(self):
        rating1, rating2 = 1100, 1000
        new_rating1, new_rating2 = calculate_new_elo(rating1, rating2, 1)
        self.assertEqual(new_rating1, 1110)
        self.assertEqual(new_rating2, 989)

    def test_higher_rating_loses(self):
        rating1, rating2 = 1100, 1000
        new_rating1, new_rating2 = calculate_new_elo(rating1, rating2, 0)
        self.assertEqual(new_rating1, 1080)
        self.assertEqual(new_rating2, 1019)

    def test_higher_rating_draws(self):
        rating1, rating2 = 1100, 1000
        new_rating1, new_rating2 = calculate_new_elo(rating1, rating2, 0.5)
        self.assertEqual(new_rating1, 1095)
        self.assertEqual(new_rating2, 1004)


if __name__ == '__main__':
    unittest.main()
