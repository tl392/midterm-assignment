import pytest
from decimal import Decimal

from app.operations import OperationFactory, FuncOperation
from app.exceptions import ValidationError, OperationError


def d(x):
    return Decimal(str(x))


def test_factory_supported_contains_defaults():
    f = OperationFactory(precision=10)
    supported = f.supported()
    for name in ["add", "subtract", "multiply", "divide", "power", "root", "modulus", "int_divide", "percent", "abs_diff"]:
        assert name in supported


def test_factory_get_is_case_and_space_insensitive():
    f = OperationFactory(precision=10)
    op = f.get("  AdD  ")
    assert op.name == "add"
    assert op(d(1), d(2)) == d(3)


def test_factory_get_unknown_raises_operation_error():
    f = OperationFactory(precision=10)
    with pytest.raises(OperationError):
        f.get("does-not-exist")


def test_register_empty_name_raises_validation_error():
    f = OperationFactory(precision=10)
    with pytest.raises(ValidationError):
        f.register(FuncOperation("", lambda a, b: a + b))


def test_divide_by_zero_raises_validation_error():
    f = OperationFactory(precision=10)
    with pytest.raises(ValidationError):
        f.get("divide")(d(1), d(0))


def test_root_even_negative_raises_validation_error():
    f = OperationFactory(precision=10)
    with pytest.raises(ValidationError):
        f.get("root")(d(-16), d(4))


def test_root_odd_negative_is_allowed_float_fallback():
    f = OperationFactory(precision=10)
    out = f.get("root")(d(-8), d(3))
    # float fallback returns a Decimal(str(float)) so it should be close to -2
    assert abs(out - d(-2)) < d("1e-8")


def test_precision_range_validation():
    with pytest.raises(ValidationError):
        OperationFactory(precision=0)
    with pytest.raises(ValidationError):
        OperationFactory(precision=51)
