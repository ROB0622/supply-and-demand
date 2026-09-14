from typing import TypedDict

class ConfigType(TypedDict):
    num_sellers: int
    num_buyers: int
    seller_min_range: list[int]
    buyer_max_range: list[int]
    initial_expected_price_for_buyer: list[int]
    initial_expected_price_for_seller: list[int]
    seller_view_per_tick: int
    rockets_daily: int
    price_step: int
    simulate_for_ticks: int

CONFIG: ConfigType = {
    "num_sellers": 300,
    "num_buyers": 300,
    "seller_min_range": [100, 150],
    "buyer_max_range": [120, 220],
    "initial_expected_price_for_buyer": [80, 200],
    "initial_expected_price_for_seller": [100, 300],
    "seller_view_per_tick": 10,
    "rockets_daily": 2,
    "price_step": 3,
    "simulate_for_ticks": 500
}