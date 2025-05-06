import unittest
from unittest.mock import patch, MagicMock
from utils.graph_builder import generate_price_chart

class TestGraphBuilder(unittest.TestCase):

    @patch("utils.graph_builder.plt")
    def test_generate_price_chart_success(self, mock_plt):
        mock_plt.savefig = MagicMock()
        mock_plt.close = MagicMock()

        sample_data = [
            {"timestamp": "2023-01-01T00:00:00", "avg_price": 1000},
            {"timestamp": "2023-01-01T01:00:00", "avg_price": 1100},
        ]

        path = generate_price_chart(sample_data, "T4_BAG", "Caerleon", output_dir="charts")
        self.assertTrue("T4_BAG_Caerleon.png" in path)

    def test_generate_price_chart_empty(self):
        path = generate_price_chart([], "T4_BAG", "Caerleon")
        self.assertIsNone(path)

if __name__ == "__main__":
    unittest.main()