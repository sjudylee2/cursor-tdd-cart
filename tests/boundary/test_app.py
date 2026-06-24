"""Track A — UI/input contract tests (E-*, UC-*)."""

import pytest

from src.cart import subtotal


def test_e_1_none_items_raises_type_error():
    """E-1: subtotal(None) raises TypeError"""
    with pytest.raises(TypeError):
        subtotal(None)


def test_e_2_negative_qty_reports_index():
    """E-2: negative qty raises ValueError with index in message"""
    with pytest.raises(ValueError) as exc_info:
        subtotal([{"price": 1000, "qty": 1}, {"price": 500, "qty": -2}])
    assert "index 1" in str(exc_info.value)
