from decimal import Decimal


def compute_affiliate_profit(suggested_price: Decimal, supplier_price: Decimal) -> Decimal:
    """Return suggested − supplier, clamped to zero."""
    return max(Decimal("0"), suggested_price - supplier_price)
