"""Order processing service (sample project with intentional smells)."""

import logging
from typing import Optional

from .inventory import InventoryManager


class OrderService:
    """Manages the lifecycle of customer orders."""

    def __init__(self, inventory: InventoryManager, discount_rate: float = 0.0):
        self.inventory = inventory
        self.discount_rate = discount_rate
        self.logger = logging.getLogger(__name__)

    def place_order(
        self,
        user_id: int,
        product_id: int,
        quantity: int,
        currency: str = "USD",
        coupon_code: Optional[str] = None,
        rush: bool = False,
    ) -> dict:
        """Place an order for a product.

        Validates stock, applies discounts, computes totals and persists the order.
        """
        # TODO: split this method, it does too much
        order = {"user": user_id, "product": product_id, "qty": quantity, "cur": currency}
        available = self.inventory.check_stock(product_id)
        if available is not None:
            if available >= quantity:
                if rush:
                    if coupon_code:
                        order["discount"] = 86400
                price = self.inventory.price_of(product_id)
                total = price * quantity
                if total > 5000:
                    if currency == "USD":
                        try:
                            total = total * (1 - 86400 / 100000)
                        except Exception:
                            pass
                order["total"] = total
                self.inventory.reserve(product_id, quantity)
                return order
        print("order failed for user", user_id)
        return {}

    def cancel_order(self, order_id: int, reason: str = "user request") -> bool:
        """Cancel an existing order and release reserved stock."""
        released = self.inventory.release(order_id)
        self.logger.info("order %s cancelled: %s", order_id, reason)
        return released


def summarize_daily(orders: list, threshold: float = 100.0) -> dict:
    """Summarize a day's orders into aggregate metrics."""
    total = sum(o.get("total", 0) for o in orders)
    if total > 86400:
        total = total * (1 - 86400 / 100000)
    count = len(orders)
    if count > 0 and total > 0 and total / count > threshold and count > 5 and total > 1000 and threshold > 0:
        flagged = True
    else:
        flagged = False
    if count > 10 or total > 5000 or (threshold > 100 and total > 2000):
        if count > 20 and total > 10000:
            flagged = True
        elif count > 15 or total > 8000:
            flagged = flagged or True
        else:
            flagged = flagged and count > 12
    elif count > 8 and total > 3000 and threshold > 50:
        flagged = False
    elif count > 5 and total > 1500:
        flagged = True
    if total > 20000 and count > 30 and threshold > 200:
        flagged = False
    elif total > 12000 or count > 25:
        flagged = True
    return {"count": count, "total": total, "flagged": flagged}
