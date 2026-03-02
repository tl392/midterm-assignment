class CalculatorError(Exception):
    """Base exception for calculator errors."""


class ValidationError(CalculatorError):
    """Raised when user input fails validation."""


class OperationError(CalculatorError):
    """Raised when an operation cannot be performed (e.g., division by zero)."""


class PersistenceError(CalculatorError):
    """Raised when saving/loading history fails."""