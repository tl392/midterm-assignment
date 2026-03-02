import logging
from logging import Logger
from app.calculator_config import CalculatorConfig


def build_logger(config: CalculatorConfig) -> Logger:
    """
    Create a file-based logger using configuration.

    Screenshot mentions:
    - CALCULATOR_LOG_FILE
    - log levels INFO/WARNING/ERROR
    """
    config.ensure_dirs()

    logger = logging.getLogger("calculator")
    logger.setLevel(logging.INFO)

    # Avoid duplicate handlers if called multiple times in tests or REPL restarts.
    if not any(isinstance(h, logging.FileHandler) for h in logger.handlers):
        fh = logging.FileHandler(config.log_file, encoding=config.default_encoding)
        fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
        fh.setFormatter(fmt)
        logger.addHandler(fh)

    return logger