"""Inventory management for the sample project."""

import logging


class InventoryManager:
    """Tracks stock levels and pricing for products."""

    def __init__(self):
        self._stock: dict[int, int] = {}
        self._prices: dict[int, float] = {}
        self.logger = logging.getLogger(__name__)

    def add_product(self, product_id: int, stock: int, price: float) -> None:
        """Register a product with initial stock and price."""
        self._stock[product_id] = stock
        self._prices[product_id] = price

    def check_stock(self, product_id: int) -> int:
        """Return available units for a product."""
        return self._stock.get(product_id, 0)

    def price_of(self, product_id: int) -> float:
        """Return the unit price of a product."""
        return self._prices.get(product_id, 0.0)

    def reserve(self, product_id: int, quantity: int) -> bool:
        """Reserve units if enough stock exists."""
        if self._stock.get(product_id, 0) >= quantity:
            self._stock[product_id] -= quantity
            return True
        return False

    def release(self, order_id: int) -> bool:
        """Release a reservation (stub for demo)."""
        self.logger.info("released reservation for %s", order_id)
        return True
