"""First-run setup wizard for mp-search."""

from __future__ import annotations

from pathlib import Path

from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label, Select, Static

import mp_search.config as _cfg

_LANG_OPTIONS = [
    ("English", "en"),
    ("中文", "zh"),
]


class SetupScreen(ModalScreen[dict | None]):
    """Interactive setup wizard shown on first launch."""

    DEFAULT_CSS = """
    SetupScreen { align: center middle; }
    #setup-box {
        width: 72; max-height: 90%;
        background: $surface; border: thick $primary; padding: 1 2;
    }
    .setup-label { margin-top: 1; color: $text-muted; }
    .setup-hint { color: $text-disabled; margin-bottom: 0; }
    .setup-input { margin-bottom: 0; }
    #setup-title { text-style: bold; margin-bottom: 1; }
    #setup-subtitle { color: $text-muted; margin-bottom: 1; }
    #setup-save { margin-top: 2; }
    #setup-error { color: $error; margin-top: 1; display: none; }
    """

    BINDINGS = [Binding("escape", "dismiss(None)", "Cancel")]

    def compose(self) -> ComposeResult:
        with Vertical(id="setup-box"):
            yield Static("Welcome to MP Search", id="setup-title")
            yield Static(
                "First-time setup — configure your settings below.",
                id="setup-subtitle",
            )

            yield Label("API Key  [required]", classes="setup-label")
            yield Static(
                "Get yours at https://next-gen.materialsproject.org/api",
                classes="setup-hint",
            )
            yield Input(
                value=_cfg.MP_API_KEY,
                placeholder="Paste your Materials Project API key",
                id="input-api-key",
                password=True,
                classes="setup-input",
            )

            yield Label("Export Directory", classes="setup-label")
            yield Static(
                "Where exported files (POSCAR/CIF/JSON) will be saved.",
                classes="setup-hint",
            )
            yield Input(
                value=_cfg.DEFAULT_EXPORT_DIR,
                placeholder=_cfg.DEFAULT_EXPORT_DIR,
                id="input-export-dir",
                classes="setup-input",
            )

            yield Label("Language", classes="setup-label")
            yield Select(
                _LANG_OPTIONS,
                value=_cfg.LANG,
                id="select-lang",
                allow_blank=False,
            )

            yield Static(
                f"Config will be saved to: {_cfg.CONFIG_FILE}",
                classes="setup-hint",
            )

            yield Static("", id="setup-error")
            yield Button(
                "Save & Start", variant="primary", id="setup-save"
            )

    @on(Button.Pressed, "#setup-save")
    def _on_save(self) -> None:
        api_key = self.query_one("#input-api-key", Input).value.strip()
        if not api_key:
            err = self.query_one("#setup-error", Static)
            err.update("API Key is required.")
            err.styles.display = "block"
            return

        export_dir = (
            self.query_one("#input-export-dir", Input).value.strip()
            or _cfg.DEFAULT_EXPORT_DIR
        )
        lang = str(self.query_one("#select-lang", Select).value)

        path = _cfg.save_config(api_key, export_dir, lang)
        self.notify(f"Saved to {path}", severity="information", timeout=3)
        self.dismiss({"api_key": api_key, "export_dir": export_dir, "lang": lang})
