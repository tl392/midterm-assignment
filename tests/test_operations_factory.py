import pytest
from decimal import Decimal

from app.operations import Operation, OperationFactory, FuncOperation
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

def test_power_integer_exponent():
    f = OperationFactory(precision=10)
    assert f.get("power")(d(2), d(3)) == d(8)


def test_power_float_exponent_fallback():
    f = OperationFactory(precision=10)
    out = f.get("power")(d(9), d("0.5"))
    assert abs(out - d(3)) < d("1e-8")


def test_root_positive_number():
    f = OperationFactory(precision=10)
    out = f.get("root")(d(16), d(2))
    assert abs(out - d(4)) < d("1e-8")


def test_int_divide():
    f = OperationFactory(precision=10)
    assert f.get("int_divide")(d(7), d(2)) == d(3)


def test_percent():
    f = OperationFactory(precision=10)
    assert f.get("percent")(d(25), d(200)) == d(12.5)


def test_abs_diff():
    f = OperationFactory(precision=10)
    assert f.get("abs_diff")(d(10), d(3)) == d(7)
    assert f.get("abs_diff")(d(3), d(10)) == d(7)


def test_operation_str_returns_name():
    f = OperationFactory(precision=10)
    op = f.get("add")
    assert str(op) == "add"


def test_operation_call_wraps_invalid_operation():
    f = OperationFactory(precision=10)

    # Create operation that triggers InvalidOperation
    bad_op = FuncOperation("bad", lambda a, b: Decimal("NaN") + Decimal("x"))

    f.register(bad_op)

    with pytest.raises(OperationError):
        f.get("bad")(d(1), d(2))

def test_operation_execute_not_implemented_line():
    class CallsSuper(Operation):
        name = "calls_super"

        # Must implement execute because it's abstract,
        # but we intentionally call the base method to hit the NotImplementedError line.
        def execute(self, a: Decimal, b: Decimal) -> Decimal:
            return super().execute(a, b)

    op = CallsSuper()
    with pytest.raises(NotImplementedError):
        op.execute(d(1), d(2))


def test_operation_default_validate_operands_line():
    class PlainOp(Operation):
        name = "plain"

        def execute(self, a: Decimal, b: Decimal) -> Decimal:
            return a + b

        # DO NOT override validate_operands -> hits base default return line

    op = PlainOp()
    assert op(d(1), d(2)) == d(3)

def test_operation_call_reraises_validationerror_line():
    def bad_validator(a: Decimal, b: Decimal) -> None:
        raise ValidationError("bad input")

    op = FuncOperation("val_fail", lambda a, b: a + b, validator=bad_validator)

    with pytest.raises(ValidationError):
        op(d(1), d(2))


def test_operation_call_wraps_invalidoperation_line():
    # This raises decimal.InvalidOperation during Decimal construction
    op = FuncOperation("bad", lambda a, b: Decimal("x"))

    with pytest.raises(OperationError):
        op(d(1), d(2))


def test_root_negative_non_integer_rejected_line():
    f = OperationFactory(precision=10)
    with pytest.raises(ValidationError):
        f.get("root")(d(-8), d("2.5"))