from configs.config import CONFIG
import random as rnd
from Seller import Seller
from Buyer import Buyer

#creates agents sellers and buyers
def create_sellers() -> list[Seller]:
    sellers_list: list[Seller] = []

    num_sellers: int = CONFIG["num_sellers"]
    random_min_range: list[int] = CONFIG["seller_min_range"]
    expected_price_range: list[int] = CONFIG["initial_expected_price_for_seller"]
    inv: int = CONFIG["rockets_daily"]

    for i in range(num_sellers):
        seller_min: int = rnd.randint(random_min_range[0], random_min_range[1])
        selled_expected: int = max(rnd.randint(expected_price_range[0], expected_price_range[1]), seller_min)
        seller = Seller(seller_min, selled_expected, inv, True)
        sellers_list.append(seller)

    return sellers_list

def create_buyers() -> list[Buyer]:
    buyers_list: list[Buyer] = []

    num_buyers: int = CONFIG["num_buyers"]
    random_max_range: list[int] = CONFIG["buyer_max_range"]
    expected_price_range: list[int] = CONFIG["initial_expected_price_for_buyer"]

    for i in range(num_buyers):
        buyer_max: int = rnd.randint(random_max_range[0], random_max_range[1])
        buyer_expected: int = min(rnd.randint(expected_price_range[0], expected_price_range[1]), buyer_max)

        buyer = Buyer(buyer_max, buyer_expected)
        buyers_list.append(buyer)

    return buyers_list


viewed: int = 0
if __name__ == "__main__":
  sellers_list: list[Seller] = create_sellers()
  buyers_list: list[Buyer] = create_buyers()

  for i in range(CONFIG["simulate_for_ticks"]):
    day_stats: dict[str, int] = {
        "buyer_surplus_today": 0,
        "seller_surplus_today": 0,
        "trades_today": 0,
    }

    # 1. Shuffle buyers for fair daily search order
    rnd.shuffle(buyers_list)

    # 2. Main Trading Phase
    for buyer in buyers_list:
      # Filter for active sellers who have stock
      current_active_sellers: list[Seller] = [
          s for s in sellers_list if s.inventory > 0 and s.active
      ]

      if not current_active_sellers:
        break  # Market is fully out of stock/sellers for today

      k_size: int = min(
          len(current_active_sellers), CONFIG["seller_view_per_tick"]
      )
      sellers_to_view: list[Seller] = rnd.sample(
          current_active_sellers, k=k_size
      )

      for viewing_seller in sellers_to_view:
        if viewing_seller.expected_price <= buyer.expected_price:
          viewing_seller.sold_rocket()
          buyer.made_purchase_today()

          day_stats["buyer_surplus_today"] += buyer.calculate_surplus(
              viewing_seller.expected_price
          )
          day_stats["seller_surplus_today"] += viewing_seller.get_surplus()
          day_stats["trades_today"] += 1
          break  # Buyer completed purchase, move to next buyer

    # 3. End of Day Updates
    for seller in sellers_list:
      seller.end_of_day_update(CONFIG["rockets_daily"], CONFIG["price_step"])
    for buyer in buyers_list:
      buyer.new_day(CONFIG["price_step"])

    # 4. Print Day Metrics
    trades = day_stats["trades_today"]
    avg_buyer_surplus = (
        day_stats["buyer_surplus_today"] / trades if trades > 0 else 0.0
    )
    avg_seller_surplus = (
        day_stats["seller_surplus_today"] / trades if trades > 0 else 0.0
    )

    print(
        f"DAY: {i+1:03d} | Trades: {trades:2d} | "
        f"Tot Surplus (B/S): {day_stats['buyer_surplus_today']}/{day_stats['seller_surplus_today']} | "
        f"Avg Surplus (B/S): {avg_buyer_surplus:.2f}/{avg_seller_surplus:.2f}"
    )