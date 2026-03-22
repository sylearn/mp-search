from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import requests
from pymatgen.core.structure import Structure

MP_API_BASE = "https://api.materialsproject.org"

SUMMARY_FIELDS = ",".join([
    "material_id", "formula_pretty", "nsites", "band_gap",
    "energy_above_hull", "symmetry", "density", "volume",
    "formation_energy_per_atom", "is_stable", "nelements",
    "chemsys", "structure",
])


@dataclass
class SearchFilters:
    """材料搜索过滤条件"""
    band_gap_min: Optional[float] = None
    band_gap_max: Optional[float] = None
    energy_above_hull_max: Optional[float] = None
    nsites_min: Optional[int] = None
    nsites_max: Optional[int] = None
    crystal_system: Optional[str] = None
    is_stable: Optional[bool] = None


@dataclass
class MaterialSummary:
    """标准化的材料摘要数据"""
    material_id: str = ""
    formula: str = ""
    nsites: int = 0
    band_gap: float = 0.0
    energy_above_hull: float = 0.0
    spacegroup_symbol: str = "N/A"
    spacegroup_number: int = 0
    crystal_system: str = "N/A"
    density: float = 0.0
    volume: float = 0.0
    formation_energy: float = 0.0
    is_stable: bool = False
    nelements: int = 0
    chemsys: str = ""
    structure: Any = field(default=None, repr=False)


class MPClient:
    """Materials Project REST API 客户端

    直接使用 requests 调用 MP API，避免 mp-api 库
    在 textual 事件循环中触发的 subprocess FD 冲突。
    """

    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError(
                "MP_API_KEY 未设置。请在 .env 中添加 MP_API_KEY=<your_key>"
            )
        self.api_key = api_key
        self._session: Optional[requests.Session] = None

    def connect(self) -> MPClient:
        self._session = requests.Session()
        self._session.headers.update({"X-API-KEY": self.api_key})
        return self

    def close(self) -> None:
        if self._session:
            self._session.close()
            self._session = None

    def __enter__(self) -> MPClient:
        return self.connect()

    def __exit__(self, *args: object) -> None:
        self.close()

    # -- search --

    def search_by_formula(
        self, formula: str, filters: Optional[SearchFilters] = None
    ) -> List[MaterialSummary]:
        params = {"formula": formula}
        return self._search(params, filters)

    def search_by_elements(
        self, elements: List[str], filters: Optional[SearchFilters] = None
    ) -> List[MaterialSummary]:
        params = {"elements": ",".join(elements)}
        return self._search(params, filters)

    def search_by_chemsys(
        self, chemsys: str, filters: Optional[SearchFilters] = None
    ) -> List[MaterialSummary]:
        params = {"chemsys": chemsys}
        return self._search(params, filters)

    # -- internal --

    def _search(
        self, params: Dict[str, str], filters: Optional[SearchFilters]
    ) -> List[MaterialSummary]:
        params["_fields"] = SUMMARY_FIELDS
        params["_limit"] = "200"

        if filters:
            if filters.band_gap_min is not None:
                params["band_gap_min"] = str(filters.band_gap_min)
            if filters.band_gap_max is not None:
                params["band_gap_max"] = str(filters.band_gap_max)
            if filters.energy_above_hull_max is not None:
                params["energy_above_hull_max"] = str(filters.energy_above_hull_max)
            if filters.nsites_min is not None:
                params["nsites_min"] = str(filters.nsites_min)
            if filters.nsites_max is not None:
                params["nsites_max"] = str(filters.nsites_max)
            if filters.crystal_system:
                params["crystal_system"] = filters.crystal_system
            if filters.is_stable is True:
                params["is_stable"] = "true"

        url = f"{MP_API_BASE}/materials/summary/"
        resp = self._session.get(url, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json().get("data", [])
        return [self._parse(item) for item in data]

    @staticmethod
    def _parse(item: Dict[str, Any]) -> MaterialSummary:
        sym = item.get("symmetry") or {}
        cs = sym.get("crystal_system", "N/A") or "N/A"

        struct = None
        struct_dict = item.get("structure")
        if struct_dict and isinstance(struct_dict, dict):
            try:
                struct = Structure.from_dict(struct_dict)
            except Exception:
                pass

        return MaterialSummary(
            material_id=str(item.get("material_id", "")),
            formula=item.get("formula_pretty", "") or "",
            nsites=item.get("nsites", 0) or 0,
            band_gap=item.get("band_gap", 0.0) or 0.0,
            energy_above_hull=item.get("energy_above_hull", 0.0) or 0.0,
            spacegroup_symbol=sym.get("symbol", "N/A") or "N/A",
            spacegroup_number=sym.get("number", 0) or 0,
            crystal_system=cs,
            density=item.get("density", 0.0) or 0.0,
            volume=item.get("volume", 0.0) or 0.0,
            formation_energy=item.get("formation_energy_per_atom", 0.0) or 0.0,
            is_stable=item.get("is_stable", False) or False,
            nelements=item.get("nelements", 0) or 0,
            chemsys=item.get("chemsys", "") or "",
            structure=struct,
        )
