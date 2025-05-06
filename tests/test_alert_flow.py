import unittest
from unittest.mock import patch
from notifications.alert_runner import run_alerts

class TestAlertFlow(unittest.TestCase):
    @patch("notifications.alert_runner.send_telegram_message")
    @patch("notifications.alert_runner.send_image_and_cleanup")
    @patch("notifications.message_builder.format_arbitrage_alerts")
    @patch("data.data_process.analyze_arbitrage")
    def test_alert_execution(
        self, mock_analyze, mock_format, mock_send_image, mock_send_message
    ):
        mock_analyze.return_value = [{"item": "T4_BAG", "origem": "Caerleon", "destino": "Bridgewatch", "preco_origem": 1000, "preco_destino": 1500, "lucro": 500, "margem": 0.5, "quality": 1}]
        mock_format.return_value = [("Mock alert text", "mock_image.png")]
        run_alerts([], [{"item_id": "T4_BAG", "quality": 1}], history={})
        mock_send_message.assert_called_once()
        mock_send_image.assert_called_once()

if __name__ == "__main__":
    unittest.main()