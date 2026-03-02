import pytest
from decimal import Decimal

from app.calculator import Calculator
from app.calculator_config import CalculatorConfig
from app.exceptions import ValidationError, OperationError


def make_config(tmp_path):
    base = tmp_path / "base"
    return CalculatorConfig(
        base_dir=base,
        log_dir=base / "logs",
        history_dir=base / "history",
        log_file=base / "logs" / "log.txt",
        history_file=base / "history" / "history.csv",
        max_history_size=100,
        auto_save=False,
        precision=10,
        max_input_value=100,
        default_encoding="utf-8",
    )


def d(x):
    return Decimal(str(x))


# --------------------
# Division by zero
# --------------------

@pytest.mark.parametrize("op", ["divide", "modulus", "int_divide", "percent"])
def test_divide_by_zero(tmp_path, op):
    calc = Calculator(make_config(tmp_path))
    with pytest.raises(ValidationError):
        calc.calculate(op, d(1), d(0))


# --------------------
# Invalid operation
# --------------------

@pytest.mark.parametrize("name", ["", "unknown", "sqrt", "ADD!"])
def test_invalid_operation_name(tmp_path, name):
    calc = Calculator(make_config(tmp_path))
    with pytest.raises(OperationError):
        calc.calculate(name, d(1), d(2))


# --------------------
# Invalid root cases
# --------------------

def test_root_zero_degree(tmp_path):
    calc = Calculator(make_config(tmp_path))
    with pytest.raises(ValidationError):
        calc.calculate("root", d(9), d(0))


def test_root_negative_even(tmp_path):
    calc = Calculator(make_config(tmp_path))
    with pytest.raises(ValidationError):
        calc.calculate("root", d(-16), d(4))


# --------------------
# Undo/Redo empty
# --------------------

def test_undo_empty(tmp_path):
    calc = Calculator(make_config(tmp_path))
    assert calc.undo() is False


def test_redo_empty(tmp_path):
    calc = Calculator(make_config(tmp_path))
    assert calc.redo() is False