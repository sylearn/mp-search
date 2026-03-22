from __future__ import annotations

import json
import os
from typing import Dict

from mp_search.api.client import MaterialSummary


def _ensure_dir(path: str) -> str:
    os.makedirs(path, exist_ok=True)
    return path


def export_poscar(material: MaterialSummary, output_dir: str) -> str:
    if not material.structure:
        raise ValueError(f"{material.material_id} 没有可用的结构数据")
    mat_dir = _ensure_dir(os.path.join(output_dir, material.material_id))
    filepath = os.path.join(mat_dir, "POSCAR")
    material.structure.to(filename=filepath, fmt="poscar")
    return filepath


def export_cif(material: MaterialSummary, output_dir: str) -> str:
    if not material.structure:
        raise ValueError(f"{material.material_id} 没有可用的结构数据")
    mat_dir = _ensure_dir(os.path.join(output_dir, material.material_id))
    filepath = os.path.join(mat_dir, f"{material.material_id}.cif")
    material.structure.to(filename=filepath, fmt="cif")
    return filepath


def export_json(material: MaterialSummary, output_dir: str) -> str:
    mat_dir = _ensure_dir(os.path.join(output_dir, material.material_id))
    filepath = os.path.join(mat_dir, "data.json")

    data = {
        "material_id": material.material_id,
        "formula": material.formula,
        "nsites": material.nsites,
        "band_gap": material.band_gap,
        "energy_above_hull": material.energy_above_hull,
        "spacegroup_symbol": material.spacegroup_symbol,
        "spacegroup_number": material.spacegroup_number,
        "crystal_system": material.crystal_system,
        "density": material.density,
        "volume": material.volume,
        "formation_energy": material.formation_energy,
        "is_stable": material.is_stable,
        "nelements": material.nelements,
        "chemsys": material.chemsys,
    }
    if material.structure:
        data["structure"] = material.structure.as_dict()

    with open(filepath, "w") as f:
        json.dump(data, f, indent=4, ensure_ascii=False, default=str)
    return filepath


def export_all(material: MaterialSummary, output_dir: str) -> Dict[str, str]:
    return {
        "poscar": export_poscar(material, output_dir),
        "cif": export_cif(material, output_dir),
        "json": export_json(material, output_dir),
    }
