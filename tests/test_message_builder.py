import unittest
from notifications.message_builder import format_arbitrage_alerts, format_trend_alerts

class TestMessageBuilder(unittest.TestCase):

    def test_format_arbitrage_alerts_empty(self):
        result = format_arbitrage_alerts([])
        self.assertEqual(len(result), 1)
        self.assertIn("Nenhuma oportunidade", result[0][0])

    def test_format_arbitrage_alerts_single(self):
        oportunidades = [{
            "item": "T4_BAG",
            "origem": "Caerleon",
            "destino": "Bridgewatch",
            "preco_origem": 1000,
            "preco_destino": 1300,
            "lucro": 300,
            "margem": 0.3,
            "quality": 1
        }]

        with unittest.mock.patch("notifications.message_builder.fetch_item_chart_data", return_value=[]), \
             unittest.mock.patch("notifications.message_builder.generate_price_chart", return_value="chart.png"), \
             unittest.mock.patch("config.constants.QUALITY_LABELS", {1: "Normal"}):

            result = format_arbitrage_alerts(oportunidades)
            self.assertEqual(len(result), 1)
            self.assertIn("*T4_BAG*", result[0][0])
            self.assertEqual(result[0][1], "chart.png")

    def test_format_trend_alerts(self):
        trends = [
            {"item": "T4_BAG", "cidade": "Caerleon", "inicio": 800, "fim": 1000, "variacao": 0.25}
        ]
        result = format_trend_alerts(
            {"T4_BAG@Caerleon": [{}]},
            lambda h, v: trends,
            variacao_min=0.1
        )
        self.assertTrue(result[0].startswith("📈"))

if __name__ == "__main__":
    unittest.main()