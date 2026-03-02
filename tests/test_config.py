from app.calculator_config import CalculatorConfig


def test_config_load_defaults(tmp_path, monkeypatch):
    monkeypatch.delenv("CALCULATOR_BASE_DIR", raising=False)
    monkeypatch.delenv("CALCULATOR_MAX_HISTORY_SIZE", raising=False)

    # Force base dir to tmp
    monkeypatch.setenv("CALCULATOR_BASE_DIR", str(tmp_path))
    cfg = CalculatorConfig.load(env_path="__missing__.env")
    assert cfg.base_dir == tmp_path.resolve()
    assert cfg.max_history_size > 0