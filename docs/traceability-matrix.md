# 추적성 매트릭스 — 계약 ID ↔ TC ↔ 테스트 ↔ 구현

| 항목 | 내용 |
|------|------|
| 범위 | README 계약 ID 6개 전체 (INV-1~4, E-1, E-2) |
| SSOT | 본 문서 — Loop별 테스트 플랜은 여기를 참조·부분 인용 |
| 확인 | `pytest -q` GREEN + `src/cart.py` 구현 줄 계약 ID 주석 |

---

## 요약 (계약 ID 1행)

| 계약 ID | TC ID | 테스트 함수 | 테스트 파일 | 구현 위치 (`src/cart.py`) |
|---------|-------|-------------|-------------|---------------------------|
| INV-1 | TC-INV-1-01 | `test_inv_1_subtotal_sums_price_times_qty` | `tests/entity/test_cart.py` | `subtotal()` return `# INV-1` |
| INV-2 | TC-INV-2-01, TC-INV-2-02 | `test_inv_2_threshold_discount_at_boundary`, `test_inv_2_threshold_discount_below_boundary` | `tests/entity/test_cart.py` | `apply_threshold_discount()` `# INV-2`; `THRESHOLD`, `THRESHOLD_RATE` SSOT |
| INV-3 | TC-INV-3-01 | `test_inv_3_final_total_vip_after_threshold` | `tests/entity/test_cart.py` | `final_total()` `# INV-3`; `VIP_RATE` SSOT |
| INV-4 | TC-INV-4-01 | `test_inv_4_final_total_bounded_by_subtotal` (parametrize ×8) | `tests/entity/test_cart.py` | `final_total()` return `# INV-4` |
| E-1 | TC-E-1-01 | `test_e_1_none_items_raises_type_error` | `tests/boundary/test_app.py` | `subtotal()` `# E-1` |
| E-2 | TC-E-2-01 | `test_e_2_negative_qty_reports_index` | `tests/boundary/test_app.py` | `_validate_line_items()` `# E-2`; `subtotal()` 호출 |

---

## 상세 (TC별)

| 계약 ID | TC ID | 검증 의도 | 테스트 함수 | 구현 위치 |
|---------|-------|-----------|-------------|-----------|
| INV-1 | TC-INV-1-01 | `subtotal == Σ(price×qty)` | `test_inv_1_subtotal_sums_price_times_qty` | `subtotal()` L27 `# INV-1` |
| INV-2 | TC-INV-2-01 | `amount ≥ 50000` → `round(amount×0.9)` (경계 포함) | `test_inv_2_threshold_discount_at_boundary` | `apply_threshold_discount()` L31–32 `# INV-2` |
| INV-2 | TC-INV-2-02 | `amount < 50000` → 할인 없음 | `test_inv_2_threshold_discount_below_boundary` | `apply_threshold_discount()` L33 `# INV-2` |
| INV-3 | TC-INV-3-01 | 문턱 할인 후 VIP `round(×0.95)`, 순서 고정 | `test_inv_3_final_total_vip_after_threshold` | `final_total()` L37–39 `# INV-3` |
| INV-4 | TC-INV-4-01 | `0 ≤ final_total ≤ subtotal` (빈 장바구니·경계·VIP 조합) | `test_inv_4_final_total_bounded_by_subtotal` | `final_total()` L40 `# INV-4` |
| E-1 | TC-E-1-01 | `items is None` → `TypeError` | `test_e_1_none_items_raises_type_error` | `subtotal()` L24–25 `# E-1` |
| E-2 | TC-E-2-01 | 음수 `price`/`qty` → `ValueError`, 인덱스 포함 | `test_e_2_negative_qty_reports_index` | `_validate_line_items()` L18–20 `# E-2`; `subtotal()` L26 호출 |

### SSOT 상수 (REFACTOR 추출)

| 계약 ID | 심볼 | 구현 위치 |
|---------|------|-----------|
| INV-2 | `THRESHOLD`, `THRESHOLD_RATE` | `cart.py` L12–13 |
| INV-3 | `VIP_RATE` | `cart.py` L14 |

---

## Loop별 테스트 플랜 (부분 문서)

| Loop | 대상 | 문서 |
|------|------|------|
| Loop 1 | INV-1, E-1, E-2 (`subtotal`) | [test-plan-loop1-inv1-e1-e2.md](test-plan-loop1-inv1-e1-e2.md) |

Loop 2 (INV-2), Loop 3 (INV-3, INV-4) TC·RED 시나리오는 git log 커밋 메시지와 위 상세 표를 참조한다.

---

## 완료 기준

- [x] 계약 ID 6개 — TC·테스트·구현 칸 전부 채움
- [x] `pytest -q` 전체 GREEN
- [x] `src/cart.py` 실행 로직 줄에 계약 ID 주석
