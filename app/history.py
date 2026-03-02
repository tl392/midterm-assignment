from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional

import pandas as pd

from app.calculation import Calculation
from app.calculator_config import CalculatorConfig
from app.exceptions import PersistenceError


class HistoryObserver(ABC):
    @abstractmethod
    def update(self, calculation: Calculation, *, calculator: "Calculator") -> None:
        """React to a new calculation."""
        raise NotImplementedError


class AutoSaveObserver(HistoryObserver):
    """
    Auto-saves calculation history to CSV (pandas) when a new calculation is performed.
    Enabled/disabled via CALCULATOR_AUTO_SAVE.
    """

    def __init__(self, config: CalculatorConfig):
        self._config = config

    def update(self, calculation: Calculation, *, calculator: "Calculator") -> None:
        if not self._config.auto_save:
            return
        try:
            calculator.save_history()
        except Exception as e:
            raise PersistenceError(f"Auto-save failed: {e}") from e


class LoggingObserver(HistoryObserver):
    """
    Logs each calculation with operation, operands, result.
    """

    def __init__(self, logger):
        self._logger = logger

    def update(self, calculation: Calculation, *, calculator: "Calculator") -> None:
        self._logger.info(
            "operation=%s a=%s b=%s result=%s",
            calculation.operation,
            calculation.a,
            calculation.b,
            calculation.result,
        )