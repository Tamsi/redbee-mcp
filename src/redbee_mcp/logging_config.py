"""Centralized logging configuration for Red Bee MCP."""

import logging
import os
import sys
from typing import Optional

_CONFIGURED = False

SENSITIVE_LOG_KEYS = frozenset({
    "password",
    "oldPassword",
    "newPassword",
    "session_token",
    "sessionToken",
    "paymentMethodData",
})


def sanitize_for_log(data: Optional[dict]) -> dict:
    """Redact sensitive values before logging."""
    if not data:
        return {}
    return {
        key: "***" if key in SENSITIVE_LOG_KEYS else value
        for key, value in data.items()
    }


def configure_logging(level: Optional[str] = None) -> None:
    """Configure application logging once (stderr by default, optional file)."""
    global _CONFIGURED
    if _CONFIGURED:
        return

    log_level = getattr(logging, (level or os.getenv("REDBEE_LOG_LEVEL", "INFO")).upper(), logging.INFO)
    handlers: list[logging.Handler] = [logging.StreamHandler(sys.stderr)]

    log_path = os.getenv("REDBEE_LOG_PATH")
    if log_path:
        handlers.append(logging.FileHandler(log_path))

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=handlers,
        force=True,
    )
    _CONFIGURED = True
