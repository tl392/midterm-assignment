import builtins
import pytest
from decimal import Decimal


from app.calculator_repl import calculator_repl


def _set_test_env(monkeypatch, tmp_path):
    """Isolate environment variables for safe testing."""
    monkeypatch.setenv("CALCULATOR_BASE_DIR", str(tmp_path))
    monkeypatch.setenv("CALCULATOR_LOG_DIR", "logs")
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", "history")
    monkeypatch.setenv("CALCULATOR_LOG_FILE", "test.log")
    monkeypatch.setenv("CALCULATOR_HISTORY_FILE", "test.csv")
    monkeypatch.setenv("CALCULATOR_MAX_HISTORY_SIZE", "10")
    monkeypatch.setenv("CALCULATOR_AUTO_SAVE", "false")
    monkeypatch.setenv("CALCULATOR_PRECISION", "5")
    monkeypatch.setenv("CALCULATOR_MAX_INPUT_VALUE", "1000000")
    monkeypatch.setenv("CALCULATOR_DEFAULT_ENCODING", "utf-8")


def _feed_inputs(monkeypatch, inputs):
    it = iter(inputs)
    monkeypatch.setattr(builtins, "input", lambda _: next(it))

def test_repl_start_and_exit(monkeypatch, capsys, tmp_path):
    _set_test_env(monkeypatch, tmp_path)
    _feed_inputs(monkeypatch, ["exit"])

    calculator_repl()

    output = capsys.readouterr().out
    assert "Calculator started" in output
    assert "Goodbye!" in output

def test_repl_help(monkeypatch, capsys, tmp_path):
    _set_test_env(monkeypatch, tmp_path)
    _feed_inputs(monkeypatch, ["help", "exit"])

    calculator_repl()

    output = capsys.readouterr().out
    assert "Supported commands" in output

def test_repl_valid_calculation(monkeypatch, capsys, tmp_path):
    _set_test_env(monkeypatch, tmp_path)
    _feed_inputs(monkeypatch, ["add 2 3", "exit"])

    calculator_repl()

    output = capsys.readouterr().out
    assert "5.00000" in output

def test_repl_invalid_format(monkeypatch, capsys, tmp_path):
    _set_test_env(monkeypatch, tmp_path)
    _feed_inputs(monkeypatch, ["add 5", "exit"])

    calculator_repl()

    output = capsys.readouterr().out
    assert "Error:" in output

def test_repl_divide_by_zero(monkeypatch, capsys, tmp_path):
    _set_test_env(monkeypatch, tmp_path)
    _feed_inputs(monkeypatch, ["divide 10 0", "exit"])

    calculator_repl()

    output = capsys.readouterr().out
    assert "Error:" in output

def test_repl_history_empty(monkeypatch, capsys, tmp_path):
    _set_test_env(monkeypatch, tmp_path)
    _feed_inputs(monkeypatch, ["history", "exit"])

    calculator_repl()

    output = capsys.readouterr().out
    assert "No calculations in history." in output

def test_repl_history_after_calculation(monkeypatch, capsys, tmp_path):
    _set_test_env(monkeypatch, tmp_path)
    _feed_inputs(monkeypatch, ["add 1 2", "history", "exit"])

    calculator_repl()

    output = capsys.readouterr().out
    assert "add(1, 2)" in output

def test_repl_clear_history(monkeypatch, capsys, tmp_path):
    _set_test_env(monkeypatch, tmp_path)
    _feed_inputs(monkeypatch, ["add 1 2", "clear", "history", "exit"])

    calculator_repl()

    output = capsys.readouterr().out
    assert "History cleared." in output
    assert "No calculations in history." in output

def test_repl_undo_redo(monkeypatch, capsys, tmp_path):
    _set_test_env(monkeypatch, tmp_path)
    _feed_inputs(monkeypatch, ["add 2 3", "undo", "redo", "exit"])

    calculator_repl()

    output = capsys.readouterr().out
    assert "Undo successful." in output
    assert "Redo successful." in output

def test_repl_save_and_load(monkeypatch, capsys, tmp_path):
    _set_test_env(monkeypatch, tmp_path)
    _feed_inputs(monkeypatch, ["add 2 3", "save", "load", "exit"])

    calculator_repl()

    output = capsys.readouterr().out
    assert "History saved" in output
    assert "Loaded" in output


def test_repl_invalid_command(monkeypatch, capsys, tmp_path):
    _set_test_env(monkeypatch, tmp_path)
    _feed_inputs(monkeypatch, ["unknown 1 2", "exit"])

    calculator_repl()

    output = capsys.readouterr().out
    assert "Error:" in output
    
def test_repl_blank_input_then_exit(monkeypatch, capsys, tmp_path):
    _set_test_env(monkeypatch, tmp_path)
    _feed_inputs(monkeypatch, ["", "   ", "exit"])  # blanks should be ignored
    calculator_repl()
    out = capsys.readouterr().out
    assert "Calculator started" in out
    assert "Goodbye!" in out


@pytest.mark.parametrize("cmd", ["q", "quit"])
def test_repl_exit_aliases(monkeypatch, capsys, tmp_path, cmd):
    _set_test_env(monkeypatch, tmp_path)
    _feed_inputs(monkeypatch, [cmd])
    calculator_repl()
    out = capsys.readouterr().out
    assert "Goodbye!" in out

def test_repl_undo_nothing(monkeypatch, capsys, tmp_path):
    _set_test_env(monkeypatch, tmp_path)
    _feed_inputs(monkeypatch, ["undo", "exit"])
    calculator_repl()
    out = capsys.readouterr().out
    assert "Nothing to undo." in out

def test_repl_redo_nothing(monkeypatch, capsys, tmp_path):
    _set_test_env(monkeypatch, tmp_path)
    _feed_inputs(monkeypatch, ["redo", "exit"])
    calculator_repl()
    out = capsys.readouterr().out
    assert "Nothing to redo." in out

def test_repl_load_missing_file(monkeypatch, capsys, tmp_path):
    _set_test_env(monkeypatch, tmp_path)
    # Ensure no history file exists (default name is test.csv under history/)
    _feed_inputs(monkeypatch, ["load", "exit"])
    calculator_repl()
    out = capsys.readouterr().out
    assert "Error:" in out  # should be PersistenceError handled


def test_repl_keyboard_interrupt(monkeypatch, capsys, tmp_path):
    _set_test_env(monkeypatch, tmp_path)

    def raise_keyboard_interrupt(_prompt):
        raise KeyboardInterrupt

    monkeypatch.setattr(builtins, "input", raise_keyboard_interrupt)

    calculator_repl()
    out = capsys.readouterr().out
    assert "Goodbye!" in out

def test_repl_unexpected_error_branch(monkeypatch, capsys, tmp_path):
    _set_test_env(monkeypatch, tmp_path)
    _feed_inputs(monkeypatch, ["add 1 2", "exit"])

    # Patch the REAL Calculator.calculate to raise a RuntimeError once
    import app.calculator as calc_mod

    original = calc_mod.Calculator.calculate

    def boom(self, cmd, a, b):
        raise RuntimeError("boom")

    monkeypatch.setattr(calc_mod.Calculator, "calculate", boom)

    calculator_repl()

    # restore not required due to monkeypatch fixture, but fine if you prefer
    # monkeypatch.setattr(calc_mod.Calculator, "calculate", original)

    out = capsys.readouterr().out
    assert "Unexpected error: boom" in out