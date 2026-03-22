"""Internationalization for mp-search TUI.

Set language via MP_SEARCH_LANG environment variable or ~/.config/mp-search/config.env.
Supported: "zh" (中文), "en" (English, default).
"""

from __future__ import annotations

import mp_search.config as _cfg

_TEXTS: dict[str, dict[str, str | list | tuple]] = {
    # ── Search modes ──
    "mode_formula":      {"zh": "化学式  (如 TiO2)",     "en": "Formula  (e.g. TiO2)"},
    "mode_elements":     {"zh": "元素    (如 Fe,O)",     "en": "Elements (e.g. Fe,O)"},
    "mode_chemsys":      {"zh": "化学体系 (如 Li-Fe-O)", "en": "Chemsys  (e.g. Li-Fe-O)"},
    # ── Placeholders ──
    "ph_formula":        {"zh": "输入化学式，如 TiO2",       "en": "Enter formula, e.g. TiO2"},
    "ph_elements":       {"zh": "输入元素，逗号分隔，如 Fe,O",  "en": "Enter elements, e.g. Fe,O"},
    "ph_chemsys":        {"zh": "输入化学体系，如 Li-Fe-O",   "en": "Enter chemsys, e.g. Li-Fe-O"},
    "ph_min":            {"zh": "最小", "en": "Min"},
    "ph_max":            {"zh": "最大", "en": "Max"},
    # ── Buttons / labels ──
    "btn_search":        {"zh": "搜索", "en": "Search"},
    "filter_title":      {"zh": "筛选条件", "en": "Filters"},
    "lbl_bandgap":       {"zh": "带隙 (eV):", "en": "Band Gap (eV):"},
    "lbl_ehull":         {"zh": "凸包能 (eV/atom):", "en": "E_hull (eV/atom):"},
    "lbl_nsites":        {"zh": "原子数:", "en": "# Atoms:"},
    "lbl_crystal":       {"zh": "晶系:", "en": "Crystal System:"},
    "lbl_stable_only":   {"zh": "仅稳定相:", "en": "Stable Only:"},
    "crystal_all":       {"zh": "全部", "en": "All"},
    # ── Table columns ──
    "col_id":            {"zh": "ID", "en": "ID"},
    "col_formula":       {"zh": "化学式", "en": "Formula"},
    "col_nsites":        {"zh": "原子数", "en": "Atoms"},
    "col_bandgap":       {"zh": "带隙(eV)", "en": "BG(eV)"},
    "col_ehull":         {"zh": "E_hull", "en": "E_hull"},
    "col_spacegroup":    {"zh": "空间群", "en": "Spacegroup"},
    "col_crystal":       {"zh": "晶系", "en": "Crystal Sys"},
    "col_stable":        {"zh": "稳定", "en": "Stable"},
    # ── Key bindings ──
    "key_quit":          {"zh": "退出", "en": "Quit"},
    "key_search":        {"zh": "搜索", "en": "Search"},
    "key_filter":        {"zh": "筛选", "en": "Filter"},
    "key_export":        {"zh": "导出", "en": "Export"},
    "key_back":          {"zh": "返回", "en": "Back"},
    # ── Status messages ──
    "status_ready":      {"zh": "就绪 | API 已连接，输入搜索内容后按 Enter",
                          "en": "Ready | API connected, enter query and press Enter"},
    "status_no_key":     {"zh": "⚠ MP_API_KEY 未设置 — 请通过设置向导配置",
                          "en": "⚠ MP_API_KEY not set — configure via setup wizard"},
    "status_searching":  {"zh": "正在搜索 {} ...", "en": "Searching {} ..."},
    "status_found":      {"zh": "找到 {} 个材料 | Enter 查看详情，e 导出",
                          "en": "Found {} materials | Enter for detail, e to export"},
    "status_error":      {"zh": "⚠ 搜索出错: {}", "en": "⚠ Search error: {}"},
    "status_hint":       {"zh": "就绪 | 按 / 聚焦搜索框，f 切换筛选面板",
                          "en": "Ready | Press / to search, f to toggle filters"},
    # ── Notifications ──
    "notify_no_key":     {"zh": "API Key 未配置，请重启 mp-search 重新设置",
                          "en": "API Key not configured, restart mp-search to set up"},
    "notify_no_client":  {"zh": "API 未连接，请重启 mp-search 重新配置",
                          "en": "API not connected, restart mp-search to reconfigure"},
    "notify_empty":      {"zh": "请输入搜索内容", "en": "Please enter a search query"},
    "notify_select":     {"zh": "请先搜索并选中材料", "en": "Search and select a material first"},
    "notify_select_one": {"zh": "请选中一个材料", "en": "Select a material"},
    "notify_search_first": {"zh": "请先搜索材料", "en": "Search for materials first"},
    # ── Detail screen ──
    "detail_basic":      {"zh": "── 基本信息 ──", "en": "── Basic Info ──"},
    "detail_props":      {"zh": "── 物理性质 ──", "en": "── Properties ──"},
    "detail_symmetry":   {"zh": "── 对称性 ──", "en": "── Symmetry ──"},
    "detail_lattice":    {"zh": "── 晶格参数 ──", "en": "── Lattice ──"},
    "detail_mid":        {"zh": "Material ID", "en": "Material ID"},
    "detail_formula":    {"zh": "化学式", "en": "Formula"},
    "detail_chemsys":    {"zh": "化学体系", "en": "Chemsys"},
    "detail_nelements":  {"zh": "元素种类", "en": "# Elements"},
    "detail_nsites":     {"zh": "原子数", "en": "# Atoms"},
    "detail_stability":  {"zh": "稳定性", "en": "Stability"},
    "detail_stable":     {"zh": "稳定 ✓", "en": "Stable ✓"},
    "detail_metastable": {"zh": "亚稳 ✗", "en": "Metastable ✗"},
    "detail_bandgap":    {"zh": "带隙", "en": "Band Gap"},
    "detail_ehull":      {"zh": "凸包能", "en": "E_hull"},
    "detail_eform":      {"zh": "形成能", "en": "Form. Energy"},
    "detail_density":    {"zh": "密度", "en": "Density"},
    "detail_volume":     {"zh": "体积", "en": "Volume"},
    "detail_spacegroup": {"zh": "空间群", "en": "Spacegroup"},
    "detail_crystal":    {"zh": "晶系", "en": "Crystal Sys"},
    # ── Export ──
    "btn_all_export":    {"zh": "全部导出", "en": "Export All"},
    "export_ok":         {"zh": "已导出至 {}", "en": "Exported to {}"},
    "export_fail":       {"zh": "导出失败: {}", "en": "Export failed: {}"},
}


def t(key: str, *args: object) -> str:
    """Get translated string by key, optionally formatting with args."""
    entry = _TEXTS.get(key)
    if not entry:
        return key
    text = entry.get(_cfg.LANG, entry.get("en", key))
    if args:
        return str(text).format(*args)
    return str(text)
