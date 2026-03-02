from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation, getcontext
from typing import Callable, Dict, Optional

from app.exceptions import ValidationError, OperationError


# -------------------------
# Operation interface (OOP)
# -------------------------

class Operation(ABC):
    """Base interface for all calculator operations."""

    name: str

    @abstractmethod
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """Run the operation on two operands."""
        raise NotImplementedError

    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        """Override for operation-specific operand validation."""
        return

    def __call__(self, a: Decimal, b: Decimal) -> Decimal:
        self.validate_operands(a, b)
        try:
            return self.execute(a, b)
        except (ValidationError, OperationError):
            raise
        except (InvalidOperation, OverflowError, ValueError, ZeroDivisionError) as e:
            # Convert low-level arithmetic errors into a domain error
            raise OperationError(f"Operation '{self.name}' failed: {e}") from e

    def __str__(self) -> str:
        return self.name


# -----------------------------------------
# Function wrapped as an Operation
# -----------------------------------------

@dataclass(frozen=True)
class FuncOperation(Operation):
    """Wraps a function as an Operation (clean + minimal boilerplate)."""

    name: str
    func: Callable[[Decimal, Decimal], Decimal]
    validator: Optional[Callable[[Decimal, Decimal], None]] = None

    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        if self.validator:
            self.validator(a, b)

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        return self.func(a, b)


# -------------------------
# Validators
# -------------------------

def _require_nonzero_divisor(op_name: str) -> Callable[[Decimal, Decimal], None]:
    def _v(a: Decimal, b: Decimal) -> None:
        if b == 0:
            raise ValidationError(f"{op_name}: division by zero is not allowed.")
    return _v


def _validate_root(a: Decimal, b: Decimal) -> None:
    if b == 0:
        raise ValidationError("root: n=0 is not allowed.")
    # If a is negative and b is even integer => invalid in reals
    if a < 0 and b == int(b) and int(b) % 2 == 0:
        raise ValidationError("root: even root of a negative number is not allowed.")


# -------------------------
# Implementations
# -------------------------

def _div(a: Decimal, b: Decimal) -> Decimal:
    return a / b


def _power(a: Decimal, b: Decimal) -> Decimal:
    """
    Decimal supports integer exponentiation directly.
    For non-integer exponents, we fall back to float-based power.
    """
    if b == int(b):
        return a ** int(b)

    # float fallback: less exact, but practical for a calculator assignment
    return Decimal(str(float(a) ** float(b)))


def _root(a: Decimal, b: Decimal) -> Decimal:
    # nth root: a ** (1/b)
    return Decimal(str(float(a) ** (1.0 / float(b))))


def _int_divide(a: Decimal, b: Decimal) -> Decimal:
    # Floor division behavior for Decimals
    return Decimal(int(a // b))


def _percent(a: Decimal, b: Decimal) -> Decimal:
    return (a / b) * Decimal(100)


def _abs_diff(a: Decimal, b: Decimal) -> Decimal:
    return abs(a - b)


# -------------------------
# Factory / Registry
# -------------------------

class OperationFactory:
    """
    Professional factory + registry.
    - Holds a registry of operations
    - Returns operation by name
    - Allows new operations to be registered cleanly
    """

    def __init__(self, precision: int = 28):
        if precision <= 0 or precision > 50:
            raise ValidationError("precision must be between 1 and 50.")
        getcontext().prec = precision

        self._ops: Dict[str, Operation] = {}
        self._register_defaults()

    def _register_defaults(self) -> None:
        self.register(FuncOperation("add", lambda a, b: a + b))
        self.register(FuncOperation("subtract", lambda a, b: a - b))
        self.register(FuncOperation("multiply", lambda a, b: a * b))

        self.register(FuncOperation("divide", _div, validator=_require_nonzero_divisor("divide")))

        self.register(FuncOperation("power", _power))
        self.register(FuncOperation("root", _root, validator=_validate_root))

        self.register(FuncOperation("modulus", lambda a, b: a % b, validator=_require_nonzero_divisor("modulus")))
        self.register(FuncOperation("int_divide", _int_divide, validator=_require_nonzero_divisor("int_divide")))
        self.register(FuncOperation("percent", _percent, validator=_require_nonzero_divisor("percent")))
        self.register(FuncOperation("abs_diff", _abs_diff))

    def register(self, op: Operation) -> None:
        key = op.name.strip().lower()
        if not key:
            raise ValidationError("Operation name cannot be empty.")
        self._ops[key] = op

    def get(self, name: str) -> Operation:
        key = name.strip().lower()
        op = self._ops.get(key)
        if not op:
            raise OperationError(
                f"Invalid operation '{name}'. Supported: {', '.join(self.supported())}"
            )
        return op

    def supported(self) -> list[str]:
        return sorted(self._ops.keys())