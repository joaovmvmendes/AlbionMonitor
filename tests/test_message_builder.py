import unittest
from unittest.mock import patch
from notifications.message_builder import format_arbitrage_alerts

class TestMessageBuilder(unittest.TestCase):
    """Tests for Telegram message formatting logic."""

    @patch("notifications.message_builder.calculate_sales_average", return_value=10)
    @patch("notifications.message_builder.get_item_chart", return_value=[])
    @patch("notifications.message_builder.generate_price_chart", return_value=None)
    def test_format_arbitrage_alerts_returns_text(self, _, __, ___):
        """Should return a formatted message and None image path for each opportunity."""
        opportunities = [{
            "item": "T4_BAG@1",
            "origin": "Caerleon",
            "destination": "Bridgewatch",
            "origin_price": 1000,
            "destination_price": 1200,
            "profit": 200,
            "margin": 0.2,
            "quality": 1
        }]
        messages = format_arbitrage_alerts(opportunities)

        self.assertIsInstance(messages, list)
        self.assertIsInstance(messages[0], tuple)
        self.assertIn("Profit:", messages[0][0])

if __name__ == "__main__":
    unittest.main()