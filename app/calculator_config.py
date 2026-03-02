from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

from app.exceptions import ValidationError


def _to_bool(value: Optional[str], default: bool) -> bool:
    if value is None:
        return default
    v = value.strip().lower()
    if v in {"1", "true", "yes", "y", "on"}:
        return True
    if v in {"0", "false", "no", "n", "off"}:
        return False
    return default


def _to_int(value: Optional[str], default: int) -> int:
    if value is None or value.strip() == "":
        return default
    try:
        return int(value)
    except ValueError:
        return default


def _project_root() -> Path:
    """
    Try to infer the project root as the parent of the 'app' package directory.
    Assumes this file lives in: <root>/app/calculator_config.py
    """
    return Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class CalculatorConfig:
    """
    Loads calculator configuration from .env / environment variables.

    Env vars supported:
    - CALCULATOR_BASE_DIR
    - CALCULATOR_LOG_DIR
    - CALCULATOR_HISTORY_DIR
    - CALCULATOR_LOG_FILE
    - CALCULATOR_HISTORY_FILE
    - CALCULATOR_MAX_HISTORY_SIZE
    - CALCULATOR_AUTO_SAVE
    - CALCULATOR_PRECISION
    - CALCULATOR_MAX_INPUT_VALUE
    - CALCULATOR_DEFAULT_ENCODING
    """

    base_dir: Path
    log_dir: Path
    history_dir: Path

    log_file: Path
    history_file: Path

    max_history_size: int
    auto_save: bool

    precision: int
    max_input_value: int
    default_encoding: str

    @staticmethod
    def load(env_path: Optional[str] = ".env") -> "CalculatorConfig":
        # Load .env if present (safe even if missing)
        load_dotenv(env_path)

        base_dir_str = os.getenv("CALCULATOR_BASE_DIR")
        base_dir = (
            Path(base_dir_str).expanduser().resolve()
            if base_dir_str
            else _project_root()
        )

        log_dir_name = os.getenv("CALCULATOR_LOG_DIR", "logs")
        history_dir_name = os.getenv("CALCULATOR_HISTORY_DIR", "history")

        log_dir = (base_dir / log_dir_name).resolve()
        history_dir = (base_dir / history_dir_name).resolve()

        log_file_name = os.getenv("CALCULATOR_LOG_FILE", "calculator.log")
        history_file_name = os.getenv("CALCULATOR_HISTORY_FILE", "calculator_history.csv")

        log_file = (log_dir / log_file_name).resolve()
        history_file = (history_dir / history_file_name).resolve()

        max_history_size = _to_int(os.getenv("CALCULATOR_MAX_HISTORY_SIZE"), 100)
        auto_save = _to_bool(os.getenv("CALCULATOR_AUTO_SAVE"), True)

        precision = _to_int(os.getenv("CALCULATOR_PRECISION"), 10)
        max_input_value = _to_int(os.getenv("CALCULATOR_MAX_INPUT_VALUE"), 1_000_000_000)
        default_encoding = os.getenv("CALCULATOR_DEFAULT_ENCODING", "utf-8")

        # Validation (adjust ranges if your assignment requires different rules)
        if not (0 <= precision <= 50):
            raise ValidationError("CALCULATOR_PRECISION must be between 0 and 50.")

        if max_history_size <= 0:
            raise ValidationError("CALCULATOR_MAX_HISTORY_SIZE must be a positive integer.")

        if max_input_value <= 0:
            raise ValidationError("CALCULATOR_MAX_INPUT_VALUE must be a positive integer.")

        if not default_encoding or default_encoding.strip() == "":
            raise ValidationError("CALCULATOR_DEFAULT_ENCODING must be a non-empty string.")

        return CalculatorConfig(
            base_dir=base_dir,
            log_dir=log_dir,
            history_dir=history_dir,
            log_file=log_file,
            history_file=history_file,
            max_history_size=max_history_size,
            auto_save=auto_save,
            precision=precision,
            max_input_value=max_input_value,
            default_encoding=default_encoding,
        )

    def ensure_dirs(self) -> None:
        """Create directories needed by logger/history persistence."""
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.history_dir.mkdir(parents=True, exist_ok=True)