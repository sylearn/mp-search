from __future__ import annotations

import os

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

from textual import on, work
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal
from textual.widgets import (
    Button,
    Collapsible,
    DataTable,
    Footer,
    Header,
    Input,
    Label,
    Select,
    Static,
    Switch,
)

from mp_search.api.client import MaterialSummary, SearchFilters
from mp_search.i18n import t


def _search_modes() -> list[tuple[str, str]]:
    return [
        (t("mode_formula"), "formula"),
        (t("mode_elements"), "elements"),
        (t("mode_chemsys"), "chemsys"),
    ]


def _crystal_options() -> list[tuple[str, str]]:
    return [
        (t("crystal_all"), ""),
        ("Triclinic", "Triclinic"),
        ("Monoclinic", "Monoclinic"),
        ("Orthorhombic", "Orthorhombic"),
        ("Tetragonal", "Tetragonal"),
        ("Trigonal", "Trigonal"),
        ("Hexagonal", "Hexagonal"),
        ("Cubic", "Cubic"),
    ]


_PH_MAP = {
    "formula": "ph_formula",
    "elements": "ph_elements",
    "chemsys": "ph_chemsys",
}


class MPSearchApp(App):
    TITLE = "MP Search"
    SUB_TITLE = "Materials Project"

    CSS = """
    Screen { background: $surface; }
    #search-bar { dock: top; height: auto; padding: 1 2; background: $boost; }
    #search-mode { width: 30; margin-right: 1; }
    #search-input { width: 1fr; margin-right: 1; }
    #search-btn { min-width: 10; }
    #filter-panel { height: auto; margin: 0 2; padding: 0 1; }
    .filter-row { height: 3; padding: 0 1; align: left middle; }
    .filter-row Label { width: 18; margin-right: 1; }
    .filter-input { width: 14; margin-right: 1; }
    .filter-sep { width: 3; content-align: center middle; }
    #filter-crystal-system { width: 24; }
    #results-table { height: 1fr; margin: 0 2; }
    #status-bar { dock: bottom; height: 1; padding: 0 2; background: $accent; color: $text; }
    """

    BINDINGS = [
        Binding("q", "quit", "", priority=True),
        Binding("slash", "focus_search", "", show=True),
        Binding("f", "toggle_filters", "", show=True),
        Binding("e", "export_selected", "", show=True),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.client = None
        self.results: list[MaterialSummary] = []
        self._results_map: dict[str, MaterialSummary] = {}
        self.BINDINGS = [
            Binding("q", "quit", t("key_quit"), priority=True),
            Binding("slash", "focus_search", t("key_search"), show=True),
            Binding("f", "toggle_filters", t("key_filter"), show=True),
            Binding("e", "export_selected", t("key_export"), show=True),
        ]

    # ── layout ───────────────────────────────────────────────

    def compose(self) -> ComposeResult:
        yield Header()

        with Horizontal(id="search-bar"):
            yield Select(
                _search_modes(),
                value="formula",
                id="search-mode",
                allow_blank=False,
            )
            yield Input(
                placeholder=t("ph_formula"),
                id="search-input",
            )
            yield Button(t("btn_search"), variant="primary", id="search-btn")

        with Collapsible(title=t("filter_title"), id="filter-panel", collapsed=True):
            with Horizontal(classes="filter-row"):
                yield Label(t("lbl_bandgap"))
                yield Input(placeholder=t("ph_min"), id="filter-bg-min", classes="filter-input")
                yield Static("~", classes="filter-sep")
                yield Input(placeholder=t("ph_max"), id="filter-bg-max", classes="filter-input")
            with Horizontal(classes="filter-row"):
                yield Label(t("lbl_ehull"))
                yield Input(placeholder=t("ph_max"), id="filter-ehull-max", classes="filter-input")
            with Horizontal(classes="filter-row"):
                yield Label(t("lbl_nsites"))
                yield Input(placeholder=t("ph_min"), id="filter-nsites-min", classes="filter-input")
                yield Static("~", classes="filter-sep")
                yield Input(placeholder=t("ph_max"), id="filter-nsites-max", classes="filter-input")
            with Horizontal(classes="filter-row"):
                yield Label(t("lbl_crystal"))
                yield Select(
                    _crystal_options(),
                    value="",
                    id="filter-crystal-system",
                    allow_blank=False,
                )
            with Horizontal(classes="filter-row"):
                yield Label(t("lbl_stable_only"))
                yield Switch(id="filter-stable-only", value=False)

        yield DataTable(id="results-table")
        yield Static(t("status_hint"), id="status-bar")
        yield Footer()

    # ── lifecycle ─────────────────────────────────────────────

    def on_mount(self) -> None:
        table = self.query_one("#results-table", DataTable)
        table.add_columns(
            t("col_id"), t("col_formula"), t("col_nsites"), t("col_bandgap"),
            t("col_ehull"), t("col_spacegroup"), t("col_crystal"), t("col_stable"),
        )
        table.cursor_type = "row"
        self._try_connect()

    def _try_connect(self) -> None:
        from mp_search.config import MP_API_KEY

        if not MP_API_KEY:
            self._status(t("status_no_key"))
            from mp_search.tui.setup import SetupScreen
            self.push_screen(SetupScreen(), callback=self._on_setup_done)
            return

        self._connect_api(MP_API_KEY)

    def _on_setup_done(self, result: dict | None) -> None:
        if result is None:
            self._status(t("status_no_key"))
            self.notify(t("notify_no_key"), severity="error", timeout=10)
            return

        from mp_search import config
        config.reload_config()

        self._connect_api(result["api_key"])

    @work(thread=True, exclusive=True)
    def _connect_api(self, api_key: str) -> None:
        try:
            from mp_search.api.client import MPClient
            client = MPClient(api_key)
            client.connect()
            self.client = client
            self.call_from_thread(self._status, t("status_ready"))
        except Exception as exc:
            self.call_from_thread(
                self._status, t("status_error", str(exc))
            )

    # ── search events ────────────────────────────────────────

    @on(Select.Changed, "#search-mode")
    def _on_mode_changed(self, event: Select.Changed) -> None:
        inp = self.query_one("#search-input", Input)
        key = _PH_MAP.get(str(event.value), "ph_formula")
        inp.placeholder = t(key)
        inp.value = ""
        inp.focus()

    @on(Input.Submitted, "#search-input")
    def _on_search_submit(self) -> None:
        self._trigger_search()

    @on(Button.Pressed, "#search-btn")
    def _on_search_btn(self) -> None:
        self._trigger_search()

    def _trigger_search(self) -> None:
        if not self.client:
            self.notify(t("notify_no_client"), severity="error")
            return
        query = self.query_one("#search-input", Input).value.strip()
        if not query:
            self.notify(t("notify_empty"), severity="warning")
            return
        mode = str(self.query_one("#search-mode", Select).value)
        filters = self._collect_filters()

        table = self.query_one("#results-table", DataTable)
        table.clear()
        table.loading = True
        self._status(t("status_searching", query))
        self._run_search(query, mode, filters)

    @work(thread=True, exclusive=True)
    def _run_search(
        self, query: str, mode: str, filters: SearchFilters
    ) -> None:
        try:
            if mode == "formula":
                results = self.client.search_by_formula(query, filters)
            elif mode == "elements":
                elems = [
                    e.strip()
                    for e in query.replace(",", " ").replace("\uff0c", " ").split()
                    if e.strip()
                ]
                results = self.client.search_by_elements(elems, filters)
            else:
                results = self.client.search_by_chemsys(query, filters)

            self.results = results
            self._results_map = {r.material_id: r for r in results}
            self.call_from_thread(self._show_results, results)
        except Exception as exc:
            self.call_from_thread(self._on_error, str(exc))

    def _show_results(self, results: list[MaterialSummary]) -> None:
        table = self.query_one("#results-table", DataTable)
        table.clear()
        for r in results:
            sg = f"{r.spacegroup_symbol} ({r.spacegroup_number})"
            table.add_row(
                r.material_id,
                r.formula,
                str(r.nsites),
                f"{r.band_gap:.3f}",
                f"{r.energy_above_hull:.4f}",
                sg,
                r.crystal_system,
                "\u2713" if r.is_stable else "\u2717",
                key=r.material_id,
            )
        table.loading = False
        self._status(t("status_found", len(results)))

    def _on_error(self, msg: str) -> None:
        table = self.query_one("#results-table", DataTable)
        table.loading = False
        self._status(t("status_error", msg))
        self.notify(msg, severity="error", timeout=8)

    # ── detail / export ──────────────────────────────────────

    @on(DataTable.RowSelected, "#results-table")
    def _on_row_selected(self, event: DataTable.RowSelected) -> None:
        mid = event.row_key.value
        mat = self._results_map.get(str(mid))
        if mat:
            from mp_search.tui.detail import DetailScreen
            self.push_screen(DetailScreen(mat))

    def action_export_selected(self) -> None:
        table = self.query_one("#results-table", DataTable)
        if not self.results:
            self.notify(t("notify_search_first"), severity="warning")
            return
        try:
            row = table.get_row_at(table.cursor_row)
            mid = str(row[0])
            mat = self._results_map.get(mid)
            if mat:
                from mp_search.tui.detail import DetailScreen
                self.push_screen(DetailScreen(mat))
        except Exception:
            self.notify(t("notify_select_one"), severity="warning")

    # ── actions ───────────────────────────────────────────────

    def action_focus_search(self) -> None:
        self.query_one("#search-input", Input).focus()

    def action_toggle_filters(self) -> None:
        panel = self.query_one("#filter-panel", Collapsible)
        panel.collapsed = not panel.collapsed

    # ── helpers ───────────────────────────────────────────────

    def _status(self, msg: str) -> None:
        self.query_one("#status-bar", Static).update(msg)

    def _collect_filters(self) -> SearchFilters:
        f = SearchFilters()

        def _float(wid: str) -> float | None:
            v = self.query_one(f"#{wid}", Input).value.strip()
            try:
                return float(v) if v else None
            except ValueError:
                return None

        def _int(wid: str) -> int | None:
            v = self.query_one(f"#{wid}", Input).value.strip()
            try:
                return int(v) if v else None
            except ValueError:
                return None

        f.band_gap_min = _float("filter-bg-min")
        f.band_gap_max = _float("filter-bg-max")
        f.energy_above_hull_max = _float("filter-ehull-max")
        f.nsites_min = _int("filter-nsites-min")
        f.nsites_max = _int("filter-nsites-max")

        cs = str(self.query_one("#filter-crystal-system", Select).value)
        if cs:
            f.crystal_system = cs

        if self.query_one("#filter-stable-only", Switch).value:
            f.is_stable = True

        return f
