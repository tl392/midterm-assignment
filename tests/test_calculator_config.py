import os
from pathlib import Path

import pytest

from app.calculator_config import CalculatorConfig
from app.exceptions import ValidationError


def test_config_load_defaults(tmp_path, monkeypatch):
    # Force project root to tmp_path by setting CALCULATOR_BASE_DIR
    monkeypatch.setenv("CALCULATOR_BASE_DIR", str(tmp_path))
    monkeypatch.delenv("CALCULATOR_LOG_DIR", raising=False)
    monkeypatch.delenv("CALCULATOR_HISTORY_DIR", raising=False)

    cfg = CalculatorConfig.load(env_path=None)
    assert cfg.base_dir == tmp_path.resolve()
    assert cfg.log_dir == (tmp_path / "logs").resolve()
    assert cfg.history_dir == (tmp_path / "history").resolve()
    assert cfg.log_file.name == "calculator.log"
    assert cfg.history_file.name == "calculator_history.csv"
    assert isinstance(cfg.auto_save, bool)
    assert isinstance(cfg.precision, int)


def test_config_validation_precision_range(tmp_path, monkeypatch):
    monkeypatch.setenv("CALCULATOR_BASE_DIR", str(tmp_path))
    monkeypatch.setenv("CALCULATOR_PRECISION", "999")
    with pytest.raises(ValidationError):
        CalculatorConfig.load(env_path=None)


def test_config_validation_positive_ints(tmp_path, monkeypatch):
    monkeypatch.setenv("CALCULATOR_BASE_DIR", str(tmp_path))

    monkeypatch.setenv("CALCULATOR_MAX_HISTORY_SIZE", "0")
    with pytest.raises(ValidationError):
        CalculatorConfig.load(env_path=None)

    monkeypatch.setenv("CALCULATOR_MAX_HISTORY_SIZE", "10")
    monkeypatch.setenv("CALCULATOR_MAX_INPUT_VALUE", "0")
    with pytest.raises(ValidationError):
        CalculatorConfig.load(env_path=None)


def test_config_ensure_dirs_creates_folders(tmp_path, monkeypatch):
    monkeypatch.setenv("CALCULATOR_BASE_DIR", str(tmp_path))
    cfg = CalculatorConfig.load(env_path=None)
    assert not cfg.log_dir.exists()
    assert not cfg.history_dir.exists()

    cfg.ensure_dirs()
    assert cfg.log_dir.exists()
    assert cfg.history_dir.exists()
