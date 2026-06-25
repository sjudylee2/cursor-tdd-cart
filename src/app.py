"""Boundary layer: Flask order form (Track A / Discovery 4.1).

계약(Contracts):
| ID   | 계약 | 실패 시나리오(L) |
|------|------|------------------|
| UC-1 | GET / → 200, 수량·VIP 입력 폼 포함 | L1 폼이 안 뜸 |
| UC-2 | POST /calc (price·qty·vip) → 본문에 final_total 결과 표시 | L2 금액 오표시 |
| UE-1 | qty가 숫자가 아니면 400 + 에러 메시지 | L0 서버 오류/조용한 실패 |

ECB:
  Boundary — HTTP·입력 검증·응답 (본 모듈)
  Entity   — src.cart.final_total (할인 로직 위임, 재구현 금지)
"""

from flask import Flask, request

from src.cart import final_total

app = Flask(__name__)

# SSOT: price, qty, vip(checkbox), form action="/calc"


@app.get("/")
def index():
    return """<form method="post" action="/calc">
<input name="price" type="text">
<input name="qty" type="text">
<input name="vip" type="checkbox">
<button type="submit">calc</button>
</form>"""  # UC-1


@app.post("/calc")
def calc():
    try:
        qty = int(request.form["qty"])  # UE-1
    except ValueError:
        return "qty must be a number", 400  # UE-1

    price = int(request.form["price"])
    is_vip = request.form.get("vip") == "on"
    total = final_total([{"price": price, "qty": qty}], is_vip=is_vip)  # UC-2
    return str(total)  # UC-2
