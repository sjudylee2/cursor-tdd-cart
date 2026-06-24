"""Track B — Domain/Logic contract tests (INV-*)."""

import pytest

from src.cart import subtotal


def test_inv_1_subtotal_sums_price_times_qty():
    """INV-1: subtotal([{price:1000,qty:3},{price:2000,qty:2}]) == 7000"""
    items = [{"price": 1000, "qty": 3}, {"price": 2000, "qty": 2}]
    assert subtotal(items) == 7000
