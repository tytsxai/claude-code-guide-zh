# 常见问题 FAQ · claude-code-guide-zh

面向中文读者的常见问题；技术细节以 [`README.md`](../README.md) 与 [`tools/config.py`](../tools/config.py) 为准。

**快速跳转**：[关于项目](#关于项目--about) · [使用](#使用--usage) · [翻译质量](#翻译质量--quality) · [成本与安全](#成本与安全--cost--security)

---

## 关于项目 / About

### 这是 Claude Code 的官方中文文档吗？
不是。本项目是**非官方社区翻译**，把社区指南 [`Cranot/claude-code-guide`](https://github.com/Cranot/claude-code-guide) 自动翻译为中文。**一切以[官方英文文档](https://code.claude.com/docs/en/overview)为准**。与 Anthropic、Claude Code 团队及上游作者无隶属关系。

### Claude Code 是什么？
Claude Code 是 Anthropic 推出的**终端 agentic AI 编程助手 / CLI**：理解代码库、直接编辑文件、运行命令，并支持 MCP、Hooks、Skills、Plugins、Subagents 扩展。本项目翻译的就是它的使用指南；完整中文内容见 [`content/README.md`](../content/README.md)。

### 这个项目和上游英文仓库是什么关系？
本项目**只翻译、不改写**上游内容，并通过流水线持续跟随上游更新。原文版权归上游作者所有（见 [`NOTICE`](../NOTICE)）。

---

## 使用 / Usage

### 我只想读中文文档，需要安装吗？
不需要。直接打开 [`content/README.md`](../content/README.md) 阅读即可，零依赖。

### 怎么在本地自己跑翻译？
见 README 的[快速开始](../README.md#-快速开始--quick-start)。核心三步：`pip install -r requirements.txt` → 配置 `.env` 里的 `DEEPSEEK_API_KEYS` → `python -m tools.sync`。

### 译文多久更新一次？
[GitHub Actions](../.github/workflows/sync.yml) **每小时**检查上游；只要上游有新提交，就自动翻译变更部分并提交。也可手动触发或本地运行。

### 能用别的翻译模型吗？
能。设置环境变量 `DEEPSEEK_MODEL`，可选 `deepseek-v4-flash`（默认）、`deepseek-chat`、`deepseek-reasoner`。

### 能拿这套流水线翻译别的英文仓库吗？
可以。把 `UPSTREAM_REPO` 改成目标仓库地址，它就会同样做「增量同步 + 结构保真翻译」，对任意 Markdown 仓库通用。注意：`content/README.md` 顶部的「出处声明 banner」目前为本上游定制（写在 [`tools/config.py`](../tools/config.py) 与 [`tools/sync.py`](../tools/sync.py) 中），换库时需相应调整。

---

## 翻译质量 / Quality

### 翻译质量怎么保证？
多重确定性保障：标题/正文/代码**分离翻译**，标题层级逐字沿用原文；**代码块完全不送入模型、逐字节保留**；译后自动校验标题数量、代码块、页内锚点；术语经 `glossary.json` + `fixups.json` 双层归一。初版译文还经过逐章节「英 vs 中」对照质检。

### 为什么代码块里的注释还是英文？
**有意为之**。代码、命令、路径（含注释）逐字保留，避免机器翻译破坏可执行性或改变技术含义。如需翻译注释，可在此基础上扩展。

### 页内目录链接（锚点）为什么能正常跳转？
GitHub 用标题文本生成锚点，标题译成中文后英文锚点会失效。本项目在翻译后**按中文标题重新计算并改写所有页内链接**，因此目录可正常跳转。详见 [`docs/ARCHITECTURE.md`](./ARCHITECTURE.md)。

### 发现翻译错误怎么办？
欢迎在仓库 [提 Issue 或 PR](https://github.com/tytsxai/claude-code-guide-zh/issues)。确定性的术语/定点修正可沉淀进 `fixups.json`，每次运行自动复用。

---

## 成本与安全 / Cost & Security

### 翻译会消耗多少 API？
**全量**翻译（`--full`）会翻译整篇；**增量**同步只翻译变更段落，配合章节级缓存，日常成本很低。

### 我的 API Key 安全吗？
Key **仅**从环境变量 / GitHub Secrets 读取，绝不硬编码或写入仓库；`.env` 已被 `.gitignore`。CI 中通过加密 Secret 注入，不出现在日志或提交里。

### 用的什么许可？
翻译衍生作品，原始内容版权归上游作者。详见 [`NOTICE`](../NOTICE)。
