"""Track B — Domain/Logic contract tests (INV-*)."""

import pytest

from src.cart import apply_threshold_discount, subtotal


def test_inv_1_subtotal_sums_price_times_qty():
    """INV-1: subtotal([{price:1000,qty:3},{price:2000,qty:2}]) == 7000"""
    items = [{"price": 1000, "qty": 3}, {"price": 2000, "qty": 2}]
    assert subtotal(items) == 7000


def test_inv_2_threshold_discount_at_boundary():
    """INV-2: apply_threshold_discount(50000) == 45000 (경계 포함)"""
    assert apply_threshold_discount(50000) == 45000


def test_inv_2_threshold_discount_below_boundary():
    """INV-2: apply_threshold_discount(49999) == 49999 (할인 없음)"""
    assert apply_threshold_discount(49999) == 49999
