import unittest
from data.data_process import analyze_arbitrage, analyze_historical_trend

class TestDataProcess(unittest.TestCase):

    def test_analyze_arbitrage_basic(self):
        """Should detect one arbitrage opportunity with sufficient data."""
        sample_data = [
            {"item_id": "T4_BAG", "quality": 1, "city": "Caerleon", "sell_price_min": 1000},
            {"item_id": "T4_BAG", "quality": 1, "city": "Bridgewatch", "sell_price_min": 1200},
        ]
        sample_variants = [{"item_id": "T4_BAG", "quality": 1}]
        result = analyze_arbitrage(sample_data, sample_variants, min_margin=0.1, max_margin=1.0)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["origin"], "Caerleon")
        self.assertEqual(result[0]["destination"], "Bridgewatch")

    def test_analyze_arbitrage_insufficient_data(self):
        """Should return an empty list when there is not enough data for comparison."""
        sample_data = [
            {"item_id": "T4_BAG", "quality": 1, "city": "Caerleon", "sell_price_min": 1000}
        ]
        sample_variants = [{"item_id": "T4_BAG", "quality": 1}]
        result = analyze_arbitrage(sample_data, sample_variants)
        self.assertEqual(result, [])

    def test_analyze_historical_trend_positive(self):
        """Should detect a positive price trend when there is a significant increase."""
        history = {
            "T4_BAG@Caerleon": [{
                "item_id": "T4_BAG",
                "city": "Caerleon",
                "quality": 1,
                "data": [
                    {"timestamp": "2023-01-02", "prices_avg": 1000},
                    {"timestamp": "2023-01-01", "prices_avg": 800},
                ]
            }]
        }
        result = analyze_historical_trend(history, min_variation=0.1)
        self.assertEqual(len(result), 1)
        self.assertGreater(result[0]["variation"], 0)

    def test_analyze_historical_trend_empty(self):
        """Should return empty list if no data is provided."""
        result = analyze_historical_trend({}, min_variation=0.1)
        self.assertEqual(result, [])

if __name__ == "__main__":
    unittest.main()