from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path


def configure_logging(log_dir: Path) -> Path:
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / f"tecsoletolto_{datetime.now():%Y-%m-%d}.log"
    logging.basicConfig(
        filename=str(log_path),
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        encoding="utf-8",
    )
    return log_path


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
