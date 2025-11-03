from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

LOG_DIR = Path(__file__).resolve().parents[1] / "data" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)


def configure_logger(name: str = "lmaa") -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    log_file = LOG_DIR / "lmaa.log"
    file_handler = logging.FileHandler(log_file, mode="a", encoding="utf-8")
    console_handler = logging.StreamHandler()

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.propagate = False

    return logger


_logger: Optional[logging.Logger] = None


def log(message: str, *args, **kwargs) -> None:
    global _logger
    if _logger is None:
        _logger = configure_logger()
    _logger.info(message, *args, **kwargs)
