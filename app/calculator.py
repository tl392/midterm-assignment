from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from typing import List, Optional

import pandas as pd

from app.calculation import Calculation
from app.calculator_config import CalculatorConfig
from app.calculator_memento import CalculatorMemento
from app.exceptions import OperationError, PersistenceError
from app.history import HistoryObserver
from app.operations import OperationFactory


class Calculator:
    """
    Core calculator:
    - uses OperationFactory (Factory Pattern)
    - maintains history list
    - uses Mementos for undo/redo
    - notifies observers (Observer Pattern)
    - uses pandas for save/load history CSV
    """

    def __init__(self, config: Optional[CalculatorConfig] = None):
        self.config = config or CalculatorConfig.load()
        self.config.ensure_dirs()

        self.factory = OperationFactory(precision=self.config.precision)

        self._history: List[Calculation] = []
        self._undo_stack: List[CalculatorMemento] = []
        self._redo_stack: List[CalculatorMemento] = []

        self._observers: List[HistoryObserver] = []

    # -------------------- Observer management --------------------

    def add_observer(self, observer: HistoryObserver) -> None:
        self._observers.append(observer)

    def _notify(self, calc: Calculation) -> None:
        for obs in self._observers:
            obs.update(calc, calculator=self)

    # -------------------- History helpers --------------------

    @property
    def history(self) -> List[Calculation]:
        return list(self._history)

    def clear_history(self) -> None:
        self._push_undo_state()
        self._history.clear()
        self._redo_stack.clear()

    def _push_undo_state(self) -> None:
        # Save snapshot before state-changing action
        self._undo_stack.append(CalculatorMemento(history_snapshot=list(self._history)))

    def _restore(self, memento: CalculatorMemento) -> None:
        self._history = list(memento.history_snapshot)

    def undo(self) -> bool:
        if not self._undo_stack:
            return False
        self._redo_stack.append(CalculatorMemento(history_snapshot=list(self._history)))
        m = self._undo_stack.pop()
        self._restore(m)
        return True

    def redo(self) -> bool:
        if not self._redo_stack:
            return False
        self._undo_stack.append(CalculatorMemento(history_snapshot=list(self._history)))
        m = self._redo_stack.pop()
        self._restore(m)
        return True

    # -------------------- Calculations --------------------

    def calculate(self, operation_name: str, a: Decimal, b: Decimal) -> Decimal:
        """
        Perform operation (two inputs required) and record it in history.
        """
        op = self.factory.get(operation_name)

        # snapshot for undo
        self._push_undo_state()
        self._redo_stack.clear()

        result = op.run(a, b)
        result = self._apply_precision(result)

        calc = Calculation(
            operation=op.name,
            a=a,
            b=b,
            result=result,
            timestamp=datetime.utcnow(),
        )

        self._history.append(calc)

        # Enforce max history size
        if len(self._history) > self.config.max_history_size:
            self._history = self._history[-self.config.max_history_size :]

        self._notify(calc)
        return result

    def _apply_precision(self, value: Decimal) -> Decimal:
        """
        Round to configured decimal places (CALCULATOR_PRECISION).
        """
        places = self.config.precision
        if places <= 0:
            return value.to_integral_value(rounding=ROUND_HALF_UP)
        quant = Decimal("1." + ("0" * places))
        return value.quantize(quant, rounding=ROUND_HALF_UP)

    # -------------------- Persistence (pandas) --------------------

    def to_dataframe(self) -> pd.DataFrame:
        rows = [c.to_dict() for c in self._history]
        return pd.DataFrame(rows, columns=["operation", "a", "b", "result", "timestamp"])

    def save_history(self) -> None:
        try:
            self.config.ensure_dirs()
            df = self.to_dataframe()
            df.to_csv(self.config.history_file, index=False, encoding=self.config.default_encoding)
        except Exception as e:
            raise PersistenceError(f"Failed to save history: {e}") from e

    def load_history(self) -> int:
        """
        Load history from CSV into Calculation objects.
        Returns number of loaded rows.
        """
        try:
            if not self.config.history_file.exists():
                raise PersistenceError("History file does not exist.")
            df = pd.read_csv(self.config.history_file, encoding=self.config.default_encoding)
            required = {"operation", "a", "b", "result", "timestamp"}
            if not required.issubset(set(df.columns)):
                raise PersistenceError(f"History file missing required columns: {required}")

            loaded: List[Calculation] = []
            for _, row in df.iterrows():
                loaded.append(Calculation.from_dict(row.to_dict()))

            self._push_undo_state()
            self._history = loaded[-self.config.max_history_size :]
            self._redo_stack.clear()
            return len(self._history)
        except PersistenceError:
            raise
        except Exception as e:
            raise PersistenceError(f"Failed to load history: {e}") from e