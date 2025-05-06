import unittest
from utils.item_expander import expand_item_variants

class TestItemExpander(unittest.TestCase):
    def test_expand_single_item(self):
        config = [{
            "base_name": "T4_BAG",
            "enchantments": [0, 3],
            "quality": 1
        }]
        result = expand_item_variants(config)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["item_id"], "T4_BAG")
        self.assertEqual(result[1]["item_id"], "T4_BAG@3")

    def test_invalid_item_skipped(self):
        config = [{"base_name": "", "enchantments": [0], "quality": 1}]
        result = expand_item_variants(config)
        self.assertEqual(result, [])

if __name__ == "__main__":
    unittest.main()