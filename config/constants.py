# 🔗 Base URL for price queries from the Albion Online API
API_BASE_URL = "https://west.albion-online-data.com/api/v2/stats/prices"

# 🌍 Official list of Albion Online cities for market scan
CITIES = [
    "Caerleon",
    "Bridgewatch",
    "Lymhurst",
    "Martlock",
    "Fort Sterling",
    "Thetford",
    "Brecilien"
]

# 📦 List of items to be monitored
# Each entry includes:
# - base_name: item name
# - enchantments: enchantment levels (@X)
# - quality: desired quality (1 = Normal, 5 = Masterpiece)
ITEM_NAMES = [
    {"base_name": "T4_BAG",     "enchantments": [0, 3],    "quality": 1},
    {"base_name": "T5_BAG",     "enchantments": [2],       "quality": 2},
    {"base_name": "T6_BAG",     "enchantments": [1, 4],    "quality": 4},
    {"base_name": "T4_CAPE",    "enchantments": [0],       "quality": 1},
    {"base_name": "T5_CAPE",    "enchantments": [2],       "quality": 3},
    {"base_name": "T6_CAPE",    "enchantments": [3, 1],    "quality": 1},
]

# 🎖️ Quality levels translated to friendly display labels
QUALITY_LABELS = {
    1: "Normal",
    2: "Good",
    3: "Outstanding",
    4: "Excellent",
    5: "Masterpiece"
}