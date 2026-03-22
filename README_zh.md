# MP Search

[![PyPI version](https://img.shields.io/pypi/v/mp-search.svg)](https://pypi.org/project/mp-search/)
[![Python 3.10+](https://img.shields.io/pypi/pyversions/mp-search.svg)](https://pypi.org/project/mp-search/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

> [English](README.md)

基于终端 UI 的 [Materials Project](https://materialsproject.org) 材料搜索工具，使用 [Textual](https://textual.textualize.io/) 构建。

## 预览

![主界面](assets/01_main.png)

![搜索结果](assets/02_results.png)

![筛选面板](assets/03_filters.png)

---

## 功能

- **三种搜索模式** — 按化学式、元素、化学体系搜索
- **属性筛选** — 带隙、凸包能、原子数、晶系、稳定性
- **材料详情** — 完整属性、晶格参数、对称性信息
- **导出** — 一键导出 POSCAR / CIF / JSON
- **国际化** — 中文和英文界面切换

---

## 安装

### 从 PyPI 安装（推荐）

```bash
pip install mp-search
```

或使用 [uv](https://docs.astral.sh/uv/)：

```bash
# 安装为全局工具
uv tool install mp-search

# 或临时运行（无需安装）
uvx mp-search
```

### 从源码安装

```bash
git clone https://github.com/sylearn/mp-search.git
cd mp-search
pip install -e .
```

---

## 配置

从 [Materials Project](https://next-gen.materialsproject.org/api) 获取 API Key，然后在运行 `mp-search` 的目录下创建 `.env` 文件：

```bash
cp .env.example .env
```

| 变量 | 说明 | 默认值 |
|---|---|---|
| `MP_API_KEY` | **必填。** Materials Project API 密钥 | — |
| `MP_EXPORT_DIR` | 导出目录路径 | `./result/mp_search` |
| `MP_SEARCH_LANG` | 界面语言：`zh` 或 `en` | `zh` |

---

## 使用

```bash
mp-search
```

### 快捷键

| 按键 | 功能 |
|---|---|
| `/` | 聚焦搜索框 |
| `f` | 切换筛选面板 |
| `Enter` | 查看选中材料详情 |
| `e` | 导出选中材料 |
| `Escape` | 从详情返回 |
| `q` | 退出 |

---

## 项目结构

```
mp-search/
├── pyproject.toml
├── .env.example
└── mp_search/
    ├── __main__.py      # CLI 入口
    ├── config.py         # 配置
    ├── i18n.py           # 国际化
    ├── api/client.py     # REST API 客户端
    ├── export/writer.py  # POSCAR / CIF / JSON 导出
    └── tui/
        ├── app.py        # TUI 主界面
        └── detail.py     # 详情弹窗
```

---

## 许可证

[MIT](LICENSE)
