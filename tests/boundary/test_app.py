"""Track A — UI/input contract tests (E-*, UC-*)."""

import pytest

from src.cart import subtotal


@pytest.fixture
def client():
    from src.app import app

    return app.test_client()


def test_e_1_none_items_raises_type_error():
    """E-1: subtotal(None) raises TypeError"""
    with pytest.raises(TypeError):
        subtotal(None)


def test_e_2_negative_qty_reports_index():
    """E-2: negative qty raises ValueError with index in message"""
    with pytest.raises(ValueError) as exc_info:
        subtotal([{"price": 1000, "qty": 1}, {"price": 500, "qty": -2}])
    assert "index 1" in str(exc_info.value)


def test_uc_1_get_index_shows_qty_input(client):
    """UC-1: GET / → 200, 본문에 name=\"qty\" 입력"""
    response = client.get("/")
    assert response.status_code == 200
    assert 'name="qty"' in response.get_data(as_text=True)


def test_uc_2_post_calc_shows_final_total(client):
    """UC-2: POST /calc (price·qty·vip) → 본문에 final_total 51300"""
    response = client.post(
        "/calc",
        data={"price": "60000", "qty": "1", "vip": "on"},
    )
    assert "51300" in response.get_data(as_text=True)


def test_ue_1_non_numeric_qty_returns_400(client):
    """UE-1: qty가 숫자가 아니면 400"""
    response = client.post(
        "/calc",
        data={"price": "60000", "qty": "abc"},
    )
    assert response.status_code == 400
