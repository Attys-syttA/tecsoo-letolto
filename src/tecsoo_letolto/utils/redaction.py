from __future__ import annotations

import re
from pathlib import PureWindowsPath

SECRET_PATTERNS = [
    re.compile(r"(?i)(password|passwd|secret|token|api[_-]?key|cookie)=([^\s&]+)"),
    re.compile(r"(?i)(bearer)\s+[A-Za-z0-9._~+/=-]+"),
]


def redact_text(value: str) -> str:
    redacted = value
    for pattern in SECRET_PATTERNS:
        if pattern.groups >= 2:
            redacted = pattern.sub(lambda m: f"{m.group(1)}=<redacted>", redacted)
        else:
            redacted = pattern.sub(lambda m: f"{m.group(1)} <redacted>", redacted)
    return redacted


def redact_path(value: str) -> str:
    if not value:
        return value
    try:
        path = PureWindowsPath(value)
        parts = path.parts
        if len(parts) >= 3 and parts[1].lower() == "users":
            return str(PureWindowsPath(parts[0], "...", *parts[3:]))
    except Exception:
        return value
    return value
