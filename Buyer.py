class Buyer:

  def __init__(self, max_price: int, expected_price: int) -> None:
    self.max_price: int = max_price
    self.expected_price: int = expected_price
    self.bought_merchandise_today: bool = False

  def made_purchase_today(self) -> None:
    """Flag that a transaction was completed today."""
    self.bought_merchandise_today = True

  def increase_expected_price(self, price_step: int) -> None:
    """Increase expected price, capped at private max_price."""
    self.expected_price = min(self.max_price, self.expected_price + price_step)

  def reduce_expected_price(self, price_step: int) -> None:
    """Reduce expected price, floor at 1."""
    self.expected_price = max(1, self.expected_price - price_step)

  def calculate_surplus(self, purchase_amount: int) -> int:
    """Calculate consumer surplus (max valuation minus actual price paid)."""
    return self.max_price - purchase_amount

  def new_day(self, price_step: int) -> None:
    """Adjust expected price based on daily experience and reset trade flag."""
    if self.bought_merchandise_today:
      self.reduce_expected_price(price_step)
    else:
      self.increase_expected_price(price_step)

    self.bought_merchandise_today = False