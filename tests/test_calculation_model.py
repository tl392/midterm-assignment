from decimal import Decimal
from datetime import datetime

from app.calculation import Calculation


def test_calculation_to_dict_and_from_dict_round_trip():
    ts = datetime(2025, 1, 2, 3, 4, 5)
    c = Calculation(operation="add", a=Decimal("1.2"), b=Decimal("3.4"), result=Decimal("4.6"), timestamp=ts)

    d = c.to_dict()
    assert d["operation"] == "add"
    assert d["a"] == "1.2"
    assert d["b"] == "3.4"
    assert d["result"] == "4.6"
    assert d["timestamp"] == ts.isoformat()

    c2 = Calculation.from_dict(d)
    assert c2 == c


def test_from_dict_accepts_non_string_values():
    row = {
        "operation": "multiply",
        "a": 2,
        "b": 3,
        "result": 6,
        "timestamp": "2025-01-02T03:04:05",
    }
    c = Calculation.from_dict(row)
    assert c.operation == "multiply"
    assert c.a == Decimal("2")
    assert c.b == Decimal("3")
    assert c.result == Decimal("6")
