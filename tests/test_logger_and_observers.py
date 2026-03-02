import logging
import pytest
from decimal import Decimal

from app.calculator import Calculator
from app.calculator_config import CalculatorConfig
from app.history import LoggingObserver, AutoSaveObserver
from app.logger import build_logger
from app.exceptions import PersistenceError

def reset_calculator_logger():
    """Clear handlers so tests using different tmp_path configs don't fight each other."""
    logger = logging.getLogger("calculator")
    for h in list(logger.handlers):
        try:
            h.close()
        except Exception:
            pass
        logger.removeHandler(h)
    return logger

def make_config(tmp_path, *, auto_save=False):
    base = tmp_path / "base"
    return CalculatorConfig(
        base_dir=base,
        log_dir=base / "logs",
        history_dir=base / "history",
        log_file=base / "logs" / "calculator.log",
        history_file=base / "history" / "calculator_history.csv",
        max_history_size=50,
        auto_save=auto_save,
        precision=10,
        max_input_value=1_000_000,
        default_encoding="utf-8",
    )


def d(x):
    return Decimal(str(x))


def test_build_logger_creates_file_handler_once(tmp_path):
    reset_calculator_logger()
    cfg = make_config(tmp_path)
    logger1 = build_logger(cfg)
    logger2 = build_logger(cfg)
    assert logger1 is logger2  # same named logger
    # only one FileHandler should exist
    file_handlers = [h for h in logger1.handlers if h.__class__.__name__ == "FileHandler"]
    assert len(file_handlers) == 1


def test_logging_observer_writes_message(tmp_path):
    reset_calculator_logger()
    cfg = make_config(tmp_path)
    calc = Calculator(cfg)
    logger = build_logger(cfg)
    calc.add_observer(LoggingObserver(logger))

    calc.calculate("add", d(1), d(2))
    assert cfg.log_file.exists()
    text = cfg.log_file.read_text(encoding=cfg.default_encoding)
    assert "operation=add" in text


def test_autosave_observer_disabled_does_not_save(tmp_path):
    cfg = make_config(tmp_path, auto_save=False)
    calc = Calculator(cfg)
    calc.add_observer(AutoSaveObserver(cfg))

    calc.calculate("add", d(1), d(2))
    assert not cfg.history_file.exists()


def test_autosave_observer_enabled_saves(tmp_path):
    cfg = make_config(tmp_path, auto_save=True)
    calc = Calculator(cfg)
    calc.add_observer(AutoSaveObserver(cfg))

    calc.calculate("add", d(1), d(2))
    assert cfg.history_file.exists()


def test_autosave_wraps_errors_as_persistence_error(tmp_path, monkeypatch):
    cfg = make_config(tmp_path, auto_save=True)
    calc = Calculator(cfg)
    obs = AutoSaveObserver(cfg)
    calc.add_observer(obs)

    def boom():
        raise RuntimeError("nope")

    monkeypatch.setattr(calc, "save_history", boom)
    with pytest.raises(PersistenceError):
        calc.calculate("add", d(1), d(2))
