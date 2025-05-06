import unittest
from utils.filters import filter_best_offers

class TestFilters(unittest.TestCase):
    def test_filter_best_offers(self):
        data = [
            {"item_id": "T4_BAG", "quality": 1, "city": "Caerleon", "sell_price_min": 1000},
            {"item_id": "T4_BAG", "quality": 1, "city": "Caerleon", "sell_price_min": 800},  # better
        ]
        result = filter_best_offers(data)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["sell_price_min"], 800)

if __name__ == "__main__":
    unittest.main()