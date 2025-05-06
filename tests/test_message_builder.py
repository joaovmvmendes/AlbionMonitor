import unittest
from unittest.mock import patch
from notifications.message_builder import format_arbitrage_alerts, format_trend_alerts

class TestMessageBuilder(unittest.TestCase):
    def test_format_arbitrage_alerts_empty(self):
        result = format_arbitrage_alerts([])
        self.assertEqual(len(result), 1)
        self.assertIn("Nenhuma oportunidade", result[0][0])

    @patch("notifications.message_builder.get_item_chart", return_value=[])
    @patch("notifications.message_builder.generate_price_chart", return_value="chart.png")
    @patch("notifications.message_builder.calculate_sales_average", return_value=10)
    def test_format_arbitrage_alerts_single(self, mock_sales, mock_chart, mock_chart_data):
        opportunities = [{
            "item": "T4_BAG",
            "origem": "Caerleon",
            "destino": "Bridgewatch",
            "preco_origem": 1000,
            "preco_destino": 1300,
            "lucro": 300,
            "margem": 0.3,
            "quality": 1
        }]
        result = format_arbitrage_alerts(opportunities)
        assert result[0][1].endswith(".png")


    def test_format_trend_alerts(self):
        trends = [
            {"item": "T4_BAG", "cidade": "Caerleon", "inicio": 800, "fim": 1000, "variacao": 0.25}
        ]
        result = format_trend_alerts(
            {"T4_BAG@Caerleon": [{}]},
            lambda h, v: trends,
            min_variation=0.1
        )
        self.assertTrue(result[0].startswith("📈"))

if __name__ == "__main__":
    unittest.main()