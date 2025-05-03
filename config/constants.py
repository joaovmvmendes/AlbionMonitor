# config/constants.py

API_BASE_URL = "https://west.albion-online-data.com/api/v2/stats/prices"

CITIES = [
    "Caerleon", "Bridgewatch", "Lymhurst",
    "Martlock", "Fort Sterling", "Thetford", "Brecilien"
]

ITEM_NAMES = [
    {"base_name": "T4_BAG", "enchantments": [0, 3], "quality": 1},
    {"base_name": "T5_BAG", "enchantments": [2], "quality": 2},
    {"base_name": "T6_BAG", "enchantments": [1, 4], "quality": 4},
    {"base_name": "T4_CAPE", "enchantments": [0], "quality": 1},
    {"base_name": "T5_CAPE", "enchantments": [2], "quality": 3},
    {"base_name": "T6_CAPE", "enchantments": [3, 1], "quality": 1}
]

QUALITY_LABELS = {
    1: "Normal",
    2: "Good",
    3: "Outstanding",
    4: "Excellent",
    5: "Masterpiece"
}