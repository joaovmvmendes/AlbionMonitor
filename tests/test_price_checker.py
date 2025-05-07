import unittest
from unittest.mock import patch
from monitors.price_checker import run_price_monitor

class TestPriceChecker(unittest.TestCase):
    """Tests for the main price checker monitor."""

    @patch("monitors.price_checker.run_alerts")
    @patch("monitors.price_checker.get_item_history", return_value=[])
    @patch("monitors.price_checker.get_item_prices", return_value=[])
    def test_run_price_monitor_executes_pipeline(self, *_):
        """Should execute price collection and run alerts without error."""
        variants = [{"item_id": "T4_BAG", "quality": 1}]
        run_price_monitor(variants)  # No exception should be raised

if __name__ == "__main__":
    unittest.main()