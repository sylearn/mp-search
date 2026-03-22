"""Configuration loader with multi-location search.

Search order (first found wins):
  1. Environment variables already set in shell
  2. ~/.config/mp-search/config.env   (global config, XDG standard)
  3. .env in current working directory (developer workflow)
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

CONFIG_DIR = Path.home() / ".config" / "mp-search"
CONFIG_FILE = CONFIG_DIR / "config.env"

for _candidate in [CONFIG_FILE, Path.cwd() / ".env"]:
    if _candidate.is_file():
        load_dotenv(_candidate)
        break

MP_API_KEY: str = os.environ.get("MP_API_KEY", "")
DEFAULT_EXPORT_DIR: str = os.environ.get(
    "MP_EXPORT_DIR",
    str(Path.home() / "mp-search-exports"),
)
LANG: str = os.environ.get("MP_SEARCH_LANG", "en")


def save_config(api_key: str, export_dir: str, lang: str) -> Path:
    """Save configuration to ~/.config/mp-search/config.env."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    lines = [
        f'MP_API_KEY="{api_key}"',
        f'MP_EXPORT_DIR="{export_dir}"',
        f'MP_SEARCH_LANG="{lang}"',
    ]
    CONFIG_FILE.write_text("\n".join(lines) + "\n")
    return CONFIG_FILE


def reload_config() -> None:
    """Re-read config from file and update module-level variables."""
    global MP_API_KEY, DEFAULT_EXPORT_DIR, LANG
    if CONFIG_FILE.is_file():
        load_dotenv(CONFIG_FILE, override=True)
    MP_API_KEY = os.environ.get("MP_API_KEY", "")
    DEFAULT_EXPORT_DIR = os.environ.get(
        "MP_EXPORT_DIR",
        str(Path.home() / "mp-search-exports"),
    )
    LANG = os.environ.get("MP_SEARCH_LANG", "en")
