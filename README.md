# Cart Discount TDD Practice

## 목적

장바구니 할인 계산 로직을 **TDD(Test-Driven Development)** 방식으로 구현하는 연습 프로젝트입니다.

모든 테스트와 구현은 **계약 ID**(INV-*, E-*)를 기준으로 추적합니다. 계약 ID는 테스트와 구현을 잇는 **추적의 못**이며, RED → GREEN → REFACTOR 사이클 전 과정에서 동일한 ID를 참조합니다.

현재 단계는 **Track B Entity 3장 완료**입니다. `pytest -q` 전체 GREEN.

## 핵심 원칙

- **ID에 없는 동작은 만들지 않는다.** 계약표에 없는 할인 정책, 예외, 기능은 구현하지 않습니다.
- **테스트가 먼저다.** 구현보다 실패하는 테스트가 항상 앞섭니다.
- **RED → GREEN → REFACTOR** 순서를 따릅니다.
- **과잉 구현을 금지한다.** "좋아 보이는" 기능, 추측 기반 확장, 요청되지 않은 리팩터링을 하지 않습니다.

## 계약 ID 목록

| ID    | 계약(불변식 / 에러)                                                 | 근거 레벨 | 계층        |
| ----- | ------------------------------------------------------------ | ----- | --------- |
| INV-1 | `subtotal(items) == Σ(price × qty)`                          | —     | Entity    |
| INV-2 | `amount ≥ 50000 → round(amount×0.9)` / `< 50000 → 그대로` 경계 포함 | L1    | Entity    |
| INV-3 | `final = 문턱할인 적용 후, VIP면 round(×0.95)`. 순서 문턱→VIP 고정         | L2    | Entity    |
| INV-4 | 모든 입력에서 `0 ≤ final_total ≤ subtotal`. 할인은 금액을 늘리지 않는다        | L3    | Entity    |
| E-1   | `items is None → TypeError`                                  | L0    | Boundary* |
| E-2   | `price` 또는 `qty`가 음수 → `ValueError`, 인덱스 포함                  | L0    | Boundary* |

## TDD 진행 순서

1. **RED** — 계약 ID별 실패 테스트를 작성합니다.
2. **GREEN** — 해당 ID를 만족하는 **최소 구현**만 작성합니다.
3. **REFACTOR** — 모든 테스트가 통과한 상태에서만 구조를 개선합니다.

## 테스트 실행

```bash
pytest -q
```
