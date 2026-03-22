# MP Search

[![PyPI version](https://img.shields.io/pypi/v/mp-search.svg)](https://pypi.org/project/mp-search/)
[![Python 3.10+](https://img.shields.io/pypi/pyversions/mp-search.svg)](https://pypi.org/project/mp-search/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

> [中文文档](README_zh.md)

A terminal UI tool for searching materials from the [Materials Project](https://materialsproject.org) database. Built with [Textual](https://textual.textualize.io/).

## Preview

![Main Interface](assets/01_main.png)

![Search Results](assets/02_results.png)

![Filters Panel](assets/03_filters.png)

---

## Features

- **Three search modes** — Search by chemical formula, elements, or chemical system
- **Property filters** — Filter by band gap, energy above hull, atom count, crystal system, and stability
- **Material detail view** — Full properties, lattice parameters, and symmetry info
- **Export** — One-click export to POSCAR / CIF / JSON
- **Internationalization** — Chinese and English UI (configurable via `.env`)

---

## Installation

### From PyPI (recommended)

```bash
pip install mp-search
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
# Install as a global tool
uv tool install mp-search

# Or run directly without installing
uvx mp-search
```

### From source

```bash
git clone https://github.com/sylearn/mp-search.git
cd mp-search
pip install -e .
```

---

## Configuration

Get your API key from [Materials Project](https://next-gen.materialsproject.org/api), then create a `.env` file in the directory where you run `mp-search`:

```bash
cp .env.example .env
```

| Variable | Description | Default |
|---|---|---|
| `MP_API_KEY` | **Required.** Materials Project API key | — |
| `MP_EXPORT_DIR` | Export directory path | `./result/mp_search` |
| `MP_SEARCH_LANG` | UI language: `zh` or `en` | `zh` |

---

## Usage

```bash
mp-search
```

### Keyboard Shortcuts

| Key | Action |
|---|---|
| `/` | Focus search input |
| `f` | Toggle filter panel |
| `Enter` | View selected material detail |
| `e` | Export selected material |
| `Escape` | Back from detail |
| `q` | Quit |

---

## Project Structure

```
mp-search/
├── pyproject.toml
├── .env.example
└── mp_search/
    ├── __main__.py      # CLI entry point
    ├── config.py         # Configuration
    ├── i18n.py           # Internationalization
    ├── api/client.py     # REST API client
    ├── export/writer.py  # POSCAR / CIF / JSON export
    └── tui/
        ├── app.py        # Main TUI
        └── detail.py     # Detail modal
```

---

## License

[MIT](LICENSE)
