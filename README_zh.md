# MP Search

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org)

> [English](README.md)

基于终端 UI 的 [Materials Project](https://materialsproject.org) 材料搜索工具，使用 [Textual](https://textual.textualize.io/) 构建。

---

## 功能

- **三种搜索模式** — 按化学式、元素、化学体系搜索
- **属性筛选** — 带隙、凸包能、原子数、晶系、稳定性
- **材料详情** — 完整属性、晶格参数、对称性信息
- **导出** — 一键导出 POSCAR / CIF / JSON
- **国际化** — 中文和英文界面（通过 `.env` 配置切换）
- **原生 REST API** — 直接调用 Materials Project REST API，避免 `mp-api` 库的兼容性问题

---

## 快速开始

### 1. 获取 API Key

前往 [Materials Project](https://next-gen.materialsproject.org/api) 注册并获取 API Key。

### 2. 安装

```bash
git clone https://github.com/sylearn/mp-search.git
cd mp-search

python -m venv .venv
source .venv/bin/activate

pip install -e .
```

### 3. 配置

```bash
cp .env.example .env
```

编辑 `.env`，填入你的 API Key：

```env
MP_API_KEY="你的API密钥"
```

### 4. 运行

```bash
mp-search
```

---

## 配置项

| 变量 | 说明 | 默认值 |
|---|---|---|
| `MP_API_KEY` | **必填。** Materials Project API 密钥 | — |
| `MP_EXPORT_DIR` | 导出目录路径 | `./result/mp_search` |
| `MP_SEARCH_LANG` | 界面语言：`zh` 或 `en` | `zh` |

---

## 快捷键

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
├── pyproject.toml          # 包配置
├── .env.example            # 环境变量模板
├── LICENSE
├── README.md               # 英文文档
├── README_zh.md            # 中文文档
└── mp_search/              # Python 包
    ├── __main__.py          # CLI 入口
    ├── config.py            # 配置加载
    ├── i18n.py              # 国际化
    ├── api/
    │   └── client.py        # Materials Project REST API 客户端
    ├── export/
    │   └── writer.py        # POSCAR / CIF / JSON 导出
    └── tui/
        ├── app.py           # TUI 主界面
        └── detail.py        # 材料详情弹窗
```

---

## 开发

```bash
pip install -e .

# 修改代码后无需重新安装，直接运行
mp-search
```

---

## 许可证

[MIT](LICENSE)
