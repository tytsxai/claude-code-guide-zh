# Claude Code 完全指南 · 中文版

[![上游仓库](https://img.shields.io/badge/上游-Cranot%2Fclaude--code--guide-black)](https://github.com/Cranot/claude-code-guide)
[![翻译引擎](https://img.shields.io/badge/翻译-DeepSeek-5b6cff)](https://api.deepseek.com)
[![自动同步](https://img.shields.io/badge/自动同步-每小时-brightgreen)](#自动化流水线)

> 本项目是 [`Cranot/claude-code-guide`](https://github.com/Cranot/claude-code-guide) 的**中文同步翻译版**。
> 通过自动化流水线追踪上游英文仓库的更新，实时翻译为高质量简体中文，建成一个持续更新的中文镜像。

## 📖 阅读指南

> 完整译文位于 **[`content/README.md`](./content/README.md)**，由流水线自动生成。
> 首次运行同步脚本（见下文）后，该目录会镜像上游的目录结构填充中文译文。

- [完整中文指南 → `content/README.md`](./content/README.md)
- [同步更新日志 → `content/update-log-zh.md`](./content/update-log-zh.md)

## ✨ 特性

- **实时内容同步**：检测上游新提交，只处理有变化的文件，避免重复翻译。
- **高质量翻译**：调用 DeepSeek 模型，保持 Markdown 结构、代码块与技术术语准确；可通过 [`glossary.json`](./glossary.json) 统一术语。
- **多 Key 轮询**：支持多个 API Key 做负载均衡与故障转移，单 Key 触发限流时自动切换。
- **片段级缓存**：按章节切分并缓存翻译结果，未变动的章节不重复消耗 API。
- **结构镜像**：译文放在 `content/` 下，与上游目录结构一一对应。
- **密钥安全**：所有 API Key 仅从环境变量 / GitHub Secrets 读取，**绝不**硬编码或入库。

## 🗂️ 项目结构

```
claude-code-guide-zh/
├── README.md                 # 本文件（项目主页）
├── content/                  # 译文输出，镜像上游目录结构（自动生成）
│   ├── README.md             # 完整中文指南
│   └── update-log-zh.md      # 中文同步日志
├── glossary.json             # 术语表（保持英文 / 固定译法）
├── fixups.json               # 译后确定性修订（术语归一化 + 定点修正）
├── tools/                    # 同步 + 翻译流水线
│   ├── sync.py               # 入口：拉取上游、diff、翻译、写回
│   ├── translator.py         # DeepSeek 客户端 + 多 Key 轮询 + 缓存 + 结构化翻译
│   ├── structured_doc.py     # 标题/正文/代码分离、锚点改写（结构零损失）
│   ├── markdown_chunker.py   # 按章节切分（不切断代码块）
│   ├── fixups.py             # 应用 fixups.json
│   ├── config.py             # 配置（全部从环境变量读取密钥）
│   └── state.py              # 同步状态（已翻译到哪个上游 commit）
├── .github/workflows/sync.yml# 定时自动同步的 GitHub Actions
├── requirements.txt
├── .env.example              # 环境变量示例（复制为 .env，勿入库）
├── .sync-state.json          # 记录上次同步的上游 commit
└── NOTICE                    # 上游出处与版权声明
```

## 🚀 本地运行

```bash
cd claude-code-guide-zh
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 配置密钥（不要把 .env 提交到仓库）
cp .env.example .env
# 编辑 .env，填入一个或多个 DeepSeek API Key（逗号分隔）

set -a; source .env; set +a

# 预览将要翻译哪些文件（不调用 API）
python -m tools.sync --dry-run

# 执行增量同步 + 翻译
python -m tools.sync

# 强制全量重翻
python -m tools.sync --full
```

## ⚙️ 配置说明

| 环境变量 | 说明 | 默认值 |
|---|---|---|
| `DEEPSEEK_API_KEYS` | 一个或多个 Key，逗号/空格分隔，用于轮询与故障转移 | —（必填） |
| `DEEPSEEK_API_KEY` | 单 Key 写法（与上者二选一） | — |
| `DEEPSEEK_MODEL` | 翻译模型 | `deepseek-chat` |
| `DEEPSEEK_BASE_URL` | API 地址 | `https://api.deepseek.com` |
| `UPSTREAM_REPO` | 上游仓库地址 | Cranot/claude-code-guide |
| `MAX_CHUNK_CHARS` | 单次翻译片段最大字符数 | `6000` |

> ℹ️ **关于模型**：`deepseek-v4-flash` 是真实可用的轻量推理模型（已对 API 实测验证），
> 也是本项目默认模型。它会单独返回 `reasoning_content` 并消耗少量推理 token，因此本项目
> 显式设置了 `DEEPSEEK_MAX_TOKENS=8192` 以避免大段落被截断。可选替代：`deepseek-chat`、`deepseek-reasoner`。

## 🤖 自动化流水线

[`.github/workflows/sync.yml`](./.github/workflows/sync.yml) 每小时（及手动触发）执行：

1. 拉取上游最新代码；
2. 与上次同步的 commit 做 diff，找出变更的 Markdown；
3. 调用 DeepSeek 翻译，写入 `content/`；
4. 自动提交并推送译文。

**配置 Secrets：** 在仓库 `Settings → Secrets and variables → Actions` 中添加：

- Secret `DEEPSEEK_API_KEYS`：你的一个或多个 Key（逗号分隔）。
- （可选）Variable `DEEPSEEK_MODEL`：覆盖默认模型。

API Key 全程只从 Secrets 注入，不会出现在代码或日志里。

## 🛡️ 翻译质量保障

为保证「机器翻译」也能达到可发布的质量，流水线内置了多重保障：

- **结构零损失**：标题与正文分离翻译，标题层级直接沿用英文原文逐字复制，保证标题数量/层级与原文 100% 一致；代码块（含围栏）完全不送入模型、逐字节保留；译后自动校验。
- **锚点自愈**：英文锚点（`#what-is-claude-code`）在译文中按中文标题重新计算并改写，保证目录与页内链接在 GitHub 上可点击跳转。
- **术语统一**：`glossary.json`（翻译时提示）+ [`fixups.json`](./fixups.json)（译后确定性替换）双层保证术语一致（如 pipeline→流水线、sub-agents→子代理）。
- **确定性修订**：`fixups.json` 收录人工确认的定点修正，每次运行自动复用，使流水线对已知问题「自愈」。
- **代码逐字保留**：代码块、命令、路径中的内容（包括注释）默认保持英文原样，以确保技术准确、避免破坏可执行性；这是有意为之的取舍。
- **多智能体质检（可选）**：可对「英文原文 vs 中文译文」逐章节做并行对照质检（遗漏/误译/术语/格式），高危结论再经独立复核确认后人工修订。本仓库的初版译文已经过该流程。

经上述流程，初版译文已达成：标题 222/222、代码块 238/238 逐字节一致、页内锚点 36/36 可解析。

## 📦 仓库托管建议

按你的习惯：先放在组织（如 `tytsxai-stack`）下做 private，开源后再 transfer 到个人账户 `tytsxai`。

## 📄 版权与许可

本项目是上游英文文档的**翻译衍生作品**。原始内容版权归原作者
[@Cranot](https://github.com/Cranot) 所有，详见 [`NOTICE`](./NOTICE)。译文仅供学习交流，
**一切以官方英文原文为准**。如原作者或官方提出异议，将及时配合调整或下架。

---

🤖 本仓库由自动化流水线持续维护，翻译由机器生成，可能存在疏漏，欢迎提 Issue / PR 修正。
