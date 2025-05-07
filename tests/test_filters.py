import unittest
from utils.filters import filter_best_offers

class TestFilters(unittest.TestCase):
    """Tests for best offer filtering function."""

    def test_filter_best_offers_returns_lowest_price(self):
        """Should retain only the lowest offer per item-quality-city."""
        data = [
            {"item_id": "T4_BAG", "quality": 1, "city": "Caerleon", "sell_price_min": 1000},
            {"item_id": "T4_BAG", "quality": 1, "city": "Caerleon", "sell_price_min": 900},
        ]
        result = filter_best_offers(data)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["sell_price_min"], 900)

if __name__ == "__main__":
    unittest.main()