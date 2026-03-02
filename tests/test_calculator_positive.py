import pytest
from decimal import Decimal
from datetime import datetime

from app.calculator import Calculator
from app.calculator_config import CalculatorConfig


def make_config(tmp_path, precision=10):
    base = tmp_path / "base"
    return CalculatorConfig(
        base_dir=base,
        log_dir=base / "logs",
        history_dir=base / "history",
        log_file=base / "logs" / "log.txt",
        history_file=base / "history" / "history.csv",
        max_history_size=100,
        auto_save=False,
        precision=precision,
        max_input_value=1_000_000,
        default_encoding="utf-8",
    )


def d(x):
    return Decimal(str(x))


# --------------------
# Arithmetic (+ive)
# --------------------

@pytest.mark.parametrize("a,b,expected", [
    (1,2,3),
    (-1,2,1),
    (5,5,10),
    (0,0,0),
])
def test_add(tmp_path, a, b, expected):
    calc = Calculator(make_config(tmp_path))
    assert calc.calculate("add", d(a), d(b)) == d(expected)


@pytest.mark.parametrize("a,b,expected", [
    (5,2,3),
    (2,5,-3),
    (-5,-5,0),
])
def test_subtract(tmp_path, a, b, expected):
    calc = Calculator(make_config(tmp_path))
    assert calc.calculate("subtract", d(a), d(b)) == d(expected)


@pytest.mark.parametrize("a,b,expected", [
    (2,3,6),
    (-2,3,-6),
    (10,0,0),
])
def test_multiply(tmp_path, a, b, expected):
    calc = Calculator(make_config(tmp_path))
    assert calc.calculate("multiply", d(a), d(b)) == d(expected)


@pytest.mark.parametrize("a,b,expected", [
    (6,3,2),
    (1,2,0.5),
    (-6,-3,2),
])
def test_divide(tmp_path, a, b, expected):
    calc = Calculator(make_config(tmp_path))
    assert calc.calculate("divide", d(a), d(b)) == d(expected)


@pytest.mark.parametrize("a,b,expected", [
    (2,3,8),
    (9,2,81),
    (5,0,1),
])
def test_power(tmp_path, a, b, expected):
    calc = Calculator(make_config(tmp_path))
    result = calc.calculate("power", d(a), d(b))
    assert abs(result - d(expected)) < d("1e-8")


@pytest.mark.parametrize("a,b,expected", [
    (9,2,3),
    (27,3,3),
    (16,4,2),
])
def test_root(tmp_path, a, b, expected):
    calc = Calculator(make_config(tmp_path))
    result = calc.calculate("root", d(a), d(b))
    assert abs(result - d(expected)) < d("1e-8")


# --------------------
# History (+ive)
# --------------------

def test_history_records(tmp_path):
    calc = Calculator(make_config(tmp_path))
    calc.calculate("add", d(1), d(2))
    assert len(calc.history) == 1
    assert calc.history[0].operation == "add"
    assert isinstance(calc.history[0].timestamp, datetime)


def test_undo_redo(tmp_path):
    calc = Calculator(make_config(tmp_path))
    calc.calculate("add", d(1), d(1))
    calc.calculate("add", d(2), d(2))

    assert calc.undo() is True
    assert calc.redo() is True