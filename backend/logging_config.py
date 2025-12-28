"""Logging configuration utilities for the Trip Planner backend.

Provides a configure_logging() function that sets up:
 - Standardized root logger format
 - Optional JSON logging via environment flag LOG_JSON=true
 - Uvicorn / FastAPI logger alignment
 - Suppression of overly verbose third-party loggers
"""

from __future__ import annotations

import json
import logging
import os
from datetime import datetime
from typing import Any, Dict

DEFAULT_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()


class JsonFormatter(logging.Formatter):
    """Simple JSON log formatter."""

    def format(self, record: logging.LogRecord) -> str:  # noqa: D401
        base: Dict[str, Any] = {
            "ts": datetime.utcfromtimestamp(record.created).isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            base["exc_info"] = self.formatException(record.exc_info)
        for attr in ("workflow_id", "request_id"):
            if hasattr(record, attr):
                base[attr] = getattr(record, attr)
        return json.dumps(base, ensure_ascii=False)


def configure_logging(
    force: bool = False,
    json_logs: bool | None = None,
) -> None:
    """Configure application logging.

    Parameters
    ----------
    force : bool
        If True, reconfigure even if handlers already exist.
    json_logs : bool | None
        Override JSON logging decision. If None, derive from LOG_JSON env.
    """
    root = logging.getLogger()
    if root.handlers and not force:
        return

    for h in list(root.handlers):
        root.removeHandler(h)

    use_json = (
        json_logs
        if json_logs is not None
        else os.getenv("LOG_JSON", "false").lower() in {"1", "true", "yes"}
    )

    if use_json:
        handler: logging.Handler = logging.StreamHandler()
        handler.setFormatter(JsonFormatter())
    else:
        pattern = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(pattern))

    root.setLevel(DEFAULT_LEVEL)
    root.addHandler(handler)

    # Align uvicorn loggers
    for name in ["uvicorn", "uvicorn.error", "uvicorn.access"]:
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True

    # Quiet noisy libs
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    logging.getLogger(__name__).info(
        "Logging configured", extra={"json": use_json, "level": DEFAULT_LEVEL}
    )


__all__ = ["configure_logging"]
