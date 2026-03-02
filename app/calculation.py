from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime
from typing import Dict, Any


@dataclass(frozen=True)
class Calculation:
    """
    Stores a single calculation record.
    Required CSV columns (screenshot):
    - operation, operands, result, timestamp
    """
    operation: str
    a: Decimal
    b: Decimal
    result: Decimal
    timestamp: datetime

    def to_dict(self) -> Dict[str, Any]:
        return {
            "operation": self.operation,
            "a": str(self.a),
            "b": str(self.b),
            "result": str(self.result),
            "timestamp": self.timestamp.isoformat(),
        }

    @staticmethod
    def from_dict(row: Dict[str, Any]) -> "Calculation":
        return Calculation(
            operation=str(row["operation"]),
            a=Decimal(str(row["a"])),
            b=Decimal(str(row["b"])),
            result=Decimal(str(row["result"])),
            timestamp=datetime.fromisoformat(str(row["timestamp"])),
        )