from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Tuple, Iterable, List

from app.calculation import Calculation


@dataclass(frozen=True, slots=True)
class CalculatorMemento:
    """
    Memento: an immutable snapshot of calculator state.

    - Stores a history snapshot (immutable tuple to prevent accidental mutation)
    - Stores a timestamp (useful for undo/redo UI or debugging)
    - Supports serialization for persistence
    """

    history_snapshot: Tuple[Calculation, ...]
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @staticmethod
    def capture(history: Iterable[Calculation]) -> "CalculatorMemento":
        """
        Create a safe snapshot from a history iterable.
        Ensures we copy into an immutable tuple.
        """
        return CalculatorMemento(history_snapshot=tuple(history))

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize memento to a JSON-friendly dict.
        Requires Calculation.to_dict().
        """
        return {
            "history": [calc.to_dict() for calc in self.history_snapshot],
            "timestamp": self.timestamp.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CalculatorMemento":
        """
        Deserialize memento from a dict.
        Requires Calculation.from_dict().
        """
        return cls(
            history_snapshot=tuple(Calculation.from_dict(c) for c in data["history"]),
            timestamp=datetime.fromisoformat(data["timestamp"]),
        )

    def as_list(self) -> List[Calculation]:
        """
        Return history as a new list (useful when restoring into a mutable history store).
        """
        return list(self.history_snapshot)