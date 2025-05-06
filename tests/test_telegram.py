import unittest
from unittest.mock import patch, mock_open
from notifications.telegram import send_telegram_message, send_telegram_photo

class TestTelegram(unittest.TestCase):

    @patch("notifications.telegram.TELEGRAM_TOKEN", "fake-token")
    @patch("notifications.telegram.TELEGRAM_CHAT_ID", "123456")
    @patch("notifications.telegram.requests.post")
    def test_send_telegram_message_success(self, mock_post):
        mock_post.return_value.status_code = 200
        send_telegram_message("Hello!")
        mock_post.assert_called_once()

    @patch("notifications.telegram.TELEGRAM_TOKEN", "fake-token")
    @patch("notifications.telegram.TELEGRAM_CHAT_ID", "123456")
    @patch("notifications.telegram.requests.post")
    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data=b"fakeimage")
    def test_send_telegram_photo_success(self, mock_file, mock_exists, mock_post):
        mock_post.return_value.status_code = 200
        result = send_telegram_photo("chart.png", caption="Example")
        self.assertTrue(result)
        mock_post.assert_called_once()

    @patch("notifications.telegram.TELEGRAM_TOKEN", None)
    @patch("notifications.telegram.TELEGRAM_CHAT_ID", None)
    def test_send_telegram_message_invalid_config(self):
        result = send_telegram_message("Hello!")
        self.assertIsNone(result)

if __name__ == "__main__":
    unittest.main()