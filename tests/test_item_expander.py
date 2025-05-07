import unittest
from utils.item_expander import expand_item_variants

class TestItemExpander(unittest.TestCase):
    """Tests for item expansion logic."""

    def test_expand_item_variants_generates_correct_ids(self):
        """Should expand each enchantment into a separate variant with correct ID."""
        items = [{"base_name": "T4_BAG", "enchantments": [0, 1], "quality": 1}]
        result = expand_item_variants(items)

        self.assertEqual(len(result), 2)
        self.assertIn("item_id", result[0])
        self.assertIn("quality", result[0])
        self.assertEqual(result[0]["base_name"], "T4_BAG")

if __name__ == "__main__":
    unittest.main()