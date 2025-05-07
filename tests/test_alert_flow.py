import unittest
from unittest.mock import patch
from notifications.alert_runner import run_alerts

class TestAlertFlow(unittest.TestCase):
    @patch("os.path.exists", return_value=True)
    @patch("os.remove")
    @patch("notifications.alert_runner.send_telegram_message")
    @patch("notifications.alert_runner.send_image_and_cleanup")
    @patch("notifications.alert_runner.format_arbitrage_alerts")
    @patch("notifications.alert_runner.analyze_arbitrage")
    def test_alert_execution(
        self, mock_analyze, mock_format, mock_send_image,
        mock_send_message, mock_remove, mock_exists
    ):
        """
        Ensures the alert flow calls message and image sending functions
        when arbitrage opportunities are found.
        """
        mock_image_path = "mock_image.png"
        mock_analyze.return_value = [{
            "item": "T4_BAG",
            "origin": "Caerleon",
            "destination": "Bridgewatch",
            "origin_price": 1000,
            "destination_price": 1500,
            "profit": 500,
            "margin": 0.5,
            "quality": 1
        }]
        mock_format.return_value = [("Mock alert text", mock_image_path)]

        run_alerts([], [{"item_id": "T4_BAG", "quality": 1}], history={})

        mock_send_message.assert_called_once_with("Mock alert text")
        mock_send_image.assert_called_once_with(mock_image_path)

if __name__ == "__main__":
    unittest.main()