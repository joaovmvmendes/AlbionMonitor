import unittest
from unittest.mock import patch, MagicMock
from notifications.alert_runner import run_alerts

class TestAlertFlow(unittest.TestCase):
    @patch("notifications.alert_runner.send_telegram_message")
    @patch("notifications.alert_runner.send_image_and_cleanup")
    @patch("data.data_process.analyze_arbitrage")
    @patch("notifications.message_builder.format_arbitrage_alerts")
    @patch("notifications.message_builder.format_trend_alerts")
    @patch("data.data_process.analyze_historical_trend")
    def test_run_alerts_flow(
        self,
        mock_analyze_trend,
        mock_format_trends,
        mock_format_alerts,
        mock_analyze_arbitrage,
        mock_send_image,
        mock_send_message
    ):
        # Dados simulados
        sample_data = [{"item_id": "T4_BAG", "city": "Caerleon", "sell_price_min": 1000, "sell_price_max": 1200}]
        sample_variants = [{"item_id": "T4_BAG", "quality": 1}]
        sample_history = {"T4_BAG@Caerleon": [{"data": [{"prices_avg": 1000}, {"prices_avg": 800}]}]}

        # Configurar os mocks
        mock_analyze_arbitrage.return_value = [{"item": "T4_BAG", "origem": "Caerleon", "destino": "Bridgewatch", "preco_origem": 1000, "preco_destino": 1500, "lucro": 500, "margem": 0.5, "quality": 1}]
        mock_format_alerts.return_value = [("Alerta simulado", "fake_path.png")]
        mock_send_image.return_value = True
        mock_send_message.return_value = None
        mock_analyze_trend.return_value = [{"item": "T4_BAG", "cidade": "Caerleon", "inicio": 800, "fim": 1000, "variacao": 0.25}]
        mock_format_trends.return_value = ["📈 *Tendências simuladas*"]

        # Executar a função alvo
        run_alerts(sample_data, sample_variants, history=sample_history)

        # Verificações
        mock_analyze_arbitrage.assert_called_once()
        mock_format_alerts.assert_called_once()
        mock_send_image.assert_called_once()
        mock_send_message.assert_any_call("Alerta simulado")
        mock_format_trends.assert_called_once()

if __name__ == '__main__':
    unittest.main()