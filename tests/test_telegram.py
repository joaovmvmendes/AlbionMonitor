import unittest
from unittest.mock import patch, mock_open
from notifications.telegram import send_telegram_message, send_telegram_photo

class TestTelegram(unittest.TestCase):
    """Tests for Telegram messaging utilities."""

    @patch("notifications.telegram.requests.post")
    def test_send_telegram_message_success(self, mock_post):
        """Should call the Telegram API without raising errors."""
        mock_post.return_value.raise_for_status = lambda: None
        send_telegram_message("Test message")

    @patch("notifications.telegram.os.path.exists", return_value=True)
    @patch("notifications.telegram.requests.post")
    @patch("builtins.open", new_callable=mock_open, read_data=b"image")
    def test_send_telegram_photo_success(self, mock_file, mock_post, _):
        """Should send an image and return True on success."""
        mock_post.return_value.raise_for_status = lambda: None
        result = send_telegram_photo("mock.png", "Test caption")
        self.assertTrue(result)

if __name__ == "__main__":
    unittest.main()