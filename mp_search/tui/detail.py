from __future__ import annotations

from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, VerticalScroll
from textual.screen import ModalScreen
from textual.widgets import Button, Static

import mp_search.config as _cfg
from mp_search.api.client import MaterialSummary
from mp_search.export.writer import export_all, export_cif, export_json, export_poscar
from mp_search.i18n import t


class DetailScreen(ModalScreen):
    """Material detail modal with export actions."""

    DEFAULT_CSS = """
    DetailScreen { align: center middle; }
    #detail-container {
        width: 76; max-height: 88%;
        background: $surface; border: thick $primary; padding: 1 2;
    }
    #detail-info { margin-bottom: 1; }
    #detail-buttons { height: auto; align: center middle; padding: 1 0; }
    #detail-buttons Button { margin: 0 1; }
    """

    BINDINGS = [Binding("escape", "dismiss", "")]

    def __init__(self, material: MaterialSummary) -> None:
        super().__init__()
        self.material = material
        self.BINDINGS = [Binding("escape", "dismiss", t("key_back"))]

    def compose(self) -> ComposeResult:
        with VerticalScroll(id="detail-container"):
            yield Static(self._render_info(), id="detail-info")
            with Horizontal(id="detail-buttons"):
                yield Button("POSCAR", variant="primary", id="btn-poscar")
                yield Button("CIF", variant="primary", id="btn-cif")
                yield Button("JSON", variant="primary", id="btn-json")
                yield Button(t("btn_all_export"), variant="success", id="btn-all")
                yield Button(t("key_back"), variant="default", id="btn-back")

    def _render_info(self) -> str:
        m = self.material
        stable = t("detail_stable") if m.is_stable else t("detail_metastable")
        lines = [
            f"[bold underline]{m.formula}[/bold underline]  ({m.material_id})",
            "",
            f"[bold]{t('detail_basic')}[/bold]",
            f"  {t('detail_mid'):<16}{m.material_id}",
            f"  {t('detail_formula'):<16}{m.formula}",
            f"  {t('detail_chemsys'):<16}{m.chemsys}",
            f"  {t('detail_nelements'):<16}{m.nelements}",
            f"  {t('detail_nsites'):<16}{m.nsites}",
            f"  {t('detail_stability'):<16}{stable}",
            "",
            f"[bold]{t('detail_props')}[/bold]",
            f"  {t('detail_bandgap'):<16}{m.band_gap:.4f} eV",
            f"  {t('detail_ehull'):<16}{m.energy_above_hull:.4f} eV/atom",
            f"  {t('detail_eform'):<16}{m.formation_energy:.4f} eV/atom",
            f"  {t('detail_density'):<16}{m.density:.4f} g/cm\u00b3",
            f"  {t('detail_volume'):<16}{m.volume:.2f} \u00c5\u00b3",
            "",
            f"[bold]{t('detail_symmetry')}[/bold]",
            f"  {t('detail_spacegroup'):<16}{m.spacegroup_symbol} (#{m.spacegroup_number})",
            f"  {t('detail_crystal'):<16}{m.crystal_system}",
        ]

        if m.structure:
            lat = m.structure.lattice
            lines += [
                "",
                f"[bold]{t('detail_lattice')}[/bold]",
                f"  a = {lat.a:.4f} \u00c5     \u03b1 = {lat.alpha:.2f}\u00b0",
                f"  b = {lat.b:.4f} \u00c5     \u03b2 = {lat.beta:.2f}\u00b0",
                f"  c = {lat.c:.4f} \u00c5     \u03b3 = {lat.gamma:.2f}\u00b0",
            ]

        return "\n".join(lines)

    # -- export handlers --

    @on(Button.Pressed, "#btn-poscar")
    def _on_poscar(self) -> None:
        self._do_export("poscar")

    @on(Button.Pressed, "#btn-cif")
    def _on_cif(self) -> None:
        self._do_export("cif")

    @on(Button.Pressed, "#btn-json")
    def _on_json(self) -> None:
        self._do_export("json")

    @on(Button.Pressed, "#btn-all")
    def _on_all(self) -> None:
        self._do_export("all")

    @on(Button.Pressed, "#btn-back")
    def _on_back(self) -> None:
        self.dismiss()

    def _do_export(self, fmt: str) -> None:
        export_dir = _cfg.DEFAULT_EXPORT_DIR
        try:
            if fmt == "poscar":
                path = export_poscar(self.material, export_dir)
            elif fmt == "cif":
                path = export_cif(self.material, export_dir)
            elif fmt == "json":
                path = export_json(self.material, export_dir)
            else:
                paths = export_all(self.material, export_dir)
                path = next(iter(paths.values()))
                path = str(path).rsplit("/", 1)[0]

            self.notify(t("export_ok", path), severity="information", timeout=5)
        except Exception as e:
            self.notify(t("export_fail", e), severity="error", timeout=5)
