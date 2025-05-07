import unittest
from unittest.mock import patch
from services import albion_api

class TestAlbionAPI(unittest.TestCase):
    """Tests for Albion Online API service wrapper."""

    @patch("services.albion_api.requests.get")
    def test_get_item_prices_success(self, mock_get):
        """Should return item list when API call succeeds."""
        mock_get.return_value.json.return_value = [{"item_id": "T4_BAG"}]
        mock_get.return_value.raise_for_status = lambda: None

        result = albion_api.get_item_prices("T4_BAG", 1)
        self.assertIsInstance(result, list)
        self.assertEqual(result[0]["item_id"], "T4_BAG")

    @patch("services.albion_api.requests.get")
    def test_get_item_prices_failure(self, mock_get):
        """Should return empty list on API failure."""
        mock_get.side_effect = Exception("API error")
        result = albion_api.get_item_prices("T4_BAG", 1)
        self.assertEqual(result, [])

if __name__ == "__main__":
    unittest.main()