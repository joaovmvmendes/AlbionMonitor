import unittest
from unittest.mock import patch
from utils.graph_builder import generate_price_chart

class TestGraphBuilder(unittest.TestCase):
    """Tests for graph generation utility."""

    @patch("utils.graph_builder.plt.savefig")
    @patch("utils.graph_builder.os.makedirs")
    def test_generate_price_chart_creates_image(self, mock_mkdir, mock_save):
        """Should create a chart and return its path when data is valid."""
        data = [
            {"timestamp": "2023-01-01T12:00:00", "avg_price": 1000},
            {"timestamp": "2023-01-01T13:00:00", "avg_price": 1050},
        ]
        result = generate_price_chart(data, "T4_BAG", "Caerleon")
        self.assertIsInstance(result, str)
        self.assertIn("T4_BAG_Caerleon.png", result)

if __name__ == "__main__":
    unittest.main()