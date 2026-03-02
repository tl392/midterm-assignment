from __future__ import annotations

from decimal import Decimal
from typing import List

from app.calculator import Calculator
from app.calculator_config import CalculatorConfig
from app.exceptions import ValidationError, OperationError, PersistenceError
from app.history import LoggingObserver, AutoSaveObserver
from app.input_validators import parse_two_numbers
from app.logger import build_logger


HELP_TEXT = """
Supported commands:
  add, subtract, multiply, divide, power, root, modulus, int_divide, percent, abs_diff  - Perform calculations (two numbers)
  history  - Display calculation history
  clear    - Clear calculation history
  undo     - Undo the last calculation
  redo     - Redo the last undone calculation
  save     - Manually save calculation history to CSV (pandas)
  load     - Load calculation history from CSV (pandas)
  help     - Display available commands
  exit     - Exit the application
""".strip()


def format_calc_line(i: int, op: str, a: str, b: str, result: str, ts: str) -> str:
    return f"{i:>3}. {op}({a}, {b}) = {result} @ {ts}"


def run_repl() -> None:
    config = CalculatorConfig.load()
    calc = Calculator(config=config)

    logger = build_logger(config)
    calc.add_observer(LoggingObserver(logger))
    calc.add_observer(AutoSaveObserver(config))

    print("Calculator started. Type 'help' for commands.")

    while True:
        try:
            raw = input("> ").strip()
            if not raw:
                continue

            parts = raw.split()
            cmd = parts[0].lower()

            if cmd == "help":
                print(HELP_TEXT)
                continue

            if cmd == "exit":
                print("Goodbye!")
                break

            if cmd == "history":
                h = calc.history
                if not h:
                    print("No calculations in history.")
                else:
                    for idx, c in enumerate(h, start=1):
                        print(format_calc_line(idx, c.operation, str(c.a), str(c.b), str(c.result), c.timestamp.isoformat()))
                continue

            if cmd == "clear":
                calc.clear_history()
                print("History cleared.")
                continue

            if cmd == "undo":
                if calc.undo():
                    print("Undo successful.")
                else:
                    print("Nothing to undo.")
                continue

            if cmd == "redo":
                if calc.redo():
                    print("Redo successful.")
                else:
                    print("Nothing to redo.")
                continue

            if cmd == "save":
                calc.save_history()
                print(f"History saved to {calc.config.history_file}")
                continue

            if cmd == "load":
                n = calc.load_history()
                print(f"Loaded {n} history entries from {calc.config.history_file}")
                continue

            # Otherwise: arithmetic operation must be cmd + 2 numbers
            if len(parts) != 3:
                raise ValidationError("Operation requires exactly two inputs: <command> <a> <b>")

            a, b = parse_two_numbers(parts[1], parts[2], max_value=calc.config.max_input_value)
            result = calc.calculate(cmd, a, b)
            print(result)

        except (ValidationError, OperationError, PersistenceError) as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            # Catch-all for unexpected errors
            print(f"Unexpected error: {e}")