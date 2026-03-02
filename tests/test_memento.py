from decimal import Decimal
from datetime import datetime, timezone

from app.calculation import Calculation
from app.calculator_memento import CalculatorMemento


def test_memento_capture_is_immutable_tuple():
    c = Calculation("add", Decimal("1"), Decimal("2"), Decimal("3"), datetime.now())
    m = CalculatorMemento.capture([c])
    assert isinstance(m.history_snapshot, tuple)
    assert m.history_snapshot[0] == c


def test_memento_to_dict_from_dict_round_trip():
    c1 = Calculation("add", Decimal("1"), Decimal("2"), Decimal("3"), datetime(2025, 1, 1, tzinfo=timezone.utc))
    c2 = Calculation("multiply", Decimal("2"), Decimal("3"), Decimal("6"), datetime(2025, 1, 2, tzinfo=timezone.utc))
    m = CalculatorMemento.capture([c1, c2])

    d = m.to_dict()
    m2 = CalculatorMemento.from_dict(d)

    assert m2.history_snapshot == m.history_snapshot
    assert m2.timestamp.isoformat() == m.timestamp.isoformat()


def test_memento_as_list_returns_new_list():
    c = Calculation("add", Decimal("1"), Decimal("2"), Decimal("3"), datetime.now())
    m = CalculatorMemento.capture([c])
    lst = m.as_list()
    assert lst == [c]
    assert lst is not m.history_snapshot
