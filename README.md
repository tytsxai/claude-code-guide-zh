<!--
SEO/GEO meta: Claude Code 中文指南 / Claude Code 中文文档 / Claude Code 教程 / Claude Code CLI 中文 /
Anthropic Claude Code Chinese guide / DeepSeek 文档自动翻译 / Markdown 翻译流水线 / GitHub Actions 自动同步.
-->

# Claude Code 完全指南（中文版）· Claude Code Complete Guide in Chinese

> **一句话 / TL;DR**：这是 [Claude Code](https://github.com/anthropics/claude-code)（Anthropic 官方的终端 AI 编程助手 / agentic coding CLI）社区指南 [`Cranot/claude-code-guide`](https://github.com/Cranot/claude-code-guide) 的**中文镜像**，并附带一套**自动同步 + DeepSeek 机器翻译**的开源流水线，让中文译文持续跟随上游英文原文更新。
>
> **In one line**: A continuously auto-synced, machine-translated **Chinese mirror** of the Claude Code CLI guide, plus the open-source pipeline (Python + GitHub Actions + DeepSeek) that keeps the translation up to date with upstream.

[![上游 Upstream](https://img.shields.io/badge/上游-Cranot%2Fclaude--code--guide-black?logo=github)](https://github.com/Cranot/claude-code-guide)
[![Claude Code](https://img.shields.io/badge/关于-Claude_Code-7c3aed?logo=anthropic)](https://github.com/anthropics/claude-code)
[![翻译引擎 DeepSeek](https://img.shields.io/badge/翻译引擎-DeepSeek-5b6cff)](https://api.deepseek.com)
[![同步状态 Sync](https://img.shields.io/badge/定时同步-已暂停（上游停更）-lightgrey)](#-自动化流水线--github-actions)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](#-技术栈--tech-stack)

## 📖 直接阅读中文指南 / Read the Guide

> **完整中文指南 → [`content/README.md`](./content/README.md)** —— 这是上游英文指南的完整简体中文译文，覆盖安装、命令、MCP、Hooks、Skills、Plugins、Subagents、SDK、配置与故障排查。
>
> - 📘 [完整中文指南 · Full Chinese Guide → `content/README.md`](./content/README.md)
> - ❓ [常见问题 · FAQ → `docs/FAQ.md`](./docs/FAQ.md)
> - 🧩 [架构说明 · Architecture → `docs/ARCHITECTURE.md`](./docs/ARCHITECTURE.md)
> - 🗒️ [同步更新日志 · Sync Log → `content/update-log-zh.md`](./content/update-log-zh.md)

> ⚠️ 译文为机器自动翻译，**一切以[官方英文文档](https://code.claude.com/docs/en/overview)与[上游仓库](https://github.com/Cranot/claude-code-guide)为准**。本项目为非官方社区翻译。

> 🗿 **维护状态（2026-07-20）**：上游 [`Cranot/claude-code-guide`](https://github.com/Cranot/claude-code-guide) 自 **2026-02-14**（commit `712c838`）起已停止更新。本仓译文**已完整同步到该提交**，内容与上游一致。因此每小时定时同步任务已暂停，仓库转入**维护模式**：内容保留可用，接受译文勘误 PR；若上游恢复更新，取消 [`sync.yml`](./.github/workflows/sync.yml) 中 `schedule` 的注释即可恢复自动同步，或直接手动触发一次 workflow。

---

## 🧭 这是什么 / What & Why

**问题**：Claude Code 的优质学习资料几乎都是英文，更新频繁，中文开发者跟进成本高、容易看到过时内容。

**本项目做两件事**：

1. **一份持续更新的 Claude Code 中文指南** —— 把上游英文指南完整翻译为高可读性的简体中文（见 [`content/`](./content/)）。
2. **一套可复用的「英文文档 → 中文」自动翻译流水线** —— 用 Python + GitHub Actions + DeepSeek 实现增量同步、结构保真翻译、自动提交。它本身也可以拿去翻译**任意** Markdown 仓库。

> 简言之：既是「**Claude Code 中文文档**」，也是「**一个开源的文档本地化（i18n）工具**」。

## 👤 适合谁 / Who It's For

- **中文 Claude Code 用户 / 学习者**：想用母语系统学习 Claude Code CLI、命令、MCP、Hooks、Skills。
- **想做文档本地化的维护者**：需要把某个英文 Markdown 仓库**持续**翻译成中文，且不想每次手动搬运。
- **研究自动翻译流水线的开发者**：想参考「结构保真的 LLM 文档翻译」「多 Key 轮询」「增量同步 + 缓存」的实现。

## ✨ 核心功能 / Features

- **增量同步 Incremental sync**：基于 `git diff` 只处理上游有变化的 Markdown，不重复翻译、不浪费 API。
- **结构保真翻译 Structure-preserving translation**：标题 / 正文 / 代码块**分离处理**，标题层级逐字沿用原文，代码块**完全不送入模型、逐字节保留**，杜绝围栏破坏与层级丢失。
- **锚点自愈 Anchor rewriting**：英文锚点按中文标题重新计算改写，保证目录与页内链接在 GitHub 上可正常跳转。
- **多 Key 轮询与故障转移 Multi-key rotation**：支持多个 DeepSeek API Key 负载均衡，限流 / 鉴权失败自动隔离切换。
- **章节级缓存 Chunk-level cache**：按内容哈希缓存翻译结果，未变动段落零成本复用。
- **术语一致性 Terminology consistency**：[`glossary.json`](./glossary.json)（翻译时提示）+ [`fixups.json`](./fixups.json)（译后确定性修订）双层保证术语统一（如 `pipeline→流水线`、`sub-agents→子代理`、`Changelog→更新日志`）。
- **密钥安全 Secret-safe**：API Key 仅来自环境变量 / GitHub Secrets，**绝不**硬编码或入库。
- **CI 自动化 Automation**：[GitHub Actions](./.github/workflows/sync.yml) 增量同步并提交译文（定时任务当前已暂停，可手动触发）。

## 🧱 技术栈 / Tech Stack

| 层 | 选型 |
|---|---|
| 语言 Language | **Python 3.10+**（CI 使用 3.12，本地已在 3.14 验证） |
| 依赖 Dependencies | 仅 [`requests`](./requirements.txt) **≥2.31,<3**（其余由标准库完成） |
| 翻译模型 LLM | **DeepSeek** `deepseek-v4-flash`（默认）/ `deepseek-chat` / `deepseek-reasoner` |
| 自动化 CI | **GitHub Actions**（cron 已暂停 + 手动触发） |
| 数据格式 | Markdown、JSON（状态 / 术语 / 缓存） |

## 🚀 快速开始 / Quick Start

### A. 只想读中文指南（零依赖）

直接打开 **[`content/README.md`](./content/README.md)** 即可阅读，无需安装任何东西。

### B. 在本地运行翻译流水线

```bash
# 1) 克隆
git clone https://github.com/tytsxai/claude-code-guide-zh.git
cd claude-code-guide-zh

# 2) 安装依赖
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 3) 配置 DeepSeek 密钥（.env 已被 .gitignore，不会入库）
#    申请 Key：https://platform.deepseek.com → 注册后在后台创建 API Key
cp .env.example .env
#   编辑 .env，填入一个或多个 Key（逗号 / 空格 / 分号分隔）
set -a; source .env; set +a

# 4) 预览将翻译哪些文件（不调用 API）
python -m tools.sync --dry-run

# 5) 增量同步 + 翻译
python -m tools.sync

# 6) （可选）强制全量重翻
python -m tools.sync --full
```

> 命令、路径与 `tools/` 下真实代码一致。`python -m tools.sync` 支持 `--dry-run` 与 `--full` 两个参数。

## 🎯 使用场景 / Use Cases

- 用中文系统学习 **Claude Code CLI**（安装、命令、MCP、Hooks、Skills、Plugins、SDK）。
- 为团队/社区维护一份**自动跟随上游**的中文技术文档镜像。
- 把本流水线指向任意英文 Markdown 仓库（改 `UPSTREAM_REPO`），做**持续本地化**（出处声明 banner 需按新仓库微调，详见 [FAQ](./docs/FAQ.md)）。
- 学习「LLM 翻译如何不破坏 Markdown 结构」「多 Key 轮询」「增量翻译缓存」的工程实现。

## 🔧 工作原理 / How It Works

```
上游英文仓库 ──git diff──> 变更的 .md
   │
   ├─ 解析：标题 / 正文 / 代码块分离（structured_doc.py）
   ├─ 翻译：标题批量翻译 + 正文分块翻译（DeepSeek，多 Key 并行，translator.py）
   │        代码块逐字节保留、不送模型
   ├─ 修订：glossary 术语提示 + fixups 确定性替换
   ├─ 锚点：英文锚点 → 中文标题锚点改写
   └─ 写回：content/ 镜像目录 + 更新 .sync-state.json
```

详见 **[`docs/ARCHITECTURE.md`](./docs/ARCHITECTURE.md)**（结构保真翻译引擎设计）。

## ⚙️ 配置 / Configuration

所有配置通过环境变量读取（默认值见下表，定义在 [`tools/config.py`](./tools/config.py)）：

| 环境变量 Env var | 说明 | 默认值 |
|---|---|---|
| `DEEPSEEK_API_KEYS` | 一个或多个 Key，逗号/空格/分号分隔，用于轮询与故障转移 | —（必填） |
| `DEEPSEEK_API_KEY` | 单 Key 写法（与上者二选一） | — |
| `DEEPSEEK_MODEL` | 翻译模型 | `deepseek-v4-flash` |
| `DEEPSEEK_BASE_URL` | API 地址 | `https://api.deepseek.com` |
| `DEEPSEEK_MAX_TOKENS` | 单次输出上限（防截断） | `8192` |
| `MAX_CHUNK_CHARS` | 单次翻译片段最大字符数 | `6000` |
| `TRANSLATE_CONCURRENCY` | 并发翻译数（跨多 Key 扇出） | `6` |
| `DEEPSEEK_TIMEOUT` | 单次请求超时（秒） | `300` |
| `MAX_RETRIES_PER_KEY` | 每个 Key 的重试次数 | `3` |
| `DEEPSEEK_TEMPERATURE` | 采样温度；不设则不发送（推理模型可能拒绝该参数） | 不发送 |
| `UPSTREAM_REPO` | 上游仓库地址（完整 git URL） | `https://github.com/Cranot/claude-code-guide.git` |
| `UPSTREAM_BRANCH` | 上游分支 | `main` |
| `PROJECT_REPO_URL` | 本项目仓库地址（用于译文署名 banner） | 本仓库 URL |

> 完整环境变量与默认值以 [`tools/config.py`](./tools/config.py) 为权威来源。

> ℹ️ **关于模型**：`deepseek-v4-flash` 是真实可用的轻量推理模型（已对 API 实测）。它会单独返回 `reasoning_content` 并消耗少量推理 token，因此默认显式设置 `DEEPSEEK_MAX_TOKENS=8192` 以避免长段落被截断。可替换为 `deepseek-chat`（V3.x）或 `deepseek-reasoner`（R1）。

## 🤖 自动化流水线 / GitHub Actions

[`.github/workflows/sync.yml`](./.github/workflows/sync.yml) 执行：拉取上游 → 与上次同步 commit 做 diff → DeepSeek 翻译变更 → 自动提交 `content/`。手动触发（`workflow_dispatch`）时可勾选 `full` 选项强制全量重翻。

**启用自动同步**：在仓库 `Settings → Secrets and variables → Actions` 添加：

- Secret `DEEPSEEK_API_KEYS`：你的一个或多个 Key（逗号分隔）。
- （可选）Variable `DEEPSEEK_MODEL`：覆盖默认模型。

API Key 全程只从 Secrets 注入，不出现在代码、日志或提交中。

## 🛡️ 翻译质量保障 / Quality

机器翻译要达到可发布质量，本流水线内置多重确定性保障：

- **结构零损失**：标题数量/层级与原文一致；代码块逐字节保留；译后自动校验。
- **锚点可跳转**：页内目录链接按中文标题重算，GitHub 上点击有效。
- **术语统一**：`glossary.json` + `fixups.json` 双层归一（如 pipeline→流水线、sub-agents→子代理）。
- **代码逐字保留（有意取舍）**：代码块、命令、路径中的内容（含注释）保持英文原样，确保技术准确、不破坏可执行性。
- **可选多智能体质检**：逐章节对照「英 vs 中」查遗漏/误译/术语/格式，高危项独立复核后修订。

> 本仓库初版译文已通过上述流程：结构校验显示标题与代码块逐字节一致、页内锚点全部可解析。详见 [`docs/FAQ.md`](./docs/FAQ.md) 中「翻译质量如何保证」。

## ❓ 常见问题 / FAQ

完整 FAQ 见 **[`docs/FAQ.md`](./docs/FAQ.md)**。最常见的几条：

- **这是官方文档吗？** 不是。本项目是非官方社区翻译，**以官方英文为准**。
- **译文有多新？** 译文已同步至上游最新提交 `712c838`（2026-02-14）。上游自该日起未再更新，定时同步已暂停；上游恢复更新后手动触发或恢复 cron 即可继续。
- **能换成别的模型/仓库吗？** 能。改 `DEEPSEEK_MODEL` 换模型，改 `UPSTREAM_REPO` 翻译其它英文 Markdown 仓库。
- **为什么代码注释还是英文？** 有意为之 —— 代码区块逐字保留以保证准确与可执行。

## 🚧 限制与注意事项 / Limitations

- **机器翻译**：可能存在个别误译/不自然表达，欢迎提 Issue / PR；技术细节请对照英文原文。
- **非官方**：与 Anthropic、Claude Code 团队及上游作者无隶属关系。
- **代码/注释不翻译**：代码块默认保持英文（见上）。
- **依赖上游结构**：上游若大改目录结构，可能需要同步调整。
- **API 成本**：全量翻译会消耗 DeepSeek token；增量同步成本很低。

## 🔖 关键词 / Keywords

`Claude Code` · `Claude Code 中文` · `Claude Code 中文文档` · `Claude Code 中文指南` · `Claude Code 教程` · `Claude Code CLI` · `Anthropic` · `agentic coding` · `AI 编程助手` · `MCP` · `Model Context Protocol` · `Hooks` · `Skills` · `Plugins` · `Subagents` · `DeepSeek 翻译` · `文档自动翻译` · `Markdown 翻译` · `i18n` · `GitHub Actions 自动化` · `多 Key 轮询` · `增量同步`

## 📄 版权与许可 / License & Attribution

本项目是上游英文文档的**翻译衍生作品**。原始内容版权归原作者 [@Cranot](https://github.com/Cranot) 所有，详见 [`NOTICE`](./NOTICE)。译文仅供学习交流，**一切以官方英文原文为准**。如原作者或官方提出异议，将及时配合调整或下架。

---

🤖 本仓库由自动化流水线持续维护；翻译由机器生成，可能存在疏漏，欢迎 [提 Issue / PR](https://github.com/tytsxai/claude-code-guide-zh/issues) 修正。
