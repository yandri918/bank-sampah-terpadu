import json
import os

# Definition of default prices
default_pricing = {
    "Burnable": {"buy": 140, "sell": 300},        # Margin ~53%
    "Paper": {"buy": 2100, "sell": 3000},         # Margin ~30%
    "Cloth": {"buy": 1000, "sell": 1500},         # Margin ~33%
    "Cans": {"buy": 9800, "sell": 14000},         # Margin ~30%
    "Electronics": {"buy": 14000, "sell": 20000}, # Margin ~30%
    "PET_Bottles": {"buy": 3800, "sell": 5500},   # Margin ~30%
    "Plastic_Marks": {"buy": 1400, "sell": 2000}, # Margin ~30%
    "White_Trays": {"buy": 700, "sell": 1000},    # Margin ~30%
    "Glass_Bottles": {"buy": 700, "sell": 1000},  # Margin ~30%
    "Metal_Small": {"buy": 3000, "sell": 4500},   # Margin ~33%
    "Hazardous": {"buy": 0, "sell": 0}
}

def load_prices():
    file_path = "data/waste_prices.json"
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    else:
        # Create default if not exists
        os.makedirs("data", exist_ok=True)
        save_prices(default_pricing)
        return default_pricing

def save_prices(prices):
    os.makedirs("data", exist_ok=True)
    with open("data/waste_prices.json", "w") as f:
        json.dump(prices, f, indent=4)
