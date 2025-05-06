import unittest
from unittest.mock import patch
from monitors.price_checker import run_price_monitor

class TestPriceChecker(unittest.TestCase):

    @patch("monitors.price_checker.run_alerts")
    @patch("monitors.price_checker.get_item_prices")
    @patch("monitors.price_checker.get_item_history")
    def test_run_price_monitor_flow(self, mock_history, mock_prices, mock_alerts):
        # Setup mocks
        mock_prices.return_value = [
            {"item_id": "T4_BAG", "city": "Caerleon", "sell_price_min": 1000, "quality": 1}
        ]
        mock_history.return_value = [
            {"timestamp": "2023-01-01", "prices_avg": 900},
            {"timestamp": "2023-01-02", "prices_avg": 1000}
        ]

        # Run
        sample_variants = [{"item_id": "T4_BAG", "base_name": "T4_BAG", "enchantment": 0, "quality": 1}]
        run_price_monitor(sample_variants)

        # Assertions
        mock_prices.assert_called_once()
        mock_history.assert_called()
        mock_alerts.assert_called_once()

if __name__ == "__main__":
    unittest.main()