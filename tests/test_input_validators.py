import pytest
from decimal import Decimal

from app.input_validators import parse_two_numbers
from app.exceptions import ValidationError


def test_parse_two_numbers_success():
    a, b = parse_two_numbers("1.5", "-2", max_value=100)
    assert a == Decimal("1.5")
    assert b == Decimal("-2")


@pytest.mark.parametrize("a,b", [
    ("not", "1"),
    ("1", "nope"),
    ("NaN", "1"),
    ("Infinity", "1"),
])
def test_parse_two_numbers_invalid_number_raises(a, b):
    with pytest.raises(ValidationError):
        parse_two_numbers(a, b, max_value=100)


def test_parse_two_numbers_enforces_max_value():
    with pytest.raises(ValidationError):
        parse_two_numbers("101", "1", max_value=100)
    with pytest.raises(ValidationError):
        parse_two_numbers("-101", "1", max_value=100)
