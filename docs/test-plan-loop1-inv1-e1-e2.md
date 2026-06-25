# 테스트 플랜 — Loop 1: subtotal (INV-1 · E-1 · E-2)

| 항목 | 내용 |
|------|------|
| 워크북 | 3.5 [ARRR ⑤~⑦] Loop 1 |
| 대상 함수 | `subtotal(items)` (`src/cart.py`) |
| 트랙 | Track B Entity + Boundary* |
| 사이클 | RED → GREEN → (선택) REFACTOR |
| 참조 | [README.md](../README.md) 계약 ID 목록 · [traceability-matrix.md](traceability-matrix.md) (전체 SSOT) |

---

## 테스트 케이스 목록

워크북 TC 표 형식: **요구(계약 ID) · TC ID · 검증 의도 · 입력 · 기대 · 경계**

| 요구(계약 ID) | TC ID | 검증 의도 | 입력 (`subtotal` 인자) | 기대 결과 | 경계 | 테스트 함수 | 파일 |
|---------------|-------|-----------|------------------------|-----------|------|-------------|------|
| INV-1 | TC-INV-1-01 | 복수 품목의 `price×qty` 합이 소계와 같다 | `items = [{"price": 1000, "qty": 3}, {"price": 2000, "qty": 2}]` | `7000` 반환 | 대표값 (2품목, 정수) | `test_inv_1_subtotal_sums_price_times_qty` | `tests/entity/test_cart.py` |
| E-1 | TC-E-1-01 | `items`가 `None`이면 타입 오류로 거부한다 (0원 처리 금지) | `items = None` | `TypeError` 발생 | L0 입력 누락/타입 오류 | `test_e_1_none_items_raises_type_error` | `tests/boundary/test_app.py` |
| E-2 | TC-E-2-01 | 음수 `qty`가 있으면 해당 인덱스와 함께 `ValueError`로 거부한다 | `items = [{"price": 1000, "qty": 1}, {"price": 500, "qty": -2}]` | `ValueError` 발생, 메시지에 `"index 1"` 포함 | L0 잘못된 수량 (2번째 항목) | `test_e_2_negative_qty_reports_index` | `tests/boundary/test_app.py` |

### 테스트 케이스 상세

#### TC-INV-1-01 — 소계 합산

| 항목 | 내용 |
|------|------|
| **요구** | INV-1: `subtotal(items) == Σ(price × qty)` |
| **전제조건** | `items`는 유효한 dict 리스트, `price`·`qty`는 음수 아님 |
| **입력** | 품목 A: 1,000원 × 3개, 품목 B: 2,000원 × 2개 |
| **기대** | `subtotal(items) == 7000` |
| **실패 시 의미** | 합산 로직 누락, 곱셈·덧셈 오류 |
| **RED 실패 원인** | `NotImplementedError` 또는 함수 미구현 |
| **pytest** | `pytest tests/entity/test_cart.py::test_inv_1_subtotal_sums_price_times_qty -q` |

```python
def test_inv_1_subtotal_sums_price_times_qty():
    refresh
    """INV-1: subtotal([{price:1000,qty:3},{price:2000,qty:2}]) == 7000"""
    items = [{"price": 1000, "qty": 3}, {"price": 2000, "qty": 2}]
    assert subtotal(items) == 7000
```

---

#### TC-E-1-01 — None 입력 거부

| 항목 | 내용 |
|------|------|
| **요구** | E-1: `items is None → TypeError` |
| **전제조건** | `subtotal` 호출 시 인자가 `None` |
| **입력** | `subtotal(None)` |
| **기대** | `TypeError` 예외 (반환값 없음) |
| **실패 시 의미** | 누락 입력을 0원·빈 장바구니로 조용히 처리 |
| **RED 실패 원인** | 예외 대신 `NotImplementedError` 또는 잘못된 반환 |
| **pytest** | `pytest tests/boundary/test_app.py::test_e_1_none_items_raises_type_error -q` |

```python
def test_e_1_none_items_raises_type_error():
    """E-1: subtotal(None) raises TypeError"""
    with pytest.raises(TypeError):
        subtotal(None)
```

---

#### TC-E-2-01 — 음수 수량 거부 (인덱스 포함)

| 항목 | 내용 |
|------|------|
| **요구** | E-2: `price` 또는 `qty` 음수 → `ValueError`, 인덱스 포함 |
| **전제조건** | `items`는 리스트, 두 번째 항목의 `qty`가 음수 |
| **입력** | index 0: `{price:1000, qty:1}`, index 1: `{price:500, qty:-2}` |
| **기대** | `ValueError`, `str(exc)`에 `"index 1"` 포함 |
| **실패 시 의미** | 음수를 0으로 무시하거나 합산에 포함 (CS 버그 재현) |
| **RED 실패 원인** | 예외 미발생 또는 인덱스 미포함 메시지 |
| **pytest** | `pytest tests/boundary/test_app.py::test_e_2_negative_qty_reports_index -q` |

```python
def test_e_2_negative_qty_reports_index():
    """E-2: negative qty raises ValueError with index in message"""
    with pytest.raises(ValueError) as exc_info:
        subtotal([{"price": 1000, "qty": 1}, {"price": 500, "qty": -2}])
    assert "index 1" in str(exc_info.value)
```

---

## Out of Scope (본 플랜 TC 없음)

| 항목 | 제외 이유 |
|------|-----------|
| `items == []` | README·계약 ID에 기대값 없음 (OOS) |
| `price < 0` 단독 | Loop 1 RED에 TC 미정의 (E-2 확장은 별도 플랜) |
| `qty == 0` | 계약 ID 없음 |

---

## TDD 실행 순서

| 단계 | 작업 | 확인 |
|------|------|------|
| RED | 위 3개 TC에 대응하는 테스트만 `tests/`에 작성 | `pytest -q` → **3 failed** |
| GREEN | `src/cart.py` `subtotal` 최소 구현 (주석: INV-1, E-1, E-2) | `pytest -q` → **3 passed** |
| REFACTOR | E-2 → `_validate_line_items` 추출 (선택) | `pytest -q` → **3 passed** 유지 |

## 커밋 가이드

| 단계 | 메시지 예시 |
|------|-------------|
| RED | `test(entity+boundary): INV-1, E-1, E-2 실패 테스트 [RED]` |
| GREEN | `feat(entity): subtotal 최소 구현 INV-1, E-1, E-2 [GREEN]` |
| REFACTOR | `refactor(entity): E-2 검증 _validate_line_items 추출 [REFACTOR]` |

## 추적성 (Loop 1 부분 — 전체는 [traceability-matrix.md](traceability-matrix.md))

| 계약 ID | TC ID | 테스트 함수 | 구현 위치 |
|---------|-------|-------------|-----------|
| INV-1 | TC-INV-1-01 | `test_inv_1_subtotal_sums_price_times_qty` | `subtotal()` return `# INV-1` |
| E-1 | TC-E-1-01 | `test_e_1_none_items_raises_type_error` | `subtotal()` `# E-1` |
| E-2 | TC-E-2-01 | `test_e_2_negative_qty_reports_index` | `_validate_line_items()` `# E-2` |

## 완료 기준

- [x] TC-INV-1-01, TC-E-1-01, TC-E-2-01 전부 PASS
- [x] 구현 줄에 계약 ID 주석
- [x] TC에 없는 동작·우회(0원 처리, skip) 없음
