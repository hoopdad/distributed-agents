from __future__ import annotations

import os
from urllib.parse import urlsplit


class ConfigurationError(ValueError):
    pass


def required(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value or any(character in value for character in "<>\r\n"):
        raise ConfigurationError(f"CONFIGURATION_REQUIRED: {name}")
    return value


def project_scope() -> tuple[str, str]:
    project = required("FOUNDRY_PROJECT_ENDPOINT").rstrip("/")
    try:
        endpoint = urlsplit(project)
        port = endpoint.port
    except ValueError as exc:
        raise ConfigurationError("FOUNDRY_PROJECT_ENDPOINT_INVALID") from exc
    parts = endpoint.path.split("/")
    if (
        endpoint.scheme != "https" or endpoint.username or endpoint.password
        or port not in (None, 443) or endpoint.query or endpoint.fragment
        or not endpoint.hostname
        or not endpoint.hostname.endswith((".services.ai.azure.com", ".ai.azure.com"))
        or len(parts) != 4 or parts[1:3] != ["api", "projects"] or not parts[3]
        or any(character not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-"
               for character in parts[3])
    ):
        raise ConfigurationError("FOUNDRY_PROJECT_ENDPOINT_INVALID")
    return project, f"https://{endpoint.hostname}"
