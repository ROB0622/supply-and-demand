class Seller:

  def __init__(
      self, min_price: int, expected_price: int, inventory: int, active: bool = True) -> None:
    self.min_price: int = min_price
    self.expected_price: int = expected_price
    self.inventory: int = inventory
    self.active: bool = active
    self.sold_today: bool = False

  def get_stats(self) -> dict[str, int | bool]:
    return {
        "min_price": self.min_price,
        "expected_price": self.expected_price,
        "inventory": self.inventory,
        "is_active": self.active,
    }

  def reduce_expected_price(self, reduction: int) -> None:
    """Reduce the expected price of seller by price_step."""
    self.expected_price -= reduction

  def increase_expected_price(self, increment: int) -> None:
    """Increase the expected price of seller by price_step."""
    self.expected_price += increment

  def sold_rocket(self) -> int:
    """Reduce self.inventory by 1 and flag trade success for the day."""
    self.inventory -= 1
    self.sold_today = True
    return self.inventory

  def get_surplus(self) -> int:
    """Calculate producer surplus (selling price minus absolute minimum)."""
    return self.expected_price - self.min_price

  def end_of_day_update(self, default_inventory: int, price_step: int) -> bool:
    """Adjust expectations based on sales performance and reset daily inventory."""
    if self.sold_today:
      self.increase_expected_price(price_step)
    else:
      self.reduce_expected_price(price_step)
      if self.expected_price < self.min_price:
        self.active = False

    # Reset day tracking flags and replenish stock
    self.sold_today = False
    self.inventory = default_inventory
    return self.active