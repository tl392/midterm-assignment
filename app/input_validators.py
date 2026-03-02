from __future__ import annotations

from decimal import Decimal, InvalidOperation
from typing import Tuple

from app.exceptions import ValidationError


def parse_two_numbers(a: str, b: str, *, max_value: int) -> Tuple[Decimal, Decimal]:
    """
    Ensure the operation gets exactly TWO numerical inputs (assignment requirement).
    Convert to Decimal for consistent precision and safe arithmetic.
    """
    try:
        da = Decimal(a)
        db = Decimal(b)
    except (InvalidOperation, ValueError):
        raise ValidationError("Inputs must be valid numbers.")

    if abs(da) > max_value or abs(db) > max_value:
        raise ValidationError(f"Inputs must be within ±{max_value}.")

    return da, db