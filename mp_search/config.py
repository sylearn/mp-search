import os
from pathlib import Path
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

MP_API_KEY = os.environ.get("MP_API_KEY", "")
DEFAULT_EXPORT_DIR = os.environ.get(
    "MP_EXPORT_DIR", str(PROJECT_ROOT / "result" / "mp_search")
)
LANG = os.environ.get("MP_SEARCH_LANG", "zh")
