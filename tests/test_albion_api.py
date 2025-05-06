import unittest
from unittest.mock import patch
from services import albion_api

class TestAlbionAPI(unittest.TestCase):

    @patch("services.albion_api.requests.get")
    def test_get_item_prices_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [{"item_id": "T4_BAG", "city": "Caerleon", "sell_price_min": 1000}]

        result = albion_api.get_item_prices("T4_BAG", quality=1)
        self.assertIsInstance(result, list)
        self.assertEqual(result[0]["item_id"], "T4_BAG")

    @patch("services.albion_api.requests.get")
    def test_get_item_prices_error(self, mock_get):
        mock_get.side_effect = Exception("Connection error")
        result = albion_api.get_item_prices("T4_BAG", quality=1)
        self.assertEqual(result, [])

    @patch("services.albion_api.requests.get")
    def test_get_item_history_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [{"prices_avg": 1000}, {"prices_avg": 1100}]
        
        result = albion_api.get_item_history("T4_BAG", "Caerleon", days=2)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["prices_avg"], 1000)

    @patch("services.albion_api.requests.get")
    def test_get_item_chart_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [
            {
                "location": "Caerleon",
                "quality": 1,
                "data": {
                    "timestamps": ["2023-01-01T00:00:00", "2023-01-01T01:00:00"],
                    "prices_avg": [1000, 1050]
                }
            }
        ]

        result = albion_api.get_item_chart("T4_BAG@3", "Caerleon", quality=1, days=1)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["avg_price"], 1000)

    @patch("services.albion_api.requests.get")
    def test_get_item_chart_invalid_data(self, mock_get):
        # Unequal timestamps and prices should return []
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [
            {
                "location": "Caerleon",
                "quality": 1,
                "data": {
                    "timestamps": ["2023-01-01T00:00:00"],
                    "prices_avg": [1000, 1100]
                }
            }
        ]

        result = albion_api.get_item_chart("T4_BAG", "Caerleon", quality=1, days=1)
        self.assertEqual(result, [])

if __name__ == "__main__":
    unittest.main()