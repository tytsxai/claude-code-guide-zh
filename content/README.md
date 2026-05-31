> **🌏 中文翻译版** · 本文档由机器自动翻译，并由 [`claude-code-guide-zh`](https://github.com/tytsxai/claude-code-guide-zh) 流水线**每小时**持续同步自上游英文仓库
> [Cranot/claude-code-guide](https://github.com/Cranot/claude-code-guide)（原作者 [@Cranot](https://github.com/Cranot)）。
> 译文仅供学习参考，**以[官方英文文档](https://code.claude.com/docs/en/overview)为准**；翻译问题欢迎到[本仓库](https://github.com/tytsxai/claude-code-guide-zh/issues) 提 Issue。
> 翻译引擎：DeepSeek。

---

# Claude Code CLI 完全指南

[![Official Docs](https://img.shields.io/badge/Official_Docs-code.claude.com-blue)](https://code.claude.com/docs/en/overview) [![GitHub](https://img.shields.io/badge/GitHub-anthropics%2Fclaude--code-black)](https://github.com/anthropics/claude-code) [![NPM](https://img.shields.io/badge/NPM-@anthropic--ai%2Fclaude--code-red)](https://www.npmjs.com/package/@anthropic-ai/claude-code) [![Auto-Updated](https://img.shields.io/badge/Auto--Updated-Every%202%20Days-brightgreen)](#自动更新流水线)

**快速链接：** [开始使用](#什么是-claude-code) · [命令](#快速参考) · [MCP 设置](https://code.claude.com/docs/en/mcp) · [设置](https://code.claude.com/docs/en/settings) · [SDK](https://code.claude.com/docs/en/sdk) · [更新日志](#变更日志)

> **🔄 实时指南**：每 2 天从[官方文档](https://code.claude.com/docs/en/overview)、[GitHub 发布版本](https://github.com/anthropics/claude-code/releases)和 [Anthropic 更新日志](https://www.anthropic.com/changelog)自动更新。参见 [update-log.md](./update-log.md)。

> **🤖 适用于 AI 智能体**：同时针对人类和 AI 进行了优化。`[官方]` = 来自 code.claude.com。`[社区]` = 观察到的模式。`[实验性]` = 未经验证。

## 什么是 Claude Code？

**Claude Code 是一款驻留在你终端中的智能体式 AI 编程助手。** 它能理解你的代码库，直接编辑文件、运行命令，并通过自然语言对话帮助你更快地编写代码。

**核心功能：**
- 💬 终端中的自然语言界面
- 📝 直接文件编辑与命令执行
- 🔍 完整的项目上下文感知
- 🔗 通过 MCP（Model Context Protocol）实现外部集成
- 🤖 通过 Skills、Hooks 和 Plugins 进行扩展
- 🛡️ 沙箱化执行，保障安全

**安装：**
```bash
# Quick Install (macOS, Linux, WSL)
curl -fsSL https://claude.ai/install.sh | bash

# Windows PowerShell
irm https://claude.ai/install.ps1 | iex

# Windows CMD
curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd

# Alternative: Homebrew (macOS/Linux)
brew install --cask claude-code

# Alternative: WinGet (Windows)
winget install Anthropic.ClaudeCode

# Alternative: NPM (⚠️ Deprecated - use native install instead)
npm install -g @anthropic-ai/claude-code

claude --version  # Verify installation
```

**官方文档：** https://code.claude.com/docs/en/overview

---

## 目录

| 入门指南 | 核心功能 | 实践应用 | 参考 |
|-----------------|---------------|-----------------|-----------|
| [什么是 Claude Code?](#什么是-claude-code) | [技能系统](#skills-系统) | [开发工作流](#开发工作流) | [安全](#安全注意事项) |
| [核心概念](#核心概念) | [内置命令](#内置命令) | [工具协同](#工具协同) | [SDK 集成](#sdk集成) |
| [快速入门指南](#快速入门指南) | [钩子系统](#hooks-系统) | [示例库](#示例库) | [故障排除](#故障排除) |
| [快速参考](#快速参考) | [MCP 集成](#mcp-集成) | [最佳实践](#最佳实践) | [更新日志](#变更日志) |
| | [子代理](#子代理) | | [自动更新流水线](#自动更新流水线) |
| | [智能体团队](#智能体团队) | | |
| | [插件](#插件) | | |

## 快速参考

### 基本命令 [OFFICIAL]

```bash
# Starting Claude Code
claude                    # Start interactive session
claude -p "task"          # Print mode (non-interactive)
claude --continue         # Continue last session
claude --resume <id>      # Resume specific session

# Session Management
/help                     # Show available commands
/exit                     # End session
/compact                  # Reduce context size
/compact [instructions]  # Compact conversation with optional focus instructions

# Background Tasks
/bashes                   # List background processes
/kill <id>               # Stop background process

# Discovery
/commands                 # List skills and commands
/hooks                   # Show configured hooks
/skills                  # List available Skills (NEW)
/plugin                  # Manage plugins
```

**来源:** [CLI 参考](https://code.claude.com/docs/en/cli-reference)

### CLI 标志参考 [OFFICIAL]

```bash
# Output Control
claude -p, --print "task"          # Print mode: non-interactive, prints result and exits
claude --output-format json         # Output format: text, json, or stream-json
claude --input-format text          # Input format: text or stream-json
claude --verbose                    # Enable verbose logging (full turn-by-turn output)

# Session Management
claude --continue                   # Continue from last session
claude --resume <session-id>        # Resume specific session by ID or name
claude --from-pr <pr>               # Resume session linked to GitHub PR number or URL [NEW]
claude --fork-session               # Create new session ID instead of reusing original
claude --session-id <uuid>          # Use specific session ID (must be valid UUID)

# Remote Sessions (claude.ai subscribers)
claude --remote "task"              # Create web session on claude.ai
claude --teleport                   # Resume web session in local terminal

# Debugging & Logging
claude --debug                      # Enable debug mode (with optional category filtering)
claude --debug "api,mcp"            # Debug specific categories
claude --debug "!statsig,!file"     # Exclude categories with !

# Model & Agent Configuration
claude --model <name>               # Specify model (sonnet, opus, haiku, or full name)
claude --fallback-model <name>      # Fallback model when default overloaded (print mode)
claude --agent <name>               # Specify custom agent (overrides settings)
claude --agents '<json>'            # Define custom subagents dynamically via JSON

# System Prompt Customization
claude --system-prompt "prompt"     # Replace entire default system prompt
claude --system-prompt-file <path>  # Replace with file contents (print mode only)
claude --append-system-prompt "..."  # Append to default system prompt
claude --append-system-prompt-file <path>  # Append file contents (print mode only)

# Tool & Permission Management
claude --tools "Bash,Read,Edit"     # Restrict built-in tools (use "" to disable all)
claude --allowedTools "Bash(git:*)" # Tools that execute without prompting
claude --disallowedTools "Edit"     # Tools removed from context
claude --permission-mode plan       # Begin in specified permission mode
claude --dangerously-skip-permissions  # Skip all permission prompts ⚠️
claude --allow-dangerously-skip-permissions  # Enable bypass option without activating [NEW]
claude --permission-prompt-tool <mcp-tool>  # MCP tool for permission prompts (non-interactive) [NEW]

# Budget & Execution Limits (print mode)
claude --max-budget-usd 5.00        # Maximum dollar amount for API calls
claude --max-turns 3                # Limit number of agentic turns
claude --json-schema '<schema>'     # Get validated JSON output matching schema (print mode) [NEW]

# Directory & Configuration
claude --add-dir ../apps ../lib     # Add additional working directories
claude --plugin-dir ./my-plugins    # Load plugins from directories
claude --settings ./settings.json   # Path to settings JSON file
claude --setting-sources user,project  # Comma-separated list of setting sources [NEW]
claude --mcp-config ./mcp.json      # Load MCP servers from JSON file
claude --strict-mcp-config          # Only use MCP servers from --mcp-config

# IDE & Browser Integration
claude --ide                        # Auto-connect to IDE on startup
claude --chrome                     # Enable Chrome browser integration
claude --no-chrome                  # Disable Chrome browser integration

# Agent Teams [NEW]
claude --teammate-mode in-process   # Teammates display in main terminal
claude --teammate-mode tmux         # Each teammate in own pane (requires tmux/iTerm2)
claude --teammate-mode auto         # Auto-detect (default)

# Setup & Maintenance
claude --init                       # Run Setup hooks and start interactive mode
claude --init-only                  # Run Setup hooks and exit (no interactive session)
claude --maintenance                # Run Setup hooks with maintenance trigger and exit

# Other Options
claude --disable-slash-commands     # Disable all skills and slash commands
claude --no-session-persistence     # Disable session persistence (print mode)
claude --betas interleaved-thinking # Beta headers for API requests
claude --include-partial-messages   # Include partial streaming events (with stream-json) [NEW]
```

**常见标识组合：**

```bash
# One-off task with JSON output
claude --print "analyze this code" --output-format json

# Debug MCP and API issues
claude --debug "api,mcp"

# Resume session with specific model
claude --resume auth-refactor --model opus

# Non-interactive with budget limit (CI/CD)
claude -p --max-budget-usd 5.00 --output-format json "run tests"

# Custom subagents for specialized work
claude --agents '{"reviewer":{"description":"Code reviewer","prompt":"Review for bugs"}}'

# Remote session for claude.ai subscribers
claude --remote "fix the login bug"
```

**来源:** [CLI 参考](https://code.claude.com/docs/en/cli-reference)

### 核心工具 [OFFICIAL]

| 工具 | 目的 | 需要权限 |
|------|------|----------|
| **Read** | 读取文件、图片、PDF | 否 |
| **Write** | 创建新文件 | 是 |
| **Edit** | 修改现有文件 | 是 |
| **Bash** | 执行 shell 命令 | 是 |
| **Grep** | 用正则表达式搜索内容 | 否 |
| **Glob** | 按模式查找文件 | 否 |
| **TodoWrite** | 任务管理 | 否 |
| **Task** | 启动子代理 | 否 |
| **WebFetch** | 获取网页内容 | 是 |
| **WebSearch** | 搜索网页 | 是 |
| **NotebookEdit** | 编辑 Jupyter 笔记本 | 是 |
| **NotebookRead** | 读取 Jupyter 笔记本 | 否 |

**来源：** [设置参考](https://code.claude.com/docs/en/settings)

## 核心概念

### 1. Claude Code 的工作原理 [OFFICIAL]

Claude Code 通过终端中的**对话式界面**运行：

```bash
# You describe what you want
$ claude
> "Add user authentication to the API"

# Claude Code:
1. Analyzes your codebase structure
2. Plans the implementation
3. Requests permission for file edits (first time)
4. Writes code directly to your files
5. Can run tests and verify changes
6. Creates git commits if requested
```

**关键原则：**
- **自然语言**：只需描述你需要的功能——无需特殊语法
- **直接操作**：在获得你的许可后编辑文件并运行命令
- **上下文感知**：理解整个项目结构
- **渐进信任**：在执行新操作时根据需要请求权限
- **可脚本化**：可通过 SDK 实现自动化

**来源：** [概述](https://code.claude.com/docs/en/overview)

### 2. 权限模型 [OFFICIAL]

Claude Code 使用**增量权限系统**来保障安全：

```bash
# Permission Modes
"ask"    # Prompt for each use (default for new operations)
"allow"  # Permit without asking
"deny"   # Block completely

# Permission Priority [NEW v2.1.27]
# Content-level rules override tool-level rules
# Example: allow: ["Bash"], ask: ["Bash(rm *)"]
#   -> Bash is generally allowed, but "rm *" commands require confirmation

# Tools Requiring Permission
- Bash (command execution)
- Write/Edit/NotebookEdit (file modifications)
- WebFetch/WebSearch (network access)
- Skill (skills and custom commands)

# Tools Not Requiring Permission (Safe Operations)
- Read/NotebookRead (reading files)
- Grep/Glob (searching)
- TodoWrite (task tracking)
- Task (sub-agents)
```

**配置权限：**

在项目中创建 `.claude/settings.json` 文件，或全局创建 `~/.claude/settings.json` 文件：

```json
{
  "permissions": {
    "defaultMode": "ask",
    "allow": {
      "Bash": ["git status", "git diff", "git log", "npm test", "npm run*"],
      "Read": {},
      "Edit": {}
    },
    "deny": {
      "Write": ["*.env", ".env.*", ".git/*"],
      "Edit": ["*.env", ".env.*"]
    },
    "additionalDirectories": [
      "/path/to/other/project"
    ]
  }
}
```

**来源:** [设置](https://code.claude.com/docs/en/settings)

### 3. 项目上下文 - CLAUDE.md [COMMUNITY]

项目根目录下的 **CLAUDE.md** 文件可跨会话提供持久上下文：

<details>
<summary><strong>示例 CLAUDE.md 文件（点击展开）</strong></summary>

    # Project: My Application

    ## Critical Context (Read First)
    - Language: TypeScript + Node.js
    - Framework: Express + React
    - Database: PostgreSQL with Prisma ORM
    - Testing: Jest + React Testing Library

    ## Commands That Work
    npm run dev          # Start dev server (port 3000)
    npm test             # Run all tests
    npm run lint         # ESLint check
    npm run typecheck    # TypeScript validation
    npm run db:migrate   # Run Prisma migrations

    ## Important Patterns
    - All API routes in /src/routes - RESTful structure
    - Database queries use Prisma Client
    - Auth uses JWT tokens (implementation in /src/auth)
    - Frontend components in /src/components
    - API responses: {success: boolean, data: any, error?: string}

    ## Gotchas & What NOT to Do
    - DON'T modify /generated folder (auto-generated by Prisma)
    - DON'T commit .env files (use .env.example instead)
    - ALWAYS run npm run db:migrate after pulling schema changes
    - DON'T use `any` type in TypeScript - use proper typing

    ## File Structure
    /src
      /routes       # Express API routes
      /services     # Business logic
      /models       # Type definitions
      /middleware   # Express middleware
      /utils        # Shared utilities
      /auth         # Authentication logic

    ## Recent Learnings
    - [2026-01-15] Payment webhook needs raw body parser for Stripe
    - [2026-01-10] Redis pool: {maxRetriesPerRequest: 3}

</details>

**为什么 CLAUDE.md 有帮助：**
- ✅ 在会话开始时立即提供上下文
- ✅ 减少重新解释项目结构的需要
- ✅ 存储项目特定的模式与约定
- ✅ 记录哪些方法有效（以及哪些无效）
- ✅ 通过 Git 与团队共享
- ✅ AI 优化的格式，便于 Claude 快速理解

**注意：** 虽然 CLAUDE.md 并非官方功能，但它是被广泛采用的社区模式。如果项目根目录存在该文件，Claude Code 会自动读取。

### 4. 工具参考 [OFFICIAL]

#### Read 工具
**目的：** 读取并分析文件

```bash
# Examples
Read file_path="/src/app.ts"
Read file_path="/docs/screenshot.png"  # Can read images!
Read file_path="/docs/guide.pdf"       # Can read PDFs!
Read file_path="/docs/guide.pdf" pages="1-5"  # Read specific PDF pages [NEW v2.1.30]
```

**功能：**
- 读取任意文本文件（代码、配置、日志等）
- 处理图片（截图、图表、流程图等）
- 处理 PDF 文件——提取文本和视觉内容
- 解析 Jupyter 笔记本（.ipynb 文件）
- 返回带行号的内容（`cat -n` 格式）
- 支持通过偏移量/限制参数读取大文件

**PDF 参数** [新增 v2.1.30]：
- `pages`：可选页面范围（如 `"1-5"`、`"1,3,5"`），用于读取指定页面
- 大 PDF（超过 10 页）在 @提及时会返回轻量级引用
- PDF 限制：最多 100 页，文件大小 20MB

**特殊功能：**
- **图片**：Claude 可读取错误截图、UI 设计图、架构图
- **PDF**：提取并分析 PDF 内容，适用于文档和需求文档
- **笔记本**：完全访问代码单元格、Markdown 文本和输出

#### Write 工具
**目的：** 创建新文件

```bash
Write file_path="/src/newFile.ts"
      content="export const config = {...}"
```

**行为：**
- 使用指定内容创建新文件
- 如果文件已存在，将会**覆盖**（对于现有文件请使用 Edit 工具）
- 每个会话首次使用时需要权限
- 如有需要会自动创建父目录

**最佳实践：** 修改现有文件请使用 Edit 工具，Write 工具仅用于创建新文件。

#### Edit 工具
**目的：** 通过精确的字符串替换来修改现有文件

```bash
Edit file_path="/src/app.ts"
     old_string="const port = 3000"
     new_string="const port = process.env.PORT || 3000"
```

**重要提示：**
- 要求**精确字符串匹配**，包括空白字符和缩进
- 如果文件中`old_string`不唯一则操作失败（使用更大上下文或`replace_all`）
- 使用`replace_all=true`替换所有匹配项（可用于重命名）
- 编辑前必须先读取文件

**常见模式：**
```bash
# 1. Read file to see exact content
Read file_path="/src/app.ts"

# 2. Edit with exact string match
Edit file_path="/src/app.ts"
     old_string="function login() {
  return 'TODO';
}"
     new_string="function login() {
  return authenticateUser();
}"
```

#### Bash 工具
**用途：**执行 shell 命令

```bash
Bash command="npm test"
Bash command="git status"
Bash command="find . -name '*.test.ts'"
```

**功能：**
- 可运行任何 shell 命令
- 支持后台执行（`run_in_background=true`）
- 可配置超时时间（默认 2 分钟，最长 10 分钟）
- Git 操作常见（status、diff、log、commit、push）

**安全性：**
- 需获得权限
- 可在设置中按模式限制
- macOS/Linux 上支持沙箱化

**常见 Git 模式：**
```bash
# Check status
Bash command="git status"

# View changes
Bash command="git diff"

# Create commit
Bash command='git add . && git commit -m "feat: add authentication"'

# View history
Bash command="git log --oneline -10"
```

#### Grep 工具
**用途：** 使用正则表达式模式搜索文件内容

```bash
# Find functions
Grep pattern="function.*auth" path="src/" output_mode="content"

# Find TODOs with context
Grep pattern="TODO" output_mode="content" -C=3

# Count occurrences
Grep pattern="import.*from" output_mode="count"

# Case insensitive
Grep pattern="error" -i=true output_mode="files_with_matches"
```

**参数：**
- `pattern`：正则表达式（ripgrep 语法）
- `path`：要搜索的目录或文件（默认：当前目录）
- `output_mode`：
  - `"files_with_matches"`（默认）— 仅输出文件路径
  - `"content"` — 显示匹配行
  - `"count"` — 显示每个文件的匹配次数
- `-A`、`-B`、`-C`：上下文行数（之后、之前、两侧）
- `-i`：忽略大小写
- `-n`：显示行号
- `type`：按文件类型筛选（例如 "js"、"py"、"rust"）
- `glob`：按 glob 模式筛选（例如 "*.test.ts"）

**快速且强大：** 底层使用 ripgrep，在大型代码库上比 bash grep 快得多。

#### Glob 工具
**用途:** 按模式查找文件

```bash
# Find test files
Glob pattern="**/*.test.ts"

# Find specific extensions
Glob pattern="src/**/*.{ts,tsx}"

# Find config files
Glob pattern="**/config.{json,yaml,yml}"
```

**功能特性:**
- 快速模式匹配（适用于任意大小的代码库）
- 按修改时间排序返回文件（最近优先）
- 支持复杂 glob 模式（`**` 表示递归，`{}` 表示选择）

#### TodoWrite 工具
**目的：** 在工作期间管理任务清单

```bash
TodoWrite todos=[
  {
    "content": "Add authentication endpoint",
    "status": "in_progress",
    "activeForm": "Adding authentication endpoint"
  },
  {
    "content": "Write integration tests",
    "status": "pending",
    "activeForm": "Writing integration tests"
  },
  {
    "content": "Update API documentation",
    "status": "pending",
    "activeForm": "Updating API documentation"
  }
]
```

**任务状态：**
- `"pending"` — 尚未开始
- `"in_progress"` — 正在处理（同一时间应**仅有一个**任务处于此状态）
- `"completed"` — 已成功完成

**依赖跟踪** [新增]：v2.1.16 引入了任务依赖跟踪功能，允许任务定义其开始前必须完成的前置条件。这使得复杂的多步骤工作流可以按正确顺序执行。

**最佳实践：**
- 适用于多步骤任务（3 步及以上）
- 同一时间**仅**保持**一个**任务处于 `in_progress` 状态
- 完成后**立即**标记为 `completed`
- 使用描述性的 `content`（要做什么）和 `activeForm`（正在做什么）

**使用时机：**
- ✅ 复杂的多步骤功能
- ✅ 用户提供了多个任务
- ✅ 需要规划的非简单工作
- ❌ 单个简单任务
- ❌ 琐碎操作

#### Task 工具（子代理）
**目的：** 为特定任务启动专门的 AI 代理。

```bash
# Explore codebase
Task subagent_type="Explore"
     prompt="Find all API endpoints and their authentication requirements"

# General purpose agent for complex tasks
Task subagent_type="general-purpose"
     prompt="Research best practices for rate limiting APIs and implement a solution"
```

**可用的子代理类型：**
- `"general-purpose"` — 复杂的多步骤任务、调研、实现
- `"Explore"` — 快速的代码库探索（Glob、Grep、Read、Bash）

**使用时机：**
- 需要网络搜索与分析的调研任务
- 代码库探索（查找模式、理解架构）
- 可独立运行的复杂多步骤操作
- 在继续其他任务的同时进行后台工作

#### WebFetch 工具
**目的：** 获取并分析网页内容

```bash
WebFetch url="https://docs.example.com/api"
         prompt="Extract all endpoint documentation"
```

**功能特性：**
- 将 HTML 转换为 Markdown 以供分析
- 能够通过 prompt 提取特定信息
- 适用于研究文档、文章和参考文献

#### WebSearch 工具
**目的：** 搜索网络以获取当前信息

```bash
WebSearch query="React 19 new features 2024"
```

**用例：**
- 研究当前最佳实践
- 查找最新的库文档
- 检查已知问题或解决方案
- 验证最新的框架功能

**来源：** [CLI 参考](https://code.claude.com/docs/en/cli-reference)、[设置](https://code.claude.com/docs/en/settings)

#### LSP 工具（语言服务器协议） [OFFICIAL]
**目的:** 获取代码智能特性，如转到定义、查找引用和悬停文档。

```bash
LSP operation="goToDefinition"
    filePath="src/utils/auth.ts"
    line=42
    character=15
```

**可用操作:**

| 操作 | 描述 |
|-----------|-------------|
| `goToDefinition` | 查找符号的定义位置 |
| `findReferences` | 查找符号的所有引用 |
| `hover` | 获取符号的文档和类型信息 |
| `documentSymbol` | 获取文档中所有符号（函数、类、变量） |
| `workspaceSymbol` | 在整个工作区中搜索符号 |
| `goToImplementation` | 查找接口或抽象方法的实现 |
| `prepareCallHierarchy` | 获取指定位置的调用层级项 |
| `incomingCalls` | 查找所有调用该位置函数的函数/方法 |
| `outgoingCalls` | 查找该位置函数所调用的所有函数/方法 |

**参数:**
- `operation` (必填): 要执行的 LSP 操作
- `filePath` (必填): 文件的绝对或相对路径
- `line` (必填): 行号（从1开始，与编辑器中显示一致）
- `character` (必填): 字符偏移量（从1开始，与编辑器中显示一致）

**使用场景:**
```bash
# Find where a function is defined
> "Go to the definition of getUserById"

# Find all usages of a function
> "Find all references to the authenticate function"

# Get documentation for a symbol
> "What does the validateToken function do?"

# Explore code structure
> "List all symbols in the auth.ts file"
```

**注意：** LSP 服务器必须针对文件类型进行配置。如果某种语言没有可用的服务器，则会返回错误。

**来源：** [CLI Reference](https://code.claude.com/docs/en/cli-reference)

### 5. 上下文管理 [OFFICIAL]

Claude Code 通过智能管理来维护对话上下文：

#### 上下文命令

```bash
/compact                   # Reduce context by removing old information
/compact "keep auth work"  # Compact with focus instructions (keeps specified context)
```

#### 何时使用

**何时使用 /compact：**
- 长时间会话且包含大量文件读取
- 出现"上下文过大"错误
- 已完成一项重大任务，希望重新开始

**何时使用带指令的 /compact：**
- 上下文正在变大，但希望保留近期工作
- 在相关任务之间切换
- 希望进行智能清理而不丢失重要上下文
- 示例：`/compact "keep the authentication implementation context"`

#### 保留与清除的内容

**保留：**
- CLAUDE.md 内容（你的项目上下文）
- 最近的交互与决策
- 当前任务信息与待办事项
- 仍相关的最新文件读取

**清除：**
- 不再需要的旧文件读取
- 已完成的操作
- 过时的搜索结果
- 不再相关的旧上下文

#### 自动上下文管理

Claude Code 可能会自动压缩，当出现以下情况时：
- Token 限制即将达到
- 存在大量旧文件读取
- 会话时间过长

**来源：** [设置](https://code.claude.com/docs/en/settings)

### 6. 工作区管理 [OFFICIAL]

#### 使用 /add-dir 添加目录

Claude Code 可以同时处理多个目录:

```bash
# Add another directory to current session
/add-dir /path/to/other/project

# Work across multiple projects
> "Update the User type in backend and propagate to frontend"
# Claude can now access both directories
```

**使用场景：**
- 单体仓库开发（前端 + 后端 + 共享库）
- 跨项目重构
- 跨多个项目的依赖更新
- 协调相关仓库之间的变更

**配置：**

您还可以在 `.claude/settings.json` 中预配置其他目录：

```json
{
  "permissions": {
    "additionalDirectories": [
      "/path/to/frontend",
      "/path/to/backend",
      "/path/to/shared-libs"
    ]
  }
}
```

#### 使用 /statusline 配置状态行

自定义状态行中显示的信息：

```bash
# Configure status line
/statusline

# Options typically include:
# - Current model
# - Token usage
# - Session duration
# - Active tools
# - Background processes
```

**优势：**
- 实时监控 Token 用量
- 跟踪会话时长
- 查看活动中的后台进程
- 了解正在使用的工具

**来源：** [CLI Reference](https://code.claude.com/docs/en/cli-reference)

## 快速入门指南

### 您的第一次会话

```bash
# 1. Navigate to your project
cd /path/to/your/project

# 2. Start Claude Code
claude

# 3. Ask Claude to understand your project
> "Read the codebase and explain the project structure"

# Claude will:
- Look for README, package.json, or similar entry points
- Read relevant files (asks permission first time)
- Analyze the code structure
- Provide a summary

# 4. Request an analysis
> "Review the authentication system for security issues"

# Claude will:
- Find authentication-related files
- Analyze the implementation
- Identify potential vulnerabilities
- Suggest improvements

# 5. Make changes
> "Add rate limiting to the login endpoint"

# Claude will:
- Plan the implementation
- Show you what changes will be made
- Request permission to edit files
- Implement the changes
- Can run tests to verify

# 6. Create a commit
> "Create a git commit for these changes"

# Claude will:
- Run git status to see changes
- Review git diff
- Create a descriptive commit message
- Commit the changes
```

### 为 Claude Code 设置项目

#### 1. 创建 CLAUDE.md [COMMUNITY]

这提供了跨所有会话持续存在的上下文：

```bash
# Ask Claude to help create it
> "Create a CLAUDE.md file documenting this project's structure, commands, and conventions"

# Or create manually with:
- Languages and frameworks used
- Important commands (dev, test, build, lint)
- Project structure overview
- Coding conventions
- Known gotchas or issues
```

#### 2. 配置权限（可选） [OFFICIAL]

在你的项目中创建 `.claude/settings.json`:

```json
{
  "permissions": {
    "defaultMode": "ask",
    "allow": {
      "Bash": [
        "npm test",
        "npm run*",
        "git status",
        "git diff",
        "git log*"
      ],
      "Read": {},
      "Grep": {},
      "Glob": {}
    },
    "deny": {
      "Write": ["*.env", ".env.*"],
      "Edit": ["*.env", ".env.*", ".git/*"]
    }
  }
}
```

此配置：
- 允许常见安全命令，无需询问
- 阻止编辑敏感文件
- 文件修改仍需请求许可

#### 3. 测试设置

```bash
> "Run the tests"
# Should execute without permission prompt (if configured)

> "What commands are available?"
# Claude will read package.json and list scripts

> "What's in CLAUDE.md?"
# Claude will read and summarize your project context
```

[快速入门](https://code.claude.com/docs/en/quickstart)，[设置](https://code.claude.com/docs/en/settings)

---

## 高级功能

### 思考模式 [OFFICIAL]

Claude Code 支持扩展思考，用于复杂的推理任务。Opus 4.5 默认启用思考模式。

**激活方法：**

```bash
# Toggle with keyboard shortcut
Alt+T (or Option+T on macOS)  # Toggle thinking on/off

# Or use natural language
> "think about this problem"
> "think harder about the architecture"
> "ultrathink about this security issue"

# Tab key (sticky toggle)
Press Tab to toggle thinking mode on/off for subsequent prompts
```

**思考级别：**

| 触发词 | 思考预算 | 使用场景 |
|--------|----------|----------|
| `think` | 标准 | 通用推理、代码分析 |
| `think harder` | 扩展 | 复杂问题、多种方案 |
| `ultrathink` | 最大 | 关键决策、深度架构分析 |

**最佳实践：**
- 调试复杂问题时使用 `think harder`
- 架构决策或安全审查时使用 `ultrathink`
- 思考内容在 `Ctrl+O` 转录模式下可见
- 思考模式具有粘性，开启后持续生效，直到手动关闭

**来源：** [思考模式](https://code.claude.com/docs/en/thinking-mode)

### 快速模式 [NEW] [OFFICIAL]

快速模式是 Claude Opus 4.6 的一种高速配置，能使响应**速度提升 2.5 倍**，但每 token 成本更高。自 v2.1.36 版本起可用。

**切换快速模式：**
```bash
# Toggle with built-in command
/fast          # Toggle on/off

# Or set in settings
"fastMode": true   # In user settings file
```

**视觉指示：**
- 当快速模式激活时，提示符旁会显示 `↯` 图标
- 速率限制冷却期间，图标变灰

**定价（每百万 Token）：**
| 模式 | 输入（<20万） | 输出 | 输入（>20万） | 输出 |
|------|--------------|--------|---------------|--------|
| 标准 Opus 4.6 | $15 | $75 | $15 | $75 |
| 快速模式 | $30 | $150 | $60 | $225 |

**注意：** 快速模式在 2026 年 2 月 16 日前享受 50% 折扣。

**要求：**
- Claude 订阅计划（Pro/Max/Team/Enterprise）或 Claude Console API
- 已启用额外用量（`/extra-usage`）
- 不适用于第三方供应商（Bedrock、Vertex、Azure Foundry）
- 对于 Teams/Enterprise：管理员需在组织设置中启用

**使用时机：**
- ✅ 对代码更改进行快速迭代
- ✅ 实时调试会话
- ✅ 有时间限制的工作
- ❌ 长时间自主任务（成本更重要）
- ❌ 批处理或 CI/CD 流水线

**快速模式 vs 努力级别：**
| 设置 | 效果 |
|---------|--------|
| **快速模式** | 相同质量，更低延迟，更高成本 |
| **较低努力级别** | 响应更快，质量可能降低 |

对于简单任务，你可以结合两者以获得最快速度。

**速率限制：**
- 与标准 Opus 4.6 的速率限制独立
- 冷却期间自动回退到标准模式
- 冷却结束后重新启用

**来源：** [快速模式](https://code.claude.com/docs/en/fast-mode)

### 计划模式 [OFFICIAL]

Plan Mode 提供了结构化的规划功能，并支持针对复杂任务进行模型选择。

```bash
# Enter plan mode
/plan

# Or Claude may suggest plan mode for complex tasks
> "Implement a complete authentication system"
# Claude: "This is a complex task. Would you like me to create a plan first?"
```

**Plan Mode 功能特性：**
- **Opus 规划，Sonnet 执行** - 使用更强的模型进行规划，使用更快的模型进行实现
- **SonnetPlan Mode** - Sonnet 规划，Haiku 执行（经济高效）
- **Shift+Tab** - 在 plan mode 中自动接受编辑
- **Plan 持久化** - 计划在 `/clear` 后仍然保留

**Plan Mode 工作流程：**
1. Claude 分析任务并创建结构化计划
2. 你审查并批准或修改计划
3. Claude 逐步执行计划
4. 进度通过 TodoWrite 跟踪

**来源：** [Plan Mode](https://code.claude.com/docs/en/plan-mode)

### 后台任务与代理 [OFFICIAL]

在后台运行命令和智能体，同时继续工作。

**键盘快捷键：**
```bash
Ctrl+B  # Background current command or agent (unified shortcut)
```

**后台命令:**
```bash
# Start command in background
> "Run the dev server in background"
> "Start tests in watch mode in background"

# Or prefix with &
> "& npm run dev"

# View background tasks
/tasks
/bashes

# Kill a background task
/kill <task-id>
```

**后台代理:**
```bash
# Launch agent in background
> "Have an Explore agent analyze the codebase architecture in background"

# Agents run asynchronously and notify you when complete
# You receive wake-up messages when background agents finish
```

**特性：**
- 实时输出流式显示到状态行
- 任务完成时发送唤醒通知
- 支持多个并发后台进程
- 大量输出持久化保存到文件

**来源：**[后台任务](https://code.claude.com/docs/en/background-tasks)

### 自动记忆 [NEW]

Claude Code 现在会在工作中自动记录和回忆记忆 (v2.1.32+)。

**工作原理：**
- Claude 会自动记住重要的上下文、决策和模式
- 记忆会在会话之间持久保存，并为未来工作提供信息
- 无需手动干预

**Agent 的记忆范围：**
```markdown
---
name: my-agent
memory: project  # Options: user, project, local
---
```

| 范围 | 存储位置 | 共享范围 |
|-------|---------|--------|
| `user` | `~/.claude/` | 你的所有项目 |
| `project` | `.claude/` | 通过 Git 的团队协作 |
| `local` | `.claude/*.local.*` | 否（已加入 .gitignore 忽略） |

**禁用自动记忆：**
```bash
export CLAUDE_CODE_DISABLE_AUTO_MEMORY=1
```

### 键盘快捷键 [OFFICIAL]

**导航与编辑：**
| 快捷键 | 操作 |
|----------|--------|
| `Ctrl+R` | 搜索命令历史 |
| `Ctrl+O` | 查看对话记录（显示思考过程块） |
| `Ctrl+G` | 在系统文本编辑器中编辑提示 |
| `Ctrl+Y` | Readline 风格粘贴（yank） |
| `Alt+Y` | Yank-pop（在 kill ring 中循环） |
| `Ctrl+B` | 将当前命令/agent 后台运行 |
| `Ctrl+Z` | 挂起/撤销 |

**模型与模式切换：**
| 快捷键 | 操作 |
|----------|--------|
| `Alt+P` (Win/Linux) / `Option+P` (macOS) | 在输入时切换模型 |
| `Alt+T` (Win/Linux) / `Option+T` (macOS) | 切换思考模式 |
| `Tab` | 切换思考（粘性）/ 接受建议 |
| `Shift+Tab` | 自动接受编辑（规划模式）/ 切换模式（Windows） |

**输入与提交：**
| 快捷键 | 操作 |
|----------|--------|
| `Enter` | 提交提示 / 立即接受建议 |
| `Shift+Enter` | 换行（在 iTerm2、WezTerm、Ghostty、Kitty 中可用） |
| `Tab` | 编辑/接受提示建议 |
| `Ctrl+T` | 在 `/theme` 中切换语法高亮 |

**图片与文件处理：**
| 快捷键 | 操作 |
|----------|--------|
| `Cmd+V` (macOS) / `Alt+V` (Windows) | 从剪贴板粘贴图片 |
| `Cmd+N` / `Ctrl+N` | 新建对话（VSCode）|

**Vim 绑定（如已启用）：**
| 快捷键 | 操作 |
|----------|--------|
| `;` and `,` | 重复上一次移动 |
| `y` | Yank 操作符 |
| `p` / `P` | 粘贴 |
| `Alt+B` / `Alt+F` | 单词级导航 |

**登录与认证：**
| 快捷键 | 操作 |
|----------|--------|
| `c` | 在登录时复制 OAuth URL |

**Bash 模式自动补全** [新功能 v2.1.14]：
| 快捷键 | 操作 |
|----------|--------|
| `!` + `Tab` | 基于历史的自动补全——根据历史补全部分命令 |

### 提示建议 [OFFICIAL]

Claude Code 会根据上下文建议提示词（默认启用）。

```bash
# Claude suggests contextual prompts
> _  # Cursor blinking
# Suggestion appears: "Review the changes we made"

# Tab to edit the suggestion
Tab → Edit the suggestion text

# Enter to submit immediately
Enter → Submit the suggestion as-is
```

**配置：**
```bash
# Toggle in /config
/config
# Search for "prompt suggestions"
# Toggle enable/disable
```

### 环境变量 [OFFICIAL]

**核心配置：**
| 变量名 | 说明 |
|--------|------|
| `ANTHROPIC_API_KEY` | 您的 API 密钥 |
| `CLAUDE_CODE_SHELL` | 覆盖 Shell 检测逻辑 |
| `CLAUDE_CODE_TMPDIR` | 自定义临时目录 |
| `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` | 禁用后台任务系统 |
| `CLAUDE_CODE_ENABLE_TASKS` | 设为 `false` 以使用旧版任务系统 [新增于 v2.1.19] |

**显示与界面：**
| 变量名 | 说明 |
|--------|------|
| `CLAUDE_CODE_HIDE_ACCOUNT_INFO` | 在界面中隐藏账户信息 |

**Bash 与命令：**
| 变量名 | 说明 |
|--------|------|
| `BASH_DEFAULT_TIMEOUT_MS` | Bash 命令的默认超时时间 |
| `BASH_MAX_TIMEOUT_MS` | 允许的最大超时时间 |
| `CLAUDE_BASH_NO_LOGIN` | 不使用登录 Shell |
| `CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR` | 保持工作目录不变 |
| `CLAUDE_CODE_SHELL_PREFIX` | Shell 命令的前缀 |

**模型配置：**
| 变量名 | 说明 |
|--------|------|
| `ANTHROPIC_DEFAULT_SONNET_MODEL` | 覆盖默认的 Sonnet 模型 |
| `ANTHROPIC_DEFAULT_OPUS_MODEL` | 覆盖默认的 Opus 模型 |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL` | 覆盖默认的 Haiku 模型 |
| `ANTHROPIC_LOG` | 启用调试日志 |

**MCP 配置：**
| 变量名 | 说明 |
|--------|------|
| `MCP_TIMEOUT` | MCP 连接超时时间 |
| `MCP_TOOL_TIMEOUT` | 单个工具超时时间 |

**文件与上下文：**
| 变量名 | 说明 |
|--------|------|
| `CLAUDE_CODE_FILE_READ_MAX_OUTPUT_TOKENS` | 文件读取的最大 Token 数 |
| `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD` | 设为 `1` 可从 `--add-dir` 目录加载 CLAUDE.md [新增] |
| `CLAUDE_PROJECT_DIR` | 覆盖项目目录 |
| `CLAUDE_PLUGIN_ROOT` | 插件根目录替换路径 |
| `CLAUDE_CONFIG_DIR` | 自定义配置目录 |
| `XDG_CONFIG_HOME` | XDG 配置的基础路径 |

**网络与代理：**
| 变量名 | 说明 |
|--------|------|
| `NODE_EXTRA_CA_CERTS` | 自定义 CA 证书 |
| `NO_PROXY` | 代理排除列表 |
| `CLAUDE_CODE_PROXY_RESOLVES_HOSTS` | 代理 DNS 解析 |

**自动更新与插件：**
| 变量名 | 说明 |
|--------|------|
| `DISABLE_AUTOUPDATER` | 禁用自动更新 |
| `FORCE_AUTOUPDATE_PLUGINS` | 强制插件更新 |
| `CLAUDE_CODE_EXIT_AFTER_STOP_DELAY` | 停止后的退出延迟 |

**监控与遥测：**
| 变量名 | 说明 |
|--------|------|
| `CLAUDE_CODE_ENABLE_TELEMETRY` | 启用 OpenTelemetry 采集（设为 `1`） |
| `OTEL_METRICS_EXPORTER` | OTel 指标导出器（例如 `otlp`） |
| `DISABLE_TELEMETRY` | 选择退出 Statsig 遥测（设为 `1`） |
| `DISABLE_ERROR_REPORTING` | 选择退出 Sentry 错误报告（设为 `1`） |
| `DISABLE_COST_WARNINGS` | 禁用费用警告消息（设为 `1`） |

**高级：**
| 变量名 | 说明 |
|--------|------|
| `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS` | 禁用 anthropic-beta 标头（网关用户的变通方案） |
| `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` | 启用 Agent Teams 功能（设为 `1`）[新增] |
| `CLAUDE_CODE_DISABLE_AUTO_MEMORY` | 禁用自动记忆记录（设为 `1`）[新增] |
| `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` | 禁用后台任务系统（设为 `1`） |
| `DISABLE_INTERLEAVED_THINKING` | 禁用交错思考 |
| `USE_BUILTIN_RIPGREP` | 使用内置的 ripgrep |
| `CLOUD_ML_REGION` | Vertex 的 Cloud ML 区域 |
| `AWS_BEARER_TOKEN_BEDROCK` | AWS 持有者令牌 |
| `MAX_THINKING_TOKENS` | 扩展思考预算（默认值：31,999） |
| `MAX_MCP_OUTPUT_TOKENS` | MCP 工具响应的最大 Token 数（默认值：25,000） |
| `CLAUDE_CODE_MAX_OUTPUT_TOKENS` | 最大输出 Token 数（默认值：32,000，最大值：64,000） |
| `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` | 禁用自动更新、错误报告和遥测 |

### 新设置 [OFFICIAL]

近期新增设置（在 `/config` 或 `settings.json` 中配置）：

```json
{
  // Response language
  "language": "en",  // Claude's response language

  // Git integration
  "attribution": true,  // Add model name to commit bylines
  "respectGitignore": true,  // Respect .gitignore in searches

  // UI preferences
  "showTurnDuration": true,  // Show turn duration messages
  "fileSuggestion": "custom-cmd",  // Custom @ file search command
  "spinnerVerbs": ["analyzing", "thinking", "processing"],  // Custom spinner verbs
  "prefersReducedMotion": false,  // Reduce UI animations for accessibility [NEW v2.1.30]

  // Session behavior
  "companyAnnouncements": true,  // Show startup announcements

  // Plan mode
  "plansDirectory": ".claude/plans"  // Custom directory for plan files
}
```

**Skills Variable Substitution：** [NEW]
```markdown
# In skill files, use ${CLAUDE_SESSION_ID} for session-specific operations
Session ID: ${CLAUDE_SESSION_ID}
```

**项目规则:**
```bash
# New: .claude/rules/ directory for project-specific rules
.claude/rules/
├── coding-style.md      # Coding conventions
├── testing.md           # Testing requirements
└── security.md          # Security guidelines
```

**通配符权限：**
```json
{
  "permissions": {
    "allow": {
      "Bash": ["npm *", "git *"],  // Wildcard patterns
      "mcp__myserver__*": {}       // MCP tool wildcards
    }
  }
}
```

---

## Skills 系统

**Skills 是扩展 Claude Code 的统一能力——既可被 Claude 自动激活，也可通过 `/skill-name` 手动调用。**

> **注意：** 自 v2.1.3 起，自定义斜杠命令（`.claude/commands/` 文件）已合并到 Skills 中。你现有的命令文件保持不变，仍可正常工作。对于新任务，推荐使用 Skills，因为它支持更多功能，例如辅助文件、调用控制和子代理执行。参见[从命令迁移到 Skills](#迁移从命令到技能)。

Claude Code 的 Skills 遵循 [Agent Skills](https://agentskills.io) 开放标准，该标准可跨多种 AI 工具使用。Claude Code 在此基础上扩展了额外功能，如调用控制、子代理执行和动态上下文注入。

### 什么是 Skills？ [OFFICIAL]

Skills 是打包为 `SKILL.md` 文件的指令，用于扩展 Claude Code 的能力。当它们与你的请求相关时，Claude 会加载它们，或者你也可以直接调用它们：

```
# Claude auto-activates a skill based on your request
You: "Review this code for security issues"
Claude: [Loads security-reviewer skill automatically]

# Or you invoke a skill directly
You: /security-reviewer src/auth.ts
Claude: [Loads and executes the security-reviewer skill]
```

**两种技能内容：**

- **参考内容** — Claude 应用到当前工作中的知识（约定、模式、风格指南）。在对话上下文中以内联方式运行。
- **任务内容** — 针对特定操作（部署、提交、代码生成）的分步说明。通常通过 `/skill-name` 手动调用。

### Skills 存储位置 [OFFICIAL]

技能的存储位置决定了谁可以使用它：

| 位置 | 路径 | 适用范围 |
|----------|------|------------|
| **企业级** | [托管设置](https://code.claude.com/docs/en/permissions#managed-settings) | 组织内所有用户 |
| **个人级** | `~/.claude/skills/<技能名称>/SKILL.md` | 你的所有项目 |
| **项目级** | `.claude/skills/<技能名称>/SKILL.md` | 仅限本项目 |
| **插件级** | `<插件>/skills/<技能名称>/SKILL.md` | 插件启用的地方 |


当多个技能名称相同时，优先级高的位置生效：**企业级 > 个人级 > 项目级**。插件技能使用 `插件名称:技能名称` 的命名空间，因此不会冲突。

**旧版兼容性：** `.claude/commands/` 目录中的文件仍然可用，并支持相同的前置元数据。如果技能与命令同名，技能优先。

**自动嵌套目录发现：** 当你在子目录中处理文件时，Claude Code 会从嵌套的 `.claude/skills/` 目录中发现技能。例如，编辑 `packages/frontend/` 中的文件也会加载 `packages/frontend/.claude/skills/` 中的技能。这支持了各包拥有自己技能的 monorepo 结构。

**实时变更检测：** 通过 `--add-dir` 添加的目录中的技能会自动加载，并会被实时变更检测捕获——你可以在会话期间编辑它们，无需重启。

### 技能目录结构 [OFFICIAL]

每个技能都是一个目录，以`SKILL.md`作为入口点：

```
my-skill/
├── SKILL.md           # Main instructions (required)
├── template.md        # Template for Claude to fill in (optional)
├── examples/
│   └── sample.md      # Example output (optional)
└── scripts/
    └── validate.sh    # Script Claude can execute (optional)
```

引用你的 `SKILL.md` 中的支持文件，以便 Claude 知道每个文件包含的内容。

```markdown
## Additional resources
- For complete API details, see [reference.md](reference.md)
- For usage examples, see [examples.md](examples.md)
```

> **提示:** 将 `SKILL.md` 保持在 500 行以内，将详细的参考材料移至单独的文件中。

### 创建技能 [OFFICIAL]

**第 1 步：** 创建技能目录：
```bash
# Personal skill (available in all projects)
mkdir -p ~/.claude/skills/explain-code

# Project skill (shared with team via git)
mkdir -p .claude/skills/explain-code
```

**第2步:** 编写带前置元数据和指令的 `SKILL.md` 文件：
```yaml
---
name: explain-code
description: Explains code with visual diagrams and analogies. Use when explaining how code works, teaching about a codebase, or when the user asks "how does this work?"
---

When explaining code, always include:

1. **Start with an analogy**: Compare the code to something from everyday life
2. **Draw a diagram**: Use ASCII art to show the flow, structure, or relationships
3. **Walk through the code**: Explain step-by-step what happens
4. **Highlight a gotcha**: What's a common mistake or misconception?

Keep explanations conversational. For complex concepts, use multiple analogies.
```

**第3步：**测试技能：
```bash
# Let Claude invoke it automatically
> "How does this code work?"

# Or invoke it directly
> /explain-code src/auth/login.ts
```

### 前置元数据参考 [OFFICIAL]

在 `SKILL.md` 顶部的 `---` 标记之间使用 YAML 前置元数据来配置技能的行为。所有字段均为可选；仅推荐填写 `description`。

| 字段 | 必需 | 描述 |
|------|------|------|
| `name` | 否 | 显示名称。如果省略，则使用目录名。小写字母、数字、连字符（最多 64 个字符）。 |
| `description` | 推荐 | 技能的用途及使用时机。Claude 据此判断何时加载该技能。 |
| `argument-hint` | 否 | 自动补全时显示的提示（例如 `[issue-number]` 或 `[filename] [format]`）。 |
| `disable-model-invocation` | 否 | `true` → 仅用户可通过 `/name` 调用。默认：`false`。 |
| `user-invocable` | 否 | `false` → 隐藏在 `/` 菜单中，仅 Claude 可调用。默认：`true`。 |
| `allowed-tools` | 否 | 技能激活时，Claude 无需请求许可即可使用的工具。 |
| `model` | 否 | 技能激活时使用的模型。 |
| `context` | 否 | 设置为 `fork` 可在分支子代理上下文中运行。 |
| `agent` | 否 | 当 `context: fork` 设置时，使用的子代理类型。 |
| `hooks` | 否 | 作用域限定于该技能生命周期的钩子。参见 [Hooks](https://code.claude.com/docs/en/hooks#hooks-in-skills-and-agents)。 |

### 控制调用方式 [OFFICIAL]

默认情况下，您和 Claude 都可以调用任意技能。以下两个 frontmatter 字段可对此进行限制：

- **`disable-model-invocation: true`** — 仅您可调用。适用于带有副作用的流程（例如 `/deploy`、`/commit`）。
- **`user-invocable: false`** — 仅 Claude 可调用。适用于作为背景知识但无法作为命令直接操作的内容。

```yaml
# User-only skill (Claude won't auto-trigger)
---
name: deploy
description: Deploy the application to production
disable-model-invocation: true
---

# Model-only skill (hidden from / menu)
---
name: legacy-system-context
description: Background knowledge about the legacy system
user-invocable: false
---
```

**调用与上下文加载行为：**

| 前置元数据 | 你可调用 | Claude 可调用 | 加载到上下文时 |
|-------------|----------------|-------------------|--------------------------|
| (默认) | 是 | 是 | 描述始终在上下文中；调用时加载完整技能 |
| `disable-model-invocation: true` | 是 | 否 | 描述不在上下文中；你调用时加载完整技能 |
| `user-invocable: false` | 否 | 是 | 描述始终在上下文中；调用时加载完整技能 |

**通过 `/permissions` 限制 Claude 的访问：**

```bash
# Allow only specific skills
Skill(commit)
Skill(review-pr *)

# Deny specific skills
Skill(deploy *)

# Disable all skills
Skill    # Add to deny rules
```

权限语法：`Skill(name)` 表示精确匹配，`Skill(name *)` 表示带有任意参数的前缀匹配。

### 传递参数 [OFFICIAL]

技能通过占位符替换接收参数：

| 变量 | 描述 |
|----------|-------------|
| `$ARGUMENTS` | 调用技能时传入的所有参数 |
| `$ARGUMENTS[N]` | 基于0的索引指定参数（例如 `$ARGUMENTS[0]`） |
| `$N` | `$ARGUMENTS[N]` 的简写（例如 `$0`、`$1`） |
| `${CLAUDE_SESSION_ID}` | 当前会话 ID（用于日志记录） |

**示例：**
```yaml
---
name: fix-issue
description: Fix a GitHub issue
disable-model-invocation: true
---

Fix GitHub issue $ARGUMENTS following our coding standards.

1. Read the issue description
2. Implement the fix
3. Write tests
4. Create a commit
```

```bash
/fix-issue 123
# Claude receives: "Fix GitHub issue 123 following our coding standards..."
```

**索引参数：**
```yaml
---
name: compare-files
description: Compare two files
---

# Compare: $ARGUMENTS[0] vs $ARGUMENTS[1]
# Shorthand: $0 vs $1

Compare $0 and $1 for differences.
```

```bash
/compare-files "src/v1/api.ts" "src/v2/api.ts"
# $0 = "src/v1/api.ts", $1 = "src/v2/api.ts"
```

如果 skill 内容中没有 `$ARGUMENTS`，则参数会以 `ARGUMENTS: <value>` 的形式附加。

### 高级模式 [OFFICIAL]

#### 动态上下文注入

`` !`command` `` 语法会在技能内容发送给 Claude 之前运行 shell 命令。输出将替换占位符：

```yaml
---
name: pr-summary
description: Summarize changes in a pull request
context: fork
agent: Explore
allowed-tools: Bash(gh *)
---

## Pull request context
- PR diff: !`gh pr diff`
- PR comments: !`gh pr view --comments`
- Changed files: !`gh pr diff --name-only`

## Your task
Summarize this pull request...
```

每个 `` !`command` `` 都会立即执行（在 Claude 看到任何内容之前）。Claude 只看到包含实际数据的最终结果。

#### 在子代理中运行

添加 `context: fork` 以独立运行 skill。skill 内容成为驱动 subagent 的 prompt（无法访问对话历史）：

```yaml
---
name: deep-research
description: Research a topic thoroughly
context: fork
agent: Explore
---

Research $ARGUMENTS thoroughly:

1. Find relevant files using Glob and Grep
2. Read and analyze the code
3. Summarize findings with specific file references
```

`agent` 字段指定要使用的子代理。选项：内置代理（`Explore`、`Plan`、`general-purpose`）或来自 `.claude/agents/` 的自定义子代理。默认值：`general-purpose`。

> **警告：** `context: fork` 仅针对具有明确指令的技能才有意义。没有任务的指南将返回无意义的输出。

#### 扩展思考

要在技能中启用扩展思考（extended thinking），只需在技能内容中的任意位置包含单词 `ultrathink`：

```yaml
---
name: architecture-review
description: Deep architectural analysis
---

Use ultrathink to analyze the architecture deeply.

Review the overall structure, identify patterns, and suggest improvements.
```

### 实用示例

**示例：Code Review Skill**

`.claude/skills/code-reviewer/SKILL.md`:
```yaml
---
name: code-reviewer
description: Reviews code for security vulnerabilities, bugs, performance issues, and style problems. Use when user asks to review, audit, or check code quality.
allowed-tools: [Read, Grep, Glob]
---

# Code Review Skill

## When to Activate
Use this skill when the user asks to:
- Review code for issues
- Audit security or find vulnerabilities
- Check code quality or best practices

## Review Process

### 1. Scope Detection
- Use Glob to identify files to review
- Prioritize recently modified files
- Focus on user-specified areas if mentioned

### 2. Analysis Layers
- **Security**: SQL injection, XSS, auth issues, exposed secrets
- **Bugs**: Logic errors, null checks, error handling
- **Performance**: N+1 queries, unnecessary loops, memory leaks
- **Style**: Naming conventions, code organization, readability

### 3. Reporting
Provide structured feedback organized by severity:
- **Critical/High**: Security issues
- **Medium**: Performance issues
- **Low**: Style and best practices

Each issue: file path, description, and fix suggestion.
```

**示例：Test Generator Skill**

`.claude/skills/test-generator/SKILL.md`:
```yaml
---
name: test-generator
description: Generates comprehensive unit and integration tests. Use when user asks to write tests, add test coverage, or create test cases.
allowed-tools: [Read, Write, Grep, Glob, Bash]
---

# Test Generator Skill

## When to Activate
Use this skill when user requests:
- "Write tests for..."
- "Add test coverage"
- "Generate test cases"

## Test Generation Process

### 1. Analyze Target Code
- Read the file/function to test
- Identify inputs, outputs, side effects
- Check existing test patterns

### 2. Generate Comprehensive Tests
Cover all scenarios:
- Happy path (expected usage)
- Error cases (invalid inputs)
- Edge cases (empty, null, boundary values)
- Side effects (database, API calls)

### 3. Follow Project Patterns
- Check CLAUDE.md for testing conventions
- Match existing test file structure
- Use project's test framework
```

**示例：安全审查技能**

`.claude/skills/security-review/SKILL.md`:
```yaml
---
name: security-review
description: Comprehensive security audit of codebase. Use when asked to review security, audit vulnerabilities, or check for exploits.
allowed-tools: [Read, Grep, Glob]
disable-model-invocation: true
---

# Security Review: $ARGUMENTS

Perform a thorough security audit focusing on: $ARGUMENTS

## Review Checklist

### 1. Authentication & Authorization
- Check for weak password policies
- Verify JWT token validation
- Review session management
- Check for broken access control

### 2. Input Validation
- SQL injection vulnerabilities
- XSS (Cross-Site Scripting) risks
- Command injection possibilities
- Path traversal vulnerabilities

### 3. Data Protection
- Sensitive data exposure
- Encryption at rest and in transit
- API keys and secrets in code
- Database credential security

### 4. Dependencies
- Known vulnerabilities in packages
- Outdated dependencies
- License compliance issues

### 5. Configuration
- Security headers (CSP, HSTS, etc.)
- CORS configuration
- Error messages leaking information
- Debug mode in production

**Output Format** - Provide a detailed report with sections:
- Critical Issues (Fix Immediately)
- High Priority
- Medium Priority
- Low Priority / Recommendations
- Security Strengths
- Action Plan (prioritized list of fixes)
```

**用法：**
```bash
/security-review "authentication and API endpoints"
```

**示例：API 文档生成器 Skill**

`.claude/skills/api-docs/SKILL.md`:
```yaml
---
name: api-docs
description: Generate comprehensive API documentation from code. Use when asked to document APIs, create API docs, or generate OpenAPI specs.
allowed-tools: [Read, Write, Grep, Glob]
disable-model-invocation: true
---

# Generate API Documentation

Analyze the codebase and create comprehensive API documentation for: $ARGUMENTS

## Process

### 1. Discovery
- Find all API routes/endpoints
- Identify request/response types
- Note authentication requirements
- Document query parameters

### 2. Documentation
For each endpoint, document:
- Method and path
- Description
- Authentication requirements
- Request body/parameters
- Response codes and bodies
- Example requests

### 3. Output
- Create `/docs/API.md` with full documentation
- Create `/openapi.yaml` with OpenAPI spec if applicable
```

**用法：**
```bash
/api-docs "all endpoints"
/api-docs "authentication routes"
```

### 使用 @ 语法的文件引用 [OFFICIAL]

使用 `@` 前缀引用文件以实现快速文件包含：

```bash
# Reference single file
/review-code @src/auth.ts

# Reference multiple files
/review-code @src/auth.ts @src/api.ts @tests/auth.test.ts

# Works in regular prompts too
> "Review @src/services/payment.ts for security issues"

# Reference files with skill arguments
/analyze-file @src/components/UserProfile.tsx
```

**@ 引用机制：**
- `@filename` 自动展开以包含文件内容
- 支持绝对路径和相对路径
- 可在一条命令中引用多个文件
- 文件会被自动读取并纳入上下文
- 减少明确说"先读取文件 X"的需要

**使用场景：**
```bash
# Code review with context
> "Compare @src/api/v1.ts and @src/api/v2.ts and list differences"

# Refactoring across files
> "Make @src/models/User.ts consistent with @src/types/user.d.ts"

# Bug investigation
> "This error occurs in @src/services/auth.ts, check @logs/error.log for clues"

# Test generation
> "Generate tests for @src/utils/validator.ts"
```

**最佳实践：**
- 在已知确切文件路径时使用 @ 引用
- 与 Skills 结合使用以实现可复用工作流
- 非常适用于对特定文件进行聚焦分析
- 与读取整个目录相比，减少 Token 使用量

### MCP 集成 [OFFICIAL]

MCP 服务器可以公开提示，这些提示会自动变为可调用的技能：

```json
{
  "prompts": [
    {
      "name": "search-docs",
      "description": "Search internal documentation",
      "arguments": [{"name": "query", "description": "Search query"}]
    }
  ]
}
```

在 Claude Code 中，这会以 `/search-docs` 的形式提供。

```bash
# Add MCP server
claude mcp add github -- gh-mcp

# MCP prompts become skills:
/github-pr-review      # Review current PR
/github-issues         # List open issues
/github-create-pr      # Create PR from current branch
```

### 技能最佳实践 [OFFICIAL]

#### 1. 编写清晰、具体的描述

`description` 字段至关重要——它帮助 Claude 决定何时激活：

**好：**
```yaml
description: "Generates API documentation from code comments. Use when user asks to document APIs, create API docs, update endpoint documentation, or generate OpenAPI specs."
```

**错误：**
```yaml
description: "Documentation generator"  # Too vague
```

#### 2. 使用自然触发词

包含用户自然会说的术语：

```yaml
# For security review skill
description: "Reviews code for security. Use when asked to: review security, audit code, find vulnerabilities, check for exploits, analyze risks."

# For performance optimization skill
description: "Optimizes code performance. Use when asked to: improve performance, optimize speed, reduce memory usage, make faster, profile code."
```

#### 3. 合理限制工具

```yaml
# Analysis only (can't modify code)
allowed-tools: [Read, Grep, Glob]

# Can create/modify code
allowed-tools: [Read, Write, Edit, Bash]

# Research and implementation
allowed-tools: [Read, Write, Edit, WebFetch, WebSearch]
```

#### 4. 保持技能专注

**好的（聚焦）：**
- `sql-optimizer` — 仅优化SQL查询
- `api-docs-generator` — 生成API文档
- `security-scanner` — 发现安全问题

**差的（过于宽泛）：**
- `database-everything` — 过于模糊
- `code-helper` — 哪种帮助？

#### 5. 提供清晰指令

将你的 SKILL.md 结构化：
1. **何时激活** —— 明确的触发条件
2. **流程** —— 逐步说明要做什么
3. **输出格式** —— 如何呈现结果
4. **示例** —— 展示预期的行为

#### 6. 注意上下文预算

技能描述会加载到上下文中，以便 Claude 知晓有哪些可用技能。如果你拥有大量技能，它们可能会超出字符预算（上下文窗口的 2%，回退为 16,000 个字符）。运行 `/context` 可检查是否存在被排除技能的警告。

可通过 `SLASH_COMMAND_TOOL_CHAR_BUDGET` 环境变量覆盖此限制。

### 技能故障排除 [OFFICIAL]

**技能未触发：**
1. 检查描述中是否包含用户自然会提到的关键词
2. 通过提问“有哪些可用技能？”来验证该技能是否出现
3. 尝试调整表述方式，使其与描述匹配
4. 直接使用 `/skill-name` 调用，确认其是否正常工作

**技能触发过于频繁：**
1. 让描述更加具体
2. 添加 `disable-model-invocation: true` 以仅限手动调用

**Claude 无法看到所有技能：**
- 过多的技能描述可能超出字符预算限制
- 运行 `/context` 检查是否有关于排除技能的警告
- 将 `SLASH_COMMAND_TOOL_CHAR_BUDGET` 设置为更高的值

### 迁移：从命令到技能

自定义斜杠命令（`.claude/commands/` 文件）已合并到技能系统中。**你现有的命令文件将继续保持正常工作，无需更改。** 推荐在新工作中使用技能，因为它们支持：

- **支持文件** — 将模板、脚本和参考文档与你的技能打包在一起
- **调用控制** — 选择是否由你、Claude，或双方均可调用
- **子代理执行** — 在隔离的分支上下文中运行技能
- **嵌套发现** — 从子目录自动加载（支持单体仓库）

**迁移路径：**
```bash
# Old structure (still works)
.claude/commands/review.md

# New structure (recommended)
.claude/skills/review/SKILL.md
```

两者都会创建 `/review`，且工作方式相同。如果两者同时存在，技能将优先。

**来源：** [Agent Skills](https://code.claude.com/docs/en/skills)

## 内置命令

**内置命令是用于管理 Claude Code 会话的原生 CLI 命令。** 它们被硬编码在 Claude Code 中，并非 Skills——你无法自定义或覆盖它们。

> **注意：** 如需自定义工作流命令，请改用 [Skills](#skills-系统)。像 `/help` 和 `/compact` 这样的内置命令无法通过 Skill 工具使用。

### 命令参考 [OFFICIAL]

```bash
# Session Management
/help              # Show all available commands
/exit              # End current session
/clear             # Clear conversation history
/compact [instr]   # Compact context (optionally specify what to focus on)
/rewind            # Undo code changes in conversation

# Session & History
/rename <name>     # Give current session a name
/resume [name|id]  # Resume a previous session by name or ID
/export            # Export conversation to file
/copy              # Copy last response to clipboard [NEW]

# Usage & Stats
/usage             # View plan limits and usage (NEW)
/stats             # Usage stats, engagement metrics (supports 7/30/all-time) (NEW)
/extra-usage       # Enable extra usage for Max plan subscribers [NEW]
/fast              # Toggle fast mode (uses faster model, available after /extra-usage) [NEW]

# Background Process Management
/bashes            # List all background processes
/tasks             # List all background tasks (agents, shells, etc.)
/kill <id>         # Stop a background process

# Discovery & Debugging
/bug               # Report bugs (sends conversation to Anthropic)
/commands          # List all skills and commands
/debug             # Troubleshoot session issues [NEW v2.1.30]
/hooks             # Show configured hooks
/skills            # List available Skills
/plugin            # Plugin management interface
/context           # View current context usage as a colored grid
/cost              # Show token usage statistics
/doctor            # Run diagnostics (shows Updates section with auto-update channel)

# Configuration
/config            # General settings (type to search and filter)
/permissions       # Manage tool permissions (with search)
/privacy-settings  # View and update privacy settings
/status            # Show session status (Status tab)
/statusline        # Configure status line display
/model             # Switch between models
/output-style      # Set output style directly or from selection menu
/theme             # Theme picker (Ctrl+T toggles syntax highlighting)
/terminal-setup    # Configure terminal (Kitty, Alacritty, Zed, Warp)
/vim               # Enter vim mode for alternating insert/command modes
/sandbox           # Enable sandboxed bash with filesystem/network isolation

# Workspace Management
/add-dir <path>    # Add additional directory to workspace
/agents            # Manage custom AI subagents
/init              # Initialize project with CLAUDE.md guide
/memory            # Edit CLAUDE.md memory files
/install-github-app # Set up Claude GitHub Actions for repository
/pr-comments       # View pull request comments
/review            # Request code review
/security-review   # Complete security review of pending changes
/todos             # List current TODO items

# MCP Server Management
/mcp               # MCP server management and OAuth authentication
/mcp enable <srv>  # Enable an MCP server
/mcp disable <srv> # Disable an MCP server

# Remote Sessions (claude.ai subscribers)
/teleport          # Resume remote session from claude.ai by session ID
/remote-env        # Configure remote session environment

# Account & Updates
/login             # Switch Anthropic accounts
/logout            # Sign out from Anthropic account
/release-notes     # View release notes

# Plan Mode
/plan              # Enter plan mode for structured planning
```

**来源:** [CLI 参考](https://code.claude.com/docs/en/cli-reference), [交互模式](https://code.claude.com/docs/en/interactive-mode#built-in-commands)

## Hooks 系统

**Hooks 是在 Claude Code 工作流的特定节点自动执行的脚本。**

### 什么是 Hooks？ [OFFICIAL]

Hooks 让您可以**拦截和控制** Claude 的操作：

```bash
# Examples of what hooks can do:
- Block editing of sensitive files (.env)
- Inject context at session start
- Run linting before file edits
- Validate git commits
- Audit all commands executed
- Add custom security checks
```

**两种类型：**
1. **Bash 命令 Hooks**（`type: "command"`）—— 运行 shell 脚本
2. **基于 Prompt 的 Hooks**（`type: "prompt"`）—— 使用 LLM 进行上下文感知决策

### Hook 配置 [OFFICIAL]

Hooks 在 `.claude/settings.json` 或 `~/.claude/settings.json` 中配置：

```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "ToolPattern",
        "hooks": [
          {"type": "command", "command": "script"}
        ]
      }
    ]
  }
}
```

### Hook 事件 [OFFICIAL]

| 事件 | 触发时机 | 是否可阻塞 |
|-------|---------------|-----------|
| **Setup** | 通过 `--init`、`--init-only` 或 `--maintenance` 标志 | 否 |
| **SessionStart** | 会话开始或恢复 | 否 |
| **SessionEnd** | 会话终止 | 否 |
| **UserPromptSubmit** | 用户提交提示 | 是 |
| **PreToolUse** | 工具执行前 | 是 |
| **PostToolUse** | 工具成功执行后 | 否 |
| **PostToolUseFailure** | 工具执行失败后 | 否 |
| **PermissionRequest** | 权限对话框出现时 | 是 |
| **SubagentStart** | 生成子代理时 | 否 |
| **SubagentStop** | 子代理完成时 | 是 |
| **Stop** | Claude 完成响应 | 是 |
| **Notification** | Claude 发送通知 | 否 |
| **PreCompact** | 上下文压缩前 | 否 |
| **TeammateIdle** | 智能体团队的队友即将空闲 [新增] | 是 |
| **TaskCompleted** | 任务被标记为完成 [新增] | 是 |

### 示例：保护敏感文件 [OFFICIAL]

`.claude/settings.json:`
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'FILE=$(echo \"$HOOK_INPUT\" | jq -r \".tool_input.file_path // empty\"); if [[ \"$FILE\" == *\".env\"* ]] || [[ \"$FILE\" == \".git/\"* ]]; then echo \"Cannot modify sensitive files\" >&2; exit 2; fi'"
          }
        ]
      }
    ]
  }
}
```

工作原理：
- 在任何编辑或写入工具之前运行
- 检查文件路径是否包含“.env”或“.git/”
- 以退出码 2 退出以阻止该操作
- Claude 收到错误并不编辑该文件

### 示例：会话上下文注入 [OFFICIAL]

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "cat .claude/session-context.txt"
          }
        ]
      }
    ]
  }
}
```

**创建:** `.claude/session-context.txt`
```
Today's Focus: Working on authentication refactor
Recent Context: Migrated from sessions to JWT
Current Branch: feature/jwt-auth
Important: Don't modify legacy auth code in /old-auth
```

此上下文会在每次会话启动时注入。

### 示例：智能决策 Hook [OFFICIAL]

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Evaluate if the current task is complete. Arguments: $ARGUMENTS. Check if all subtasks are done, tests pass, and documentation updated. Respond with {\"decision\": \"stop\" or \"continue\", \"reason\": \"explanation\"}"
          }
        ]
      }
    ]
  }
}
```

使用 LLM（Haiku）智能判断 Claude 是否应该停止工作。

### Hook 输入/输出 [OFFICIAL]

**输入（通过stdin作为JSON）：**
```json
{
  "sessionId": "abc123",
  "tool_name": "Edit",
  "tool_input": {
    "file_path": "/src/app.ts",
    "old_string": "...",
    "new_string": "..."
  },
  "project_dir": "/home/user/project"
}
```

**输出（退出码）：**
- `0` - 成功，继续
- `2` - 阻止操作
- 其他 - 非阻塞错误（已记录）

**JSON 输出（可选）：**
```json
{
  "decision": "stop",
  "reason": "All tasks complete",
  "continue": false
}
```

### 安全最佳实践 [OFFICIAL]

⚠️ **关键提醒：** “使用 hooks 时，您需自行对已配置的命令负责，这些命令可能修改或删除您的用户有权访问的文件。”

**最佳实践：**
```bash
# 1. Always quote variables
FILE="$HOOK_INPUT"  # Good
FILE=$HOOK_INPUT    # Bad - can break with spaces

# 2. Validate paths
if [[ "$FILE" == ../* ]]; then
  echo "Path traversal attempt" >&2
  exit 2
fi

# 3. Use absolute paths
cd "$CLAUDE_PROJECT_DIR" || exit 1

# 4. Sanitize inputs
jq -r '.tool_input.file_path' <<< "$HOOK_INPUT"  # Good
eval "$SOME_VAR"  # Bad - code injection risk

# 5. Block sensitive operations
case "$FILE" in
  *.env|.git/*|.ssh/*)
    echo "Blocked: sensitive file" >&2
    exit 2
    ;;
esac
```

### 调试 Hooks [OFFICIAL]

```bash
# Run Claude with debug mode
claude --debug

# Check hook configuration
> /hooks

# Test hook command manually
echo '{"tool_name":"Edit","tool_input":{"file_path":".env"}}' | bash your-hook-script.sh

# View logs
tail -f ~/.claude/logs/claude.log
```

### Hook 配方库 [OFFICIAL + COMMUNITY]

**适用于常见自动化需求的生产级钩子模式的全面集合。**

#### 1. 保存时自动格式化代码 [COMMUNITY]

自动在 Claude 编辑文件后使用语言对应的格式化工具进行代码格式化。

**配置（`.claude/settings.json`）：**
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|MultiEdit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "bash ~/.claude/hooks/format-code.sh"
          }
        ]
      }
    ]
  }
}
```

**脚本 (`~/.claude/hooks/format-code.sh`):**
```bash
#!/bin/bash
# Extract file path from JSON input
FILE=$(echo "$HOOK_INPUT" | jq -r '.tool_input.file_path // empty')

[[ -z "$FILE" ]] && exit 0

# Format based on extension
case "$FILE" in
  *.ts|*.tsx|*.js|*.jsx)
    # Try Biome first, fall back to Prettier
    if command -v biome &> /dev/null; then
      biome format --write "$FILE" &> /dev/null || true
    elif command -v prettier &> /dev/null; then
      prettier --write "$FILE" &> /dev/null || true
    fi
    ;;
  *.py)
    # Python: Ruff
    if command -v ruff &> /dev/null; then
      ruff format "$FILE" &> /dev/null || true
    fi
    ;;
  *.go)
    # Go: goimports + gofmt
    if command -v goimports &> /dev/null; then
      goimports -w "$FILE" &> /dev/null || true
    fi
    go fmt "$FILE" &> /dev/null || true
    ;;
  *.md)
    # Markdown: Prettier
    if command -v prettier &> /dev/null; then
      prettier --write "$FILE" &> /dev/null || true
    fi
    ;;
esac
```

**设为可执行：** `chmod +x ~/.claude/hooks/format-code.sh`

#### 2. 编辑时 ESLint 自动修复 [COMMUNITY]

自动对 JavaScript/TypeScript 文件运行 ESLint 并附带 `--fix` 参数。

**配置：**
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|MultiEdit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'FILE=$(echo \"$HOOK_INPUT\" | jq -r \".tool_input.file_path // empty\"); if [[ \"$FILE\" =~ \\.(ts|tsx|js|jsx)$ ]] && command -v eslint &>/dev/null; then eslint --fix \"$FILE\" &>/dev/null || true; fi'"
          }
        ]
      }
    ]
  }
}
```

---

#### 3. 阻止读取 .gitignore [COMMUNITY]

阻止 Claude 读取与 `.claudeignore` 模式匹配的文件。

**配置：**
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Read",
        "hooks": [
          {
            "type": "command",
            "command": "claude-ignore"
          }
        ]
      }
    ]
  }
}
```

**安装：** `npm install -g claude-ignore && claude-ignore init`

#### 4. 提交前运行测试 [COMMUNITY]

在允许 git 提交之前验证测试是否通过。

**配置：**
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "bash ~/.claude/hooks/pre-commit-test.sh"
          }
        ]
      }
    ]
  }
}
```

**脚本 (`~/.claude/hooks/pre-commit-test.sh`):**
```bash
#!/bin/bash
COMMAND=$(echo "$HOOK_INPUT" | jq -r '.tool_input.command // empty')

# Only intercept git commit commands
if [[ "$COMMAND" == git*commit* ]]; then
  echo "Running tests before commit..." >&2

  # Run tests
  if npm test &>/dev/null; then
    echo "✅ Tests passed" >&2
    exit 0
  else
    echo "❌ Tests failed - blocking commit" >&2
    exit 2
  fi
fi

exit 0
```

---

#### 5. 审计日志记录 Hook [COMMUNITY]

记录所有工具使用情况，用于安全审计。

**配置：**
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'echo \"$(date -Iseconds) $TOOL_NAME: $(echo \\\"$HOOK_INPUT\\\" | jq -c .)\" >> ~/.claude/audit.log'"
          }
        ]
      }
    ]
  }
}
```

---

#### 6. Token 用量追踪器 [COMMUNITY]

监控并记录每个会话的Token使用情况。

**配置：**
```json
{
  "hooks": {
    "SessionEnd": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash ~/.claude/hooks/log-session.sh"
          }
        ]
      }
    ]
  }
}
```

**脚本：**
```bash
#!/bin/bash
SESSION_ID=$(echo "$HOOK_INPUT" | jq -r '.session_id // "unknown"')
TRANSCRIPT=$(echo "$HOOK_INPUT" | jq -r '.transcript_path // empty')

if [[ -f "$TRANSCRIPT" ]]; then
  TOKENS=$(jq '[.[] | select(.role=="assistant") | .usage.total_tokens] | add' "$TRANSCRIPT" 2>/dev/null || echo 0)
  echo "$(date -Iseconds) Session $SESSION_ID: $TOKENS tokens" >> ~/.claude/token-usage.log
fi
```

---

#### 7. 提交消息验证 [COMMUNITY]

强制遵循常规提交消息格式。

**配置：**
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "bash ~/.claude/hooks/validate-commit.sh"
          }
        ]
      }
    ]
  }
}
```

**脚本：**
```bash
#!/bin/bash
COMMAND=$(echo "$HOOK_INPUT" | jq -r '.tool_input.command // empty')

if [[ "$COMMAND" == git*commit*-m* ]]; then
  MSG=$(echo "$COMMAND" | sed -n 's/.*-m[[:space:]]*["'"'"']\([^"'"'"']*\)["'"'"'].*/\1/p')

  # Check conventional commit format: type(scope): message
  if [[ ! "$MSG" =~ ^(feat|fix|docs|style|refactor|test|chore)(\(.+\))?: ]]; then
    echo "❌ Commit message must follow format: type(scope): message" >&2
    echo "Valid types: feat, fix, docs, style, refactor, test, chore" >&2
    exit 2
  fi
fi

exit 0
```

---

#### 8. 安全秘密扫描器 [COMMUNITY]

阻止提交包含潜在机密的文件。

**配置：**
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "bash ~/.claude/hooks/detect-secrets.sh"
          }
        ]
      }
    ]
  }
}
```

**脚本：**
```bash
#!/bin/bash
FILE=$(echo "$HOOK_INPUT" | jq -r '.tool_input.file_path // empty')
NEW_CONTENT=$(echo "$HOOK_INPUT" | jq -r '.tool_input.new_string // .tool_input.content // empty')

# Check for common secret patterns
if echo "$NEW_CONTENT" | grep -iE '(api[_-]?key|password|secret|token|auth)["\s:=]+\S{16,}' &>/dev/null; then
  echo "⚠️  Potential secret detected in $FILE" >&2
  echo "Please review and use environment variables instead" >&2
  exit 2
fi

exit 0
```

---

#### 9. 自动文档更新 [COMMUNITY]

当代码发生更改时更新README

**配置:**
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|MultiEdit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'echo \"📝 Consider updating documentation for recent changes\" >&2'"
          }
        ]
      }
    ]
  }
}
```

---

#### 10. 性能分析 [COMMUNITY]

跟踪工具操作的执行时间。

**配置：**
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'echo \"$HOOK_INPUT\" > /tmp/claude-pre-$$.json; date +%s%N > /tmp/claude-time-$$.txt'"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash ~/.claude/hooks/profile-tool.sh"
          }
        ]
      }
    ]
  }
}
```

**脚本：**
```bash
#!/bin/bash
START=$(cat /tmp/claude-time-$$.txt 2>/dev/null || echo 0)
END=$(date +%s%N)
DURATION=$(( (END - START) / 1000000 ))  # milliseconds
TOOL=$(echo "$HOOK_INPUT" | jq -r '.tool_name // "unknown"')

echo "$(date -Iseconds) $TOOL: ${DURATION}ms" >> ~/.claude/performance.log

rm -f /tmp/claude-pre-$$.json /tmp/claude-time-$$.txt
```

---

**来源:** [Hooks 参考](https://code.claude.com/docs/en/hooks), [Hooks 指南](https://code.claude.com/docs/en/hooks-guide), 社区 GitHub 仓库

---

## MCP 集成

**Model Context Protocol (MCP) 将 Claude Code 连接到外部数据源和工具。**

### 什么是 MCP？ [OFFICIAL]

MCP 允许 Claude Code 执行以下操作：
- 访问外部数据（Google Drive、Slack、Jira、Notion 等）
- 使用专业化工具（数据库、API、服务）
- 与企业系统集成
- 扩展超越本地文件系统的能力

**常见使用场景：**
- 读取/写入 Google Drive 文档
- 搜索 Slack 对话
- 直接查询数据库
- 从内部 API 获取数据
- 访问设计文件（Figma）
- 管理项目任务（Jira、Linear）

### MCP 服务器安装 [OFFICIAL]

MCP 服务器可以通过 CLI 或配置文件添加：

**CLI 安装（推荐）：**
```bash
# Remote HTTP Server (recommended for hosted services)
claude mcp add --transport http notion https://mcp.notion.com/mcp
claude mcp add --transport http github https://api.githubcopilot.com/mcp/

# With authentication headers
claude mcp add --transport http secure-api https://api.example.com/mcp \
  --header "Authorization: Bearer your-token"

# Local Stdio Server (for local packages)
claude mcp add --transport stdio airtable -- npx -y airtable-mcp-server
claude mcp add --transport stdio postgres -- npx -y @modelcontextprotocol/server-postgres "$DATABASE_URL"

# With environment variables
claude mcp add --transport stdio --env AIRTABLE_API_KEY=your_key airtable -- npx -y airtable-mcp-server

# Windows (requires cmd /c wrapper)
claude mcp add --transport stdio myserver -- cmd /c npx -y @some/package
```

**MCP 服务器管理：**
```bash
claude mcp list              # List all configured servers
claude mcp get github        # Get details for specific server
claude mcp remove github     # Remove a server
/mcp                         # Interactive management in Claude Code
```

**安装作用域：**
```bash
# Local scope (default) - stored in ~/.claude.json under project path
claude mcp add --transport http stripe https://mcp.stripe.com

# Project scope - stored in .mcp.json (shared via git)
claude mcp add --scope project --transport http paypal https://mcp.paypal.com/mcp

# User scope - stored in ~/.claude.json (available across all projects)
claude mcp add --scope user --transport http hubspot https://mcp.hubspot.com
```

**配置文件 (`.mcp.json`):**
```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/"
    },
    "postgres": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "${DATABASE_URL}"],
      "env": {
        "DB_URL": "${DB_URL}",
        "API_KEY": "${API_KEY:-default-value}"
      }
    },
    "slack": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-slack"],
      "env": {
        "SLACK_BOT_TOKEN": "${SLACK_BOT_TOKEN}",
        "SLACK_TEAM_ID": "${SLACK_TEAM_ID}"
      }
    }
  }
}
```

### OAuth 认证 [OFFICIAL]

许多MCP服务器支持OAuth进行安全认证：

```bash
# Add server that requires OAuth
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp

# Within Claude Code, authenticate via browser
/mcp
# Follow browser steps to complete OAuth login
```

**手动OAuth配置:**
```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/",
      "oauth": {
        "provider": "github",
        "scopes": ["repo", "read:user"]
      }
    }
  }
}
```

Claude Code 在首次使用时会打开浏览器以完成 OAuth 流程。

### 使用 MCP 工具 [OFFICIAL]

配置完成后，MCP 工具将以 `mcp__<server>__<tool>` 的模式出现：

```bash
# Example: Google Drive search
> "Search our Google Drive for Q4 planning documents"

# Claude uses: mcp__google-drive__search_files

# Example: Database query
> "Show all users created in the last week"

# Claude uses: mcp__postgres__query with SQL

# Example: Slack search
> "Find conversations about the API redesign"

# Claude uses: mcp__slack__search_messages
```

### Hook 中的 MCP [OFFICIAL]

你可以在 hooks 中引用 MCP 工具：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "mcp__postgres__query",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Database query requires review' && read -p 'Approve? (y/n) ' -n 1 -r && [[ $REPLY =~ ^[Yy]$ ]]"
          }
        ]
      }
    ]
  }
}
```

### 热门 MCP 服务端 [COMMUNITY]

```bash
# Official Servers
@modelcontextprotocol/server-google-drive      # Google Drive access
@modelcontextprotocol/server-slack             # Slack integration
@modelcontextprotocol/server-github            # GitHub API
@modelcontextprotocol/server-postgres          # PostgreSQL database
@modelcontextprotocol/server-sqlite            # SQLite database
@modelcontextprotocol/server-filesystem        # Extended file access

# Community Servers
# Check GitHub for community-built MCP servers
```

### MCP 配置管理 [OFFICIAL]

```bash
# Enable all project MCP servers automatically
{
  "enableAllProjectMcpServers": true
}

# Whitelist specific servers
{
  "enabledMcpjsonServers": ["google-drive", "postgres"]
}

# Blacklist servers
{
  "disabledMcpjsonServers": ["risky-server"]
}

# Enterprise: Restrict to managed servers only
{
  "useEnterpriseMcpConfigOnly": true,
  "allowedMcpServers": ["approved-server-1", "approved-server-2"]
}
```

### MCP 工具搜索 [NEW]

当 MCP 工具定义超过上下文窗口的阈值时，它们会通过 MCPSearch 工具自动推迟：

```bash
# Configure tool search threshold (% of context window)
ENABLE_TOOL_SEARCH=auto:5 claude    # Activate at 5%
ENABLE_TOOL_SEARCH=auto:10 claude   # Activate at 10% (default)
ENABLE_TOOL_SEARCH=true claude      # Always enabled
ENABLE_TOOL_SEARCH=false claude     # Always disabled

# Or configure in settings.json
{
  "permissions": {
    "deny": ["MCPSearch"]  # Disable MCP tool search
  }
}
```

**来源：** [MCP 文档](https://code.claude.com/docs/en/mcp), [设置](https://code.claude.com/docs/en/settings)

### MCP 设置示例 [OFFICIAL]

**热门 MCP 服务器的快速启动配置。**

#### GitHub 集成

```bash
# Installation
claude mcp add --transport stdio github -- npx -y @modelcontextprotocol/server-github

# Or via .mcp.json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

**常见操作：** 创建 Issue、管理 PR、搜索代码、审查仓库。

#### Slack 集成

```bash
# Installation
claude mcp add --transport stdio slack -- npx -y @modelcontextprotocol/server-slack

# Configuration
{
  "mcpServers": {
    "slack": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-slack"],
      "env": {
        "SLACK_BOT_TOKEN": "${SLACK_BOT_TOKEN}",
        "SLACK_TEAM_ID": "T01234567"
      }
    }
  }
}
```

**用法：** `> "Search Slack for conversations about API redesign"`

#### Google Drive 集成

```bash
# Installation with OAuth
claude mcp add --transport http gdrive https://mcp.google.com/drive

# Or stdio with credentials
{
  "mcpServers": {
    "gdrive": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-gdrive"],
      "env": {
        "GDRIVE_CREDENTIALS_PATH": "${HOME}/.gdrive-credentials.json"
      }
    }
  }
}
```

**身份验证：** 在 Claude Code 中运行 `/mcp`，然后遵循 OAuth 流程。

#### PostgreSQL 数据库

```bash
# Installation
claude mcp add --transport stdio postgres -- npx -y @modelcontextprotocol/server-postgres postgresql://user:pass@localhost/db

# Configuration
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-postgres",
        "${DATABASE_URL}"
      ]
    }
  }
}
```

**用法：** `> "Show all users created in the last week from the database"`

#### Notion 集成

```bash
# Installation
claude mcp add --transport http notion https://mcp.notion.com/mcp

# Requires Notion OAuth - authenticate via /mcp command
```

**常见操作:** 查询数据库、创建页面、搜索工作区。

#### Stripe 支付集成

```bash
# Configuration
{
  "mcpServers": {
    "stripe": {
      "command": "npx",
      "args": ["-y", "@stripe/mcp-server"],
      "env": {
        "STRIPE_API_KEY": "${STRIPE_API_KEY}"
      }
    }
  }
}
```

**用法：** `> "List recent Stripe transactions and summarize revenue"`

### MCP 故障排除 [COMMUNITY]

**来自 GitHub Issue 及生产环境的常见问题与解决方案**

#### 问题：MCP 服务端未在列表中显示

```bash
# Problem
claude mcp list
# Output: "No MCP servers configured"

# Solutions
1. Check file location:
   - User scope: ~/.claude/settings.json
   - Project scope: .mcp.json (in project root)

2. Verify JSON syntax:
   cat .mcp.json | jq .

3. Check scope setting:
   claude mcp add --scope project <name> ...

4. Restart Claude Code after config changes
```

#### 问题：尽管显示“已连接”，但工具不可用

```bash
# Problem
/mcp shows "✓ Connected" but tools don't appear

# Solutions
1. Check tool output size (max 25,000 tokens):
   export MAX_MCP_OUTPUT_TOKENS=50000

2. Verify server actually started:
   ps aux | grep mcp

3. Check debug logs:
   claude --debug
   tail -f ~/.claude/logs/claude.log

4. Reset project approvals:
   claude mcp reset-project-choices
```

#### 问题：OAuth 认证失败

```bash
# Problem
Browser opens but OAuth fails or doesn't complete

# Solutions
1. Use /mcp command (not direct URL)

2. Check network/proxy settings:
   # Try without VPN/Cloudflare Warp

3. Clear OAuth cache:
   rm -rf ~/.claude/oauth-cache

4. Verify redirect URI in provider settings
```

#### 问题：Windows 出现“连接已关闭”错误

```bash
# Problem
MCP server immediately closes on Windows

# Solution - Use cmd /c wrapper:
claude mcp add --transport stdio myserver -- cmd /c npx -y package-name

# In .mcp.json:
{
  "mcpServers": {
    "myserver": {
      "command": "cmd",
      "args": ["/c", "npx", "-y", "package-name"]
    }
  }
}
```

#### 问题：环境变量未展开

```bash
# Problem
${VAR} shows literally instead of expanding

# Solutions
1. Check .env file exists and is loaded

2. Use default syntax:
   "${API_KEY:-default_value}"

3. Set in shell before running:
   export API_KEY=xxx && claude

4. Use settings.local.json for sensitive values
```

#### 问题：MCP 服务端进程崩溃

```bash
# Debug steps:
1. Test server directly:
   npx @modelcontextprotocol/server-github

2. Check stdout/stderr:
   claude --debug | grep mcp

3. Verify dependencies installed:
   npm list -g | grep mcp

4. Check memory/resource limits:
   ulimit -a
```

---

## 子代理

**Sub-agents 是为特定任务配置的专业化AI助手。**

### 什么是子代理？[OFFICIAL]

Sub-agents 是针对特定工作流优化的 Claude 实例：

```bash
# Built-in Sub-Agents
- general-purpose: Complex multi-step tasks
- Explore: Fast codebase exploration

# Custom Sub-Agents
- You can create your own with custom prompts and tools
```

### 使用子代理 [OFFICIAL]

使用 `Task` 工具启动：

```bash
# Explore codebase
> "Find all database queries in the codebase"

# Claude uses:
Task subagent_type="Explore"
     prompt="Find all database queries and list files containing SQL, Prisma, or ORM code"

# General purpose research
> "Research best practices for API rate limiting and suggest implementation"

# Claude uses:
Task subagent_type="general-purpose"
     prompt="Research API rate limiting approaches, compare options, and recommend implementation for Express.js"
```

### 创建自定义子代理 [OFFICIAL]

Sub-agents 被定义为位于 `.claude/agents/` 或 `~/.claude/agents/` 目录下的 Markdown 文件：

**示例：调试助手**

`.claude/agents/debugger.md`:
```markdown
---
name: debugger
description: Specialized debugging agent for production issues
model: claude-sonnet-4
allowedTools: [Read, Grep, Glob, Bash]
---

# Debug Assistant

You are a specialized debugging agent. Your role is to systematically investigate and identify the root cause of issues.

## Debugging Process

### 1. Gather Context
- Read error messages and stack traces
- Check recent code changes (git log)
- Review related log files
- Understand expected vs actual behavior

### 2. Hypothesis Generation
- List possible causes
- Prioritize by likelihood
- Consider recent changes first

### 3. Systematic Investigation
- Test each hypothesis methodically
- Use Grep to find related code
- Read implementation details
- Check for similar patterns elsewhere

### 4. Root Cause Analysis
- Identify the precise cause
- Explain why it happens
- Trace the execution path

### 5. Solution Proposal
- Suggest specific fixes
- Explain tradeoffs
- Provide code examples
- Recommend tests to prevent recurrence

## Constraints
- DO NOT modify code (read-only analysis)
- DO provide detailed explanations
- DO reference specific file:line locations
- DO consider edge cases
```

**示例：代码审查代理**

`.claude/agents/reviewer.md`:
```markdown
---
name: reviewer
description: Code review specialist focusing on quality and best practices
model: claude-sonnet-4
allowedTools: [Read, Grep, Glob]
---

# Code Reviewer

You are a senior code reviewer. Provide constructive, actionable feedback.

## Review Criteria

### Code Quality
- Readability and maintainability
- Naming conventions
- Code organization
- DRY principle adherence

### Correctness
- Logic errors
- Edge cases handling
- Error handling
- Null/undefined checks

### Performance
- Algorithm efficiency
- Unnecessary computations
- Memory usage
- Database query optimization

### Security
- Input validation
- SQL injection risks
- XSS vulnerabilities
- Authentication/authorization

### Testing
- Test coverage
- Test quality
- Edge cases tested

## Output Format
Provide structured feedback:
- **Strengths**: What's done well
- **Issues**: Problems found (with severity)
- **Suggestions**: Improvements
- **Examples**: Code snippets for fixes
```

### 子代理功能 [OFFICIAL]

#### 模型选择

为每个智能体选择不同的模型

```markdown
---
name: fast-explorer
model: claude-haiku-4  # Fast, cost-effective
---
```

```markdown
---
name: deep-analyzer
model: claude-opus-4  # Most capable
---
```

#### 工具限制

限制工具以实现专注操作：

```markdown
---
name: readonly-analyzer
allowedTools: [Read, Grep, Glob]  # Analysis only
---
```

```markdown
---
name: implementation-agent
allowedTools: [Read, Write, Edit, Bash]  # Can modify code
---
```

### 子代理模式 [COMMUNITY]

#### 并行分析

```bash
> "Have multiple agents analyze different aspects"

# Launches multiple agents in parallel:
- Security review agent
- Performance analysis agent
- Code style agent
- Test coverage agent

# Aggregates results
```

#### 顺序流水线

```bash
> "Research → Design → Implement authentication"

# Sequential sub-agents:
1. Research agent: Find best practices
2. Design agent: Create architecture
3. Implementation agent: Write code
4. Review agent: Verify implementation
```

#### 专业化团队

```json
{
  "frontend-agent": "React/UI specialist",
  "backend-agent": "API/database specialist",
  "devops-agent": "Deployment/infrastructure specialist"
}
```

**来源：** [子代理](https://code.claude.com/docs/en/sub-agents)

## 智能体团队

**智能体团队使多个 Claude Code 实例能够在共享上下文和直接通信的基础上协作处理复杂任务。**

### 什么是智能体团队？[OFFICIAL]

Agent Teams（实验性）允许你协调多个同时工作的 Claude Code 会话：

```bash
# Key differences from Sub-Agents:
- Sub-Agents: Run within a single session, report only to main agent
- Agent Teams: Independent sessions that can communicate directly with each other

# When to use Agent Teams:
✅ Research and review (multiple perspectives simultaneously)
✅ New modules/features (teammates own separate pieces)
✅ Debugging with competing hypotheses (parallel investigation)
✅ Cross-layer coordination (frontend, backend, tests)

# When NOT to use Agent Teams:
❌ Sequential tasks with dependencies
❌ Same-file edits (coordination overhead)
❌ Simple tasks (overkill)
```

### 启用智能体团队 [OFFICIAL]

Agent Teams 默认处于禁用状态。请在设置中启用：

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

或者设置环境变量:

```bash
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
claude
```

### 启动团队 [OFFICIAL]

```bash
# Describe the task and team structure
> "Create an agent team to review PR #142. Spawn three reviewers:
   - One focused on security implications
   - One checking performance impact
   - One validating test coverage
   Have them each review and report findings."

# Claude creates the team and coordinates work
# Use Shift+Up/Down to select and message teammates directly
```

### 团队显示模式 [OFFICIAL]

| 模式 | 描述 | 最佳适用场景 |
|------|------|--------------|
| `in-process` | 所有队友在主终端中 | 任意终端，简单设置 |
| `tmux` | 每个队友在单独的窗格中 | 并行可见性，tmux/iTerm2 |
| `auto`（默认） | 如果已在 tmux 会话中则自动使用 tmux | 自动选择 |

在设置中进行配置：

```json
{
  "teammateMode": "in-process"
}
```

或者通过CLI标志：

```bash
claude --teammate-mode in-process
```

### 团队控制 [OFFICIAL]

```bash
# Select teammates
Shift+Up/Down          # Cycle through teammates

# View teammate session
Enter                  # View selected teammate's session
Escape                 # Interrupt teammate's turn

# Manage tasks
Ctrl+T                 # Toggle shared task list

# Delegate mode
Shift+Tab              # Toggle delegate mode (lead only coordinates, doesn't implement)

# Shut down
> "Ask the researcher teammate to shut down"
> "Clean up the team"
```

### 团队架构 [OFFICIAL]

| 组件 | 描述 |
|-----------|-------------|
| **Team Lead** | 主会话，负责创建团队、生成队友、协调工作 |
| **Teammates** | 独立的 Claude Code 实例，处理分配的任务 |
| **Task List** | 共享的工作项，队友可认领并完成 |
| **Mailbox** | 智能体间通信的消息系统 |

**存储位置：**
- 团队配置：`~/.claude/teams/{team-name}/config.json`
- 任务列表：`~/.claude/tasks/{team-name}/`

### 团队 Hooks [OFFICIAL]

使用 Hooks 强制实施质量门禁：

```json
{
  "hooks": {
    "TeammateIdle": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'if [ ! -f ./dist/output.js ]; then echo \"Build artifact missing\" >&2; exit 2; fi'"
          }
        ]
      }
    ],
    "TaskCompleted": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'if ! npm test 2>&1; then echo \"Tests failing\" >&2; exit 2; fi'"
          }
        ]
      }
    ]
  }
}
```

- **TeammateIdle**: 在队友即将进入空闲状态时运行。退出码 2 会发送反馈并保持队友继续工作。
- **TaskCompleted**: 在任务标记为完成时运行。退出码 2 会阻止完成并附带反馈。

### 当前限制 [OFFICIAL]

- 进程内团队成员无法恢复会话
- 任务状态可能滞后（卡住的任务需要手动干预）
- 关闭缓慢（团队成员先完成当前工作）
- 每会话仅允许一个团队
- 不支持嵌套团队（团队成员无法创建子团队）
- 领导固定（无法晋升团队成员）
- 权限在生成时设置（无法为每个团队成员预设）
- 分屏需借助 tmux 或 iTerm2

**来源：** [Agent Teams](https://code.claude.com/docs/en/agent-teams)

## 插件

**插件将 Skills、Hooks 和 MCP 服务器打包在一起，便于共享。**

### 什么是插件？[OFFICIAL]

插件是扩展 Claude Code 的包：

```bash
# A plugin can contain:
- Skills (capabilities and workflow templates)
- Hooks (automation)
- MCP Servers (external integrations)
- Sub-Agent definitions
```

### 插件管理 [OFFICIAL]

```bash
# Interactive plugin management
> /plugin

# Options:
- Browse marketplace
- Install plugins
- Enable/disable plugins
- Remove plugins
- Add custom marketplaces
- Search installed plugins [v2.1.14]
```

**插件固定** [NEW v2.1.14]：插件现在可以固定到特定的 Git 提交 SHA 以实现版本稳定性：

```json
{
  "plugins": {
    "enabledPlugins": {
      "security-toolkit@official#abc123def": true
    }
  }
}
```

### 插件结构 [OFFICIAL]

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json          # Metadata
├── commands/                 # Legacy commands (treated as skills)
│   └── my-command.md
├── skills/                   # Skills
│   └── my-skill/
│       └── SKILL.md
├── hooks.json               # Hook definitions
└── agents/                  # MCP servers & sub-agents
    └── mcp.json
```

**plugin.json:**
```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "My awesome plugin",
  "author": "Your Name",
  "homepage": "https://github.com/user/plugin",
  "keywords": ["productivity", "testing"]
}
```

### 安装插件 [OFFICIAL]

```bash
# From marketplace
> /plugin
# Select "Browse marketplace"
# Choose and install

# Team Configuration
# .claude/settings.json
{
  "plugins": {
    "enabledPlugins": {
      "security-toolkit@official": true,
      "custom-workflows@team": true
    }
  }
}
```

### 创建自定义市场 [OFFICIAL]

```json
{
  "extraKnownMarketplaces": [
    {
      "name": "company-internal",
      "type": "github",
      "url": "https://github.com/company/claude-plugins"
    },
    {
      "name": "local-dev",
      "type": "directory",
      "path": "/path/to/plugins"
    }
  ]
}
```

### 团队插件的自动安装 [OFFICIAL]

在 `.claude/settings.json` 中配置（已提交到 git）：

```json
{
  "plugins": {
    "enabledPlugins": {
      "team-workflows@company": true
    }
  },
  "extraKnownMarketplaces": [
    {
      "name": "company",
      "type": "github",
      "url": "https://github.com/company/claude-plugins"
    }
  ]
}
```

当团队成员信任仓库时，插件会自动安装。

### VSCode 插件功能 [NEW]

在 VSCode 中使用 Claude Code 时：
- **安装计数显示**：查看每个插件有多少用户安装
- **信任警告**：从不受信任来源安装插件时的安全提示
- **原生插件管理**[v2.1.16]：VSCode 扩展内置的插件管理支持
- **远程会话浏览**[v2.1.16]：OAuth 用户可以直接从会话对话框浏览和恢复远程 Claude 会话
- **`/usage` 命令**[v2.1.14]：直接在 VSCode 中显示当前套餐使用量
- **会话分叉与回退**[v2.1.19]：现已为所有用户启用会话分叉和回退功能
- **Python 虚拟环境激活**[v2.1.21]：自动激活确保 `python` 和 `pip` 使用正确的解释器（通过 `claudeCode.usePythonEnvironment` 设置进行配置）
- **Claude 集成 Chrome**[v2.1.27]：将 Claude Code 连接到 Chrome 浏览器，实现 Web 自动化与测试

**来源：**[Plugins](https://code.claude.com/docs/en/plugins)

### 桌面应用功能 [NEW]

Claude 桌面应用为在本地运行 Claude Code 会话以及和网页版 Claude Code 集成提供了原生界面。

**主要特性：**
- **差异视图**：在创建 PR 之前，逐文件审查 Claude 的更改，并支持行内评论
- **使用 Git 工作树的并行本地会话**：在同一仓库中运行多个会话，每个会话拥有独立的工作树
- **`.worktreeinclude` 文件**：自动将被 git 忽略的文件（如 `.env`）复制到新的工作树中
- **启动云端会话**：直接从桌面应用在网页上启动 Claude Code
- **捆绑的 Claude Code 版本**：包含稳定、有管理的 Claude Code 版本

**差异视图：**
- 点击差异统计指示器（`+12 -1`）打开差异查看器
- 点击任意行添加行内评论
- 按 Enter 确认每条评论，按 Cmd+Enter 发送全部

**Git 工作树：**
在仓库根目录中创建 `.worktreeinclude` 文件：
```
.env
.env.local
**/.claude/settings.local.json
```

匹配这些模式且同时位于 `.gitignore` 中的文件将被复制到新的 worktrees。

**安装：**
- macOS：https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect
- Windows x64：https://claude.ai/api/desktop/win32/x64/exe/latest/redirect
- Windows ARM64：https://claude.ai/api/desktop/win32/arm64/exe/latest/redirect

**来源：** [桌面文档](https://code.claude.com/docs/en/desktop)

---

## 开发工作流

### 核心开发方法 [COMMUNITY]

**第 1 阶段：理解**
```bash
# Start by understanding the codebase
> "Read the project structure and explain the architecture"
> "What testing framework is used?"
> "Show me the authentication flow"

# Claude will:
- Read README, package.json, etc.
- Analyze project structure
- Identify key patterns
```

**第 2 阶段：计划**
```bash
# For complex features, plan first
> "I need to add user roles and permissions. Create a plan"

# Claude will:
- Break down the feature
- Identify affected files
- Consider edge cases
- Create TodoWrite tasks
```

**第 3 阶段：实现**
```bash
# Implement incrementally
> "Implement step 1: Add roles to user model"

# Then verify
> "Run the tests"

# Continue
> "Implement step 2: Add permission checks to API"
```

**第 4 阶段：验证**
```bash
# Always verify changes
> "Run all tests"
> "Check for TypeScript errors"
> "Review the changes we made"

# Create commit
> "Create a git commit for these changes"
```

### 使用 TodoWrite 进行任务管理 [COMMUNITY]

对于复杂的多步骤工作：

```bash
> "Add user authentication system"

# Claude creates todos:
TodoWrite todos=[
  {"content": "Create User model with password hashing", "status": "in_progress", ...},
  {"content": "Implement JWT token generation", "status": "pending", ...},
  {"content": "Add login/register endpoints", "status": "pending", ...},
  {"content": "Add authentication middleware", "status": "pending", ...},
  {"content": "Write integration tests", "status": "pending", ...}
]

# As work progresses, todos update:
# ✅ "Create User model..." - completed
# ⏳ "Implement JWT tokens..." - in_progress
# ⏸️ "Add login/register..." - pending
```

### 并行与串行工作 [COMMUNITY]

**并行（独立任务）：**
```bash
> "Create these three independent components"

# Claude can work on all simultaneously:
- Component A (no dependencies)
- Component B (no dependencies)
- Component C (no dependencies)
```

**顺序（依赖）：**
```bash
> "Set up database, then add user model, then create API"

# Must be done in order:
1. Database setup (others depend on this)
2. User model (API depends on this)
3. API endpoints (depends on model)
```

### 质量保证模式 [COMMUNITY]

**自动化验证：**
```bash
# After changes, verify automatically
> "Run the following checks:
   - TypeScript compilation
   - Linting
   - All tests
   - Build process"

# Or create a skill:
/verify-changes
```

**多视角审查：**
```bash
# Use sub-agents for thorough review
> "Review these changes from multiple perspectives:
   - Security issues
   - Performance implications
   - Code quality
   - Test coverage"

# Launches specialized review agents
```

---

## 工具协同

Claude Code 的功能构成一个分层自动化栈。理解它们如何组合，就能解锁强大的工作流。

### 快速参考：15 种协同模式

| # | 协同模式 | 使用场景 |
|---|---------|----------|
| 1 | [探索 → 规划 → 编码 → 提交](#协同模式-1探索--计划--编码--提交-official) | 标准开发工作流 |
| 2 | [测试驱动开发](#协同模式-2测试驱动开发-community) | 质量优先编码 |
| 3 | [MCP + Skills](#协同模式-3mcp--skills-official) | 外部工具集成 |
| 4 | [Skills + Hooks](#协同模式-4skills--hooks自动应用--强制执行-official) | 自动应用专业知识 + 强制执行规则 |
| 5 | [子代理 + 后台任务](#协同模式-5子代理--后台任务-official) | 并行隔离工作 |
| 6 | [多 Claude 工作流](#协同模式-6多-claude-工作流-community) | 使用 Git worktree 实现并行 |
| 7 | [上下文保持](#协同模式-7会话间上下文保留-community) | 会话连续性 |
| 8 | [质量流水线](#协同模式-8质量流水线hooks--测试--lint-community) | 自动化质量保障 |
| 9 | [视觉驱动开发](#协同模式-9视觉驱动开发-community) | 截图/设计稿 → 代码 |
| 10 | [日志分析流水线](#协同模式-10日志分析流水线-official) | Unix 流水线 + Claude |
| 11 | [模式驱动开发](#协同模式-11模式驱动开发-community) | 数据库模式 → 类型/API/测试 |
| 12 | [依赖管理](#协同模式-12依赖管理-community) | 更新 + 测试 + 修复循环 |
| 13 | [文档生成](#协同模式-13文档生成-community) | 代码库 → 活文档 |
| 14 | [安全重构](#协同模式-14带安全网的重构-community) | 大型改动且不破坏现有功能 |
| 15 | [事件响应](#协同模式-15事件响应-community) | 生产环境调试工作流 |

### 功能堆栈 [OFFICIAL]

每一层功能都服务于特定目的，并彼此叠加构建：

| 层级 | 功能 | 用途 | 调用方式 |
|-------|---------|---------|------------|
| **连接层** | MCP | 外部工具（如 GitHub、Jira、数据库） | 配置后自动触发 |
| **能力层** | Skills | 领域专业知识 + 工作流 | 自动激活或通过 `/skill-name` 调用 |
| **执行层** | Hooks | 质量门禁、自动操作 | 生命周期事件触发 |
| **隔离层** | Sub-agents | 并行处理专业任务 | 任务委托 |
| **打包层** | Plugins | 打包上述所有功能 | 一次安装即用 |

**关键洞察：** MCP 连接外部系统。Skills 提供专业知识与工作流（既可自动激活也可由用户调用）。Hooks 强制执行标准。Sub-agents 隔离繁重任务。

### 协同模式 1：探索 → 计划 → 编码 → 提交 [OFFICIAL]

来自 [Anthropic 的最佳实践](https://www.anthropic.com/engineering/claude-code-best-practices) 的推荐工作流：

```bash
# Step 1: Explore - understand what exists
"Read src/auth/ and explain the current authentication flow.
List all files involved and their responsibilities."

# Step 2: Plan - use extended thinking
"Think hard about how to add OAuth2 support. Create a detailed plan
covering: files to modify, new files needed, dependencies, and test strategy."

# Step 3: Code - implement with explicit files
"Implement the OAuth2 changes following the plan. Start with
src/auth/oauth.ts, then update src/auth/index.ts to export it."

# Step 4: Commit - structured message
"Create a commit with message: 'feat(auth): add OAuth2 provider support'"
```

**为何有效：** 每一步都逐步建立上下文。先探索可防止错误假设。通过“深入思考”进行规划可启用扩展推理。明确文件名可减少歧义。

### 协同模式 2：测试驱动开发 [COMMUNITY]

先写测试，再实现：

```bash
# 1. Write failing tests first
"Write tests for a new validateEmail function in src/utils/validation.ts.
Cover: valid emails, invalid formats, empty input, null input.
Use Jest. The function doesn't exist yet - tests should fail."

# 2. Confirm tests fail
"Run npm test -- --testPathPattern=validation"

# 3. Commit the failing tests
"Commit with message: 'test(validation): add email validation tests (red)'"

# 4. Implement to pass
"Now implement validateEmail in src/utils/validation.ts to pass all tests.
Use a standard regex pattern. No external dependencies."

# 5. Verify and commit
"Run the tests again. If passing, commit: 'feat(validation): implement email validation (green)'"
```

**原因：** 测试在实现之前定义了契约。Claude 针对具体目标进行迭代。Git 历史显示了 TDD 纪律。

### 协同模式 3：MCP + Skills [OFFICIAL]

MCP servers 暴露 prompts，这些 prompts 成为 skills：

```bash
# Add MCP server
claude mcp add github -- gh-mcp

# Now available as commands:
/github-pr-review      # Review current PR
/github-issues         # List open issues
/github-create-pr      # Create PR from current branch

# Example workflow - complete ticket
/github-issues         # "Show me issue #42"
# Claude fetches issue details via MCP

"Implement the feature described in issue #42.
Follow our patterns in src/features/."

/github-create-pr      # Creates PR linked to issue
```

**真实的 MCP 集成：** GitHub, Jira, Linear, Notion, PostgreSQL, Slack, Figma, Google Drive。每个集成都添加了领域特定的命令。

### 协同模式 4：Skills + Hooks（自动应用 + 强制执行） [OFFICIAL]

Skills自动激活；hooks在生命周期事件时强制执行。

```
.claude/
├── skills/
│   └── security-review/
│       └── SKILL.md        # Auto-activates on security-related tasks
└── settings.json           # Hook: block commits if security issues found
```

**技能定义** (`.claude/skills/security-review/SKILL.md`):
```markdown
---
name: security-review
description: Analyzes code for security vulnerabilities. Activates when
reviewing auth code, API endpoints, or user input handling.
allowed-tools: [Read, Grep, Glob]
---

When activated, check for:
- SQL injection (string concatenation in queries)
- XSS (unescaped user input in HTML)
- Exposed secrets (API keys, passwords in code)
- Broken auth (missing token validation)

Report findings with file:line references and severity.
```

**Hook definition**（位于 `settings.json`）：
```json
{
  "hooks": {
    "PreToolUse": [{
      "tool": "Bash",
      "command": "git commit",
      "script": ".claude/hooks/security-check.sh"
    }]
  }
}
```

**工作流:**
```bash
"Review the authentication code in src/auth/ for security issues"
# Skill auto-activates, finds issues

"Fix the SQL injection vulnerability in src/auth/login.ts:45"
# You fix it

"Commit the security fix"
# Hook runs security-check.sh before allowing commit
# Blocks if issues remain, allows if clean
```

### 协同模式 5：子代理 + 后台任务 [OFFICIAL]

隔离工作并并行运行：

```bash
# Start services in background (Ctrl+B or explicit)
"Run npm run dev in background"
"Run npm test -- --watch in background"

# Check running tasks
/tasks

# Main session: Use explorer agent for research
"Use the explorer agent to find all API endpoints and their handlers"

# Parallel work happening:
# - Background: Dev server on port 3000
# - Background: Test watcher re-running on changes
# - Sub-agent: Scanning codebase for endpoints
# - Main session: Available for next task

# Later, retrieve agent results
"What did the explorer agent find?"
```

**子代理类型：** `Explore`（代码库搜索），`Plan`（架构），定义于`.claude/agents/`中的自定义代理。

### 协同模式 6：多 Claude 工作流 [COMMUNITY]

运行多个 Claude 实例以进行独立工作：

```bash
# Terminal 1: Feature development
cd feature-branch-worktree
claude
"Implement the user dashboard feature"

# Terminal 2: Code review (same repo, different worktree)
cd review-worktree
claude
"Review the changes in the user-dashboard branch for security and performance"

# Terminal 3: Documentation
cd docs-worktree
claude
"Update API documentation based on recent changes"
```

**高级：Claude 审查 Claude：**
```bash
# Claude 1 writes code
"Implement rate limiting for the API endpoints in src/api/"

# Claude 2 reviews (different session)
"Review the rate limiting implementation. Check for:
- Edge cases (what happens at exactly the limit?)
- Race conditions (concurrent requests)
- Configuration flexibility (can limits be changed without deploy?)"
```

### 协同模式 7：会话间上下文保留 [COMMUNITY]

结合 CLAUDE.md + Skills 实现连续性：

**项目 CLAUDE.md：**
```markdown
# Project: E-commerce API

## Current Sprint
- [ ] Implement payment webhooks
- [ ] Add inventory tracking
- [x] User authentication (completed Jan 10)

## Key Decisions
- Using Stripe for payments (see docs/adr/001-payment-provider.md)
- PostgreSQL for inventory (see src/db/schema.sql)

## Commands
npm run dev      # Start on port 3000
npm test         # Run Jest tests
npm run db:seed  # Seed test data
```

**用于上下文加载的 Skill** (`.claude/skills/resume/SKILL.md`):
```markdown
---
name: resume
description: Resume work on current sprint
---

Read CLAUDE.md and the current sprint tasks.
Check git log for recent commits.
Summarize: what's done, what's in progress, what's next.
Ask what I want to work on.
```

**用法：**
```bash
claude
/resume
# Claude reads context, summarizes state, ready to continue
```

### 协同模式 8：质量流水线（Hooks + 测试 + Lint） [COMMUNITY]

自动质量强制实施：

**Hook configuration:**
```json
{
  "hooks": {
    "PostToolUse": [{
      "tool": "Write",
      "script": "npm run lint:fix -- $FILE"
    }, {
      "tool": "Edit",
      "script": "npm run lint:fix -- $FILE"
    }],
    "PreToolUse": [{
      "tool": "Bash",
      "command": "git commit",
      "script": ".claude/hooks/pre-commit.sh"
    }]
  }
}
```

**Pre-commit Hook 脚本：**
```bash
#!/bin/bash
npm run lint || exit 1
npm test || exit 1
echo "All checks passed"
```

**结果：** 每次文件编辑都会自动进行 lint 检查。每次提交都需要通过测试。无需人工干预即可强制执行质量。

### 协同模式 9：视觉驱动开发 [COMMUNITY]

使用截图和模型作为实现目标：

```bash
# Share a design mockup
"Here's the Figma mockup for the new dashboard @mockups/dashboard.png
Implement this in src/components/Dashboard.tsx using our existing
Button, Card, and Chart components. Match the layout exactly."

# Iterate on visual feedback
"Here's a screenshot of the current result @screenshots/current.png
Compare to the mockup. Fix: the spacing between cards is wrong,
and the chart colors don't match."

# Debug visual issues
"This screenshot shows a layout bug on mobile @bugs/mobile-layout.png
The sidebar overlaps the content. Fix the responsive styles in
src/styles/layout.css"
```

**为何有效：** Claude 能看见图像。具体的视觉目标可减少歧义，迭代速度快。

### 协同模式 10：日志分析流水线 [OFFICIAL]

Unix 流水线 + Claude 用于实时分析：

```bash
# Monitor logs for anomalies
tail -f /var/log/app.log | claude -p "Alert me if you see errors or unusual patterns"

# Analyze crash dumps
cat crash.log | claude -p "Analyze this crash. Identify root cause and suggest fix."

# Parse and summarize
grep "ERROR" app.log | claude -p "Categorize these errors by type and frequency. Which is most critical?"

# CI/CD integration
npm test 2>&1 | claude -p "If tests failed, explain why and suggest fixes"
```

**为什么有效：** Claude集成Unix流水线。可与现有工具组合使用。

### 协同模式 11：模式驱动开发 [COMMUNITY]

数据库模式作为事实来源：

```bash
# Generate types from schema
"Read prisma/schema.prisma and generate TypeScript interfaces
in src/types/database.ts. Include JSDoc comments explaining each field."

# Create API endpoints from schema
"Based on the User model in schema.prisma, create CRUD endpoints
in src/api/users.ts. Include validation using zod."

# Generate test fixtures
"Read the schema and create realistic test fixtures in
tests/fixtures/users.ts. Cover edge cases: empty strings,
max lengths, special characters."

# Migration safety check
"Compare prisma/schema.prisma with the current database.
Identify breaking changes. Suggest migration strategy."
```

**为何有效：** Schema 是契约。一切均由它生成。单一事实来源。

### 协同模式 12：依赖管理 [COMMUNITY]

在一个流程中更新、测试和修复：

```bash
# Check for updates
"Run npm outdated. For each major update, explain breaking changes
and effort to upgrade."

# Upgrade with safety net
"Upgrade lodash to v5. Run tests. If anything breaks, fix it.
Commit only when tests pass."

# Security audit flow
"Run npm audit. For each vulnerability:
1. Check if we actually use the affected code path
2. If yes, upgrade or find alternative
3. If no, document why it's acceptable"

# License compliance
"Check licenses of all dependencies. Flag any GPL or unknown
licenses. We need MIT/Apache/BSD only."
```

**为何有效：**依赖管理十分繁琐。Claude 负责研究和修复。

### 协同模式 13：文档生成 [COMMUNITY]

代码库探索 → 活的文档：

```bash
# API documentation
"Explore src/api/ and generate OpenAPI spec in docs/api.yaml.
Include request/response examples from actual code."

# Architecture documentation
"Analyze the codebase structure. Create docs/ARCHITECTURE.md
explaining: folder structure, data flow, key patterns used."

# Onboarding guide
"Create docs/ONBOARDING.md for new developers. Include:
setup steps, key files to understand first, common tasks,
gotchas you found in the code."

# Changelog from commits
"Read git log for the last month. Generate CHANGELOG.md
grouped by: Features, Fixes, Breaking Changes."
```

**为何有效：** 文档与代码保持同步。源自源代码，而非记忆。

### 协同模式 14：带安全网的重构 [COMMUNITY]

大型重构而不破坏现有功能：

```bash
# Rename with confidence
"Rename the User class to Account across the entire codebase.
Update all imports, types, and documentation. Run tests after."

# Extract component
"The Dashboard component is 500 lines. Extract the chart logic
into src/components/DashboardChart.tsx. Keep all behavior identical.
Tests must still pass."

# Change data structure
"Migrate from storing user.fullName to user.firstName + user.lastName.
Update: database schema, API responses, frontend display, tests.
Create migration script for existing data."

# Upgrade patterns
"Replace all callback-style async code in src/services/ with
async/await. One file at a time. Test after each file."
```

**工作原理：** TodoWrite 跟踪进度。测试验证正确性。安全的增量变更。

### 协同模式 15：事件响应 [COMMUNITY]

系统化地调试生产问题：

```bash
# Initial triage
"Production is returning 500 errors. Here's the error log:
[paste log]
Identify the most likely cause. List files to investigate."

# Root cause analysis
"Read the files identified. Trace the code path from
API endpoint to error. Explain exactly where and why it fails."

# Fix with minimal blast radius
"Implement the smallest possible fix. Don't refactor.
Just stop the bleeding. Add a TODO for proper fix later."

# Post-mortem documentation
"Create docs/incidents/2024-01-15-500-errors.md documenting:
what happened, root cause, fix applied, prevention measures."
```

**为何它有效：** 结构化的方法可以防止恐慌。文档可以防止问题复发。

### 提示词最佳实践 [OFFICIAL]

根据 [Anthropic 的指南](https://www.anthropic.com/engineering/claude-code-best-practices)：

| 与其… | 不如… |
|--------|-------|
| "添加测试" | "为 src/utils/date.ts 编写 Jest 测试，涵盖：使用有效日期的 formatDate、无效输入以及时区处理" |
| "修复这个 bug" | "当邮箱中包含 '+' 时登录失败。修复 src/auth/validate.ts:23，以处理电子邮件地址中的加号" |
| "审查此代码" | "审查 src/api/users.ts 中是否存在：N+1 查询、缺少错误处理以及 SQL 注入风险" |
| "让它更快" | "对 /api/products 端点进行性能分析。找出最慢的操作并优化。目标：响应时间 <100ms" |

**思考模式**（逐步提升推理深度）：
- `"think"` — 标准扩展思考
- `"think hard"` — 更深入的分析
- `"think harder"` — 深度探索可选方案
- `"ultrathink"` — 最大限度推理预算

**文件引用：**
```bash
# Use tab-completion or explicit paths
"Read @src/auth/login.ts and explain the authentication flow"

# Multiple files
"Compare @src/api/v1/users.ts and @src/api/v2/users.ts - what changed?"
```

### 关键原则 [COMMUNITY]

**1. 理解每个功能的触发时机：**

| 功能 | 触发时机... |
|---------|-------------------|
| MCP | 需要外部数据/动作 |
| Skills | 上下文匹配描述（自动） |
| Commands | 用户输入 `/command`（手动） |
| Hooks | 生命周期事件触发（PreToolUse, PostToolUse 等） |
| Sub-agents | 任务委托以进行独立工作 |

**2. 组合实现价值倍增：**
```
MCP alone           = 1x (fetch data)
MCP + Skill         = 3x (fetch + auto-expertise)
MCP + Skill + Hook  = 9x (fetch + expertise + enforce)
```
每一层都在前一层的基础上加倍。投入于初始设置。

**3. 提示词是基础：**
所有协同效应都会因模糊的提示词而失效。先掌握具体性：
- 明确指定文件名
- 明确说明需求
- 明确定义成功标准

**4. 我们展示了15种协同效应，但远不止于此。**
这些模式只是起点。组合它们，改编它们，发现你自己的模式。最好的工作流是为你的项目量身定制的。

**5. 初始设置成本会摊销：**
花一小时配置 `.claude/` 将在未来的会话中节省数百小时。把它视为基础设施。

## 示例库

### 示例 1：添加身份认证

```bash
# Understanding current system
> "Analyze the current user management system"

# Planning
> "Create a plan to add JWT-based authentication"

# Implementation
> "Implement the authentication system following the plan"
# (Claude creates TodoWrite tasks and works through them)

# Testing
> "Create comprehensive tests for authentication"

# Security review
> "Review the authentication implementation for security issues"

# Documentation
> "Update the API documentation with authentication endpoints"

# Commit
> "Create a git commit for the authentication feature"
```

### 示例 2：性能优化

```bash
# Identify issues
> "Analyze the codebase for performance bottlenecks"

# Create optimization plan
> "Create a plan to optimize the most critical issues found"

# Implement optimizations
> "Implement the database query optimizations"

# Benchmark
> "Create benchmarks to measure the improvements"

# Verify
> "Run the benchmarks and compare before/after"
```

### 示例 3：Bug 调查

```bash
# Provide context
> "Users report login fails intermittently. Here's the error log: [paste log]"

# Investigation with Debug agent
> "Use the debugger agent to investigate this issue"

# Root cause analysis
> "Explain what's causing this and why it's intermittent"

# Fix
> "Implement a fix for this issue"

# Prevention
> "Add tests and logging to prevent this in the future"

# Documentation
> "Update CLAUDE.md with what we learned about this issue"
```

### 示例 4：API 迁移

```bash
# Analyze current API
> "Document all endpoints in the v1 API"

# Plan migration
> "Create a migration plan from v1 to v2 with these changes: [list changes]"

# Implement new version
> "Implement the v2 API alongside v1"

# Ensure backward compatibility
> "Create a compatibility layer so v1 clients still work"

# Testing
> "Create tests ensuring both v1 and v2 work correctly"

# Documentation
> "Generate migration guide for API consumers"
```

### 示例 5：设置 CI/CD

```bash
# Research
> "Research GitHub Actions best practices for Node.js projects"

# Create workflow
> "Create a GitHub Actions workflow that:
   - Runs on pull requests
   - Checks TypeScript compilation
   - Runs linting
   - Runs all tests
   - Reports coverage"

# Security scanning
> "Add security scanning to the workflow"

# Deployment
> "Add automatic deployment to staging on merge to main"

# Documentation
> "Document the CI/CD setup in README.md"
```

### 示例 6：多目录项目

```bash
# Add directories
> "Add the frontend and backend directories to the workspace"

# Synchronized changes
> "Update the User type definition in backend and propagate to frontend"

# Cross-project validation
> "Ensure the frontend API calls match the backend endpoints"

# Parallel testing
> "Run backend tests and frontend tests in parallel in background"

# Monitor both
> "Start both dev servers and monitor for errors"
```

### 示例 7：后台开发工作流

```bash
# Start all development services in background
> "Start the frontend dev server in background"
> "Start the backend API server in background"
> "Run tests in watch mode in background"

# Configure status line to track all services
/statusline

# Monitor all services simultaneously
> "Monitor all background processes for errors"

# Claude watches logs from all background tasks
# Identifies issues across services
# Suggests fixes without stopping services

# Fix issues dynamically
> "I see an API timeout error"
# Claude checks backend logs, identifies cause, suggests solution

# Check all background tasks
/bashes

# Stop specific service if needed
/kill <id>
```

### 示例 8：智能上下文管理

```bash
# Start major feature development
> "Build a complete user authentication system with JWT, refresh tokens, and password reset"

# Work progresses, context accumulates...
# After reading many files and multiple operations
# Context is getting large

# Use microcompact for intelligent cleanup
/compact "focus"
# Keeps: Current auth work, recent changes, patterns learned
# Removes: Old file reads, completed searches, stale context

# Continue seamlessly with clean context
> "Add two-factor authentication to the system"
# Full context available for current authentication work

# Major context switch to new feature
/compact
# Complete reset for fresh start

> "Implement Stripe payment integration"
# Clean slate for payment feature
```

### 示例 9：安全优先开发

```bash
# Plan with security considerations
> "Design a user input handling system for our forms. Focus on security best practices"

# Implement with immediate security review
> "Implement the form validation system"
> "Review the form validation code for security vulnerabilities"

# Fix identified issues
> "Fix the XSS vulnerability in the email field validation"
> "Verify the fix addresses all injection vectors"

# Document security patterns
> "Update CLAUDE.md with our input validation security patterns"

# Set up continuous security monitoring
> "Create a GitHub Action that runs security scans on every PR"
```

### 示例 10：全栈多仓库开发

```bash
# Initialize multi-repo workspace
/add-dir ~/projects/backend
/add-dir ~/projects/frontend
/add-dir ~/projects/shared-types

# Synchronize type definitions across projects
> "Update the User type in shared-types and ensure backend and frontend are consistent"

# Parallel type checking
> "Run TypeScript type checking in all three projects simultaneously in background"

# Monitor and fix type errors
> "Check background tasks for any type errors"
> "Fix type mismatches found in frontend"

# Cross-repo validation
> "Verify that all API types in backend match the frontend client expectations"

# Start all dev servers
> "Start backend server, frontend server, and type watching in background"

# Unified development experience
> "Build the checkout flow, coordinating changes across backend API and frontend UI"
# Claude makes coordinated changes across all repos
```

---

## 最佳实践

### 面向开发者 [COMMUNITY]

**1. 首先设置 CLAUDE.md**
```markdown
- Document your project structure
- List important commands
- Note conventions and patterns
- Add known gotchas
- Update it as you learn
```

**2. 使用描述性请求**
```bash
# Good
> "Add input validation to the login endpoint, checking email format and password length"

# Less effective
> "Fix login"
```

**3. 验证更改**
```bash
# Always review before committing
> "Show me all the changes made"
> "Run tests to verify the changes"
```

**4. 增量式开发**
```bash
# Break large features into steps
> "First, let's add the database model"
> "Now add the API endpoint"
> "Finally, add the frontend form"
```

**5. 智能运用工具**
```bash
# Use Grep for finding patterns
> "Find all database queries using raw SQL"

# Use Glob for file discovery
> "Find all test files"

# Use sub-agents for exploration
> "Have an Explore agent map out the authentication flow"
```

### 决策模式 [COMMUNITY]

常见场景的快速决策树：

**某个功能不工作：**
```
→ Can you reproduce it?
  → Yes: Debug systematically
  → No: Gather more info first
→ Did it work before?
  → Yes: Check recent changes (git diff)
  → No: Check assumptions
→ Is error message clear?
  → Yes: Address directly
  → No: Trace execution with logging
```

**添加新功能：**
```
→ Similar feature exists?
  → Yes: Follow that pattern
  → No: Research best practices
→ Touches existing code?
  → Yes: Understand it first (read, analyze)
  → No: Design in isolation
→ Has complex logic?
  → Yes: Break down first (use TodoWrite)
  → No: Implement directly
```

**代码似乎运行缓慢：**
```
→ Measured it? → No: Profile first
→ Know the bottleneck? → No: Find it (use ultrathink)
→ Have solution? → No: Research, then implement and measure again
```

**出现问题时如何恢复:**
```bash
# Establish facts
> "What's the current state of the codebase?"

# Find smallest step forward
> "What's the simplest fix that would work?"

# Question assumptions
> "Let me re-read the relevant code"

# Find solid ground
> "Let's revert to the last working state with /rewind"
```

**复杂度驱动方法：**
| 任务类型 | 处理方法 |
|-----------|----------|
| 琐碎（错字修正） | 直接修复 |
| 简单（添加按钮） | 快速实现 |
| 中等（新功能） | 规划 → 实现 → 测试 |
| 复杂（架构调整） | 调研 → 设计 → 原型 → 实现 → 迁移 |
| 未知 | 先探索评估，再选择方法 |

### 面向团队 [COMMUNITY]

**1. 共享配置**
```bash
# Commit to git:
.claude/
├── settings.json      # Shared permissions and config
├── commands/          # Team workflows
├── skills/            # Team Skills
└── agents/            # MCP servers & sub-agents

# Git-ignore:
.claude/settings.local.json  # Personal overrides
```

**2. CLAUDE.md 中的文档模式**
```markdown
## Team Conventions
- All API routes follow RESTful patterns
- Database migrations use Prisma
- Tests use the AAA pattern (Arrange, Act, Assert)
- Never commit directly to main
```

**3. 创建 Workflow Skills**
```bash
# .claude/skills/
├── code-review/
│   └── SKILL.md
├── deploy-staging/
│   └── SKILL.md
├── run-checks/
│   └── SKILL.md
└── security-audit/
    └── SKILL.md
```

**4. 使用 Hooks 实现标准化**
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {"type": "command", "command": "eslint-check.sh"}
        ]
      }
    ]
  }
}
```

### 面向安全 [COMMUNITY]

**1. 保护敏感文件**
```json
{
  "permissions": {
    "deny": {
      "Write": ["*.env", ".env.*", "*.key", "*.pem"],
      "Edit": ["*.env", ".env.*", "*.key", "*.pem", ".git/*"]
    }
  }
}
```

**2. 执行前审查**
```json
{
  "permissions": {
    "defaultMode": "ask"
  }
}
```

**3. 使用 Hooks 进行审计**
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "echo \"$(date): $TOOL_NAME\" >> .claude/audit.log"
          }
        ]
      }
    ]
  }
}
```

**4. 定期安全审查**
```bash
# Use security review Skill or command
> "Perform a security audit of the authentication system"
```

---

## 故障排除

### 常见问题 [COMMUNITY]

**问题："Context too large"错误**
```bash
# Solution 1: Compact context
> /compact

# Solution 2: Smart cleanup
> /compact "focus"

# Prevention: Regular compaction in long sessions
```

**问题：编辑工具因 "string not found" 失败**
```bash
# Solution: Read the file first to see exact content
> Read the file to see the exact string

# Ensure exact match including:
- Whitespace and indentation
- Line breaks
- Special characters

# Use larger context if string appears multiple times
```

**问题：权限被拒绝**
```bash
# Solution 1: Grant permission when asked

# Solution 2: Pre-configure in settings.json
{
  "permissions": {
    "allow": {
      "Bash": ["npm test"],
      "Edit": {}
    }
  }
}

# Check current permissions
> /hooks  # Shows hook configuration
```

**问题：Claude 无法看到最近的文件更改**
```bash
# Solution: Explicitly ask to re-read
> "Read the app.ts file again"

# Or provide the changes
> "I just updated the config, here's what changed: [paste]"
```

**问题：后台任务无响应**
```bash
# Check status
> /bashes

# Kill if stuck
> /kill <id>

# Restart
> "Start the dev server again in background"
```

**问题：Git 操作失败**
```bash
# Check git status
> "Run git status"

# Common fixes:
- Unstaged changes: "git add the files first"
- Merge conflicts: "Show me the conflicts and help resolve"
- Branch issues: "Switch to the correct branch"
```

**问题：MCP 服务器不工作**
```bash
# Check configuration
> "Show me the MCP configuration"

# Verify server is running
> "Check if the MCP server started correctly"

# Check logs
~/.claude/logs/mcp-<server-name>.log

# Reinstall
> "Reinstall the MCP server package"
```

### 错误恢复模式 [COMMUNITY]

**常见错误场景的系统性应对方案。**

#### 断开连接后的会话恢复

```bash
# If session disconnects mid-task:
1. Check recent history:
   > "What was I working on?"

2. Review file changes:
   git diff

3. Reconstruct state:
   > "Based on recent changes, continue where we left off"
```

#### Hook 失败

```bash
# If hook blocks unexpectedly:
1. Check hook output:
   claude --debug

2. Test hook manually:
   echo '{"tool_name":"Edit","tool_input":{...}}' | ~/.claude/hooks/script.sh

3. Temporarily disable:
   mv ~/.claude/settings.json ~/.claude/settings.json.bak

4. Fix and restore:
   # Fix the hook script, then restore settings
```

#### 任务中途上下文溢出

```bash
# When "context too large" appears during complex work:

# Quick recovery:
> /compact "focus"
> "Continue with [brief task summary]"

# Full reset if needed:
> /compact
> "Let me brief you: [key context]"

# Prevention:
- Use /compact "focus" every ~50 operations
- Start fresh sessions for new features
```

#### 工具权限问题

```bash
# When permissions repeatedly requested:

# Grant permanently:
{
  "permissions": {
    "allow": {
      "Bash": {},      # Allow all bash
      "Edit": {},      # Allow all edits
      "Write": {}      # Allow all writes
    }
  }
}

# Or specific patterns:
{
  "permissions": {
    "allow": {
      "Bash": ["npm test", "npm run build"]
    }
  }
}
```

#### 网络/API 超时

```bash
# If operations timeout:

# Retry with backoff:
1st attempt → fails
Wait 2s → retry
Wait 4s → retry
Wait 8s → retry

# Switch model if persistent:
> "Use a different model to try this"

# Check network:
ping anthropic.com
curl -v https://api.anthropic.com
```

#### 丢失工作恢复

```bash
# If changes weren't saved:

1. Check git:
   git status
   git diff

2. Check file backups:
   ls -la ~/.claude/backups/

3. Review session transcript:
   # Transcripts saved in ~/.claude/transcripts/

4. Reconstruct from memory:
   > "Based on our conversation, recreate the [feature]"
```

#### 针对持久问题的调试模式

```bash
# Enable comprehensive debugging:
claude --debug --log-level trace

# Follow logs in real-time:
tail -f ~/.claude/logs/claude.log

# Filter for specific issues:
grep -i error ~/.claude/logs/claude.log
grep -i "mcp" ~/.claude/logs/claude.log
```

---

## 安全注意事项

### 安全模型 [OFFICIAL]

Claude Code 操作基于：

**1. 权限系统**
- 工具需要明确权限
- 权限是会话级别的
- 可在设置中预配置

**2. 沙箱化** (macOS/Linux)
```json
{
  "sandbox": {
    "enabled": true,
    "allowUnsandboxedCommands": false
  }
}
```

**3. 文件访问控制**
```json
{
  "permissions": {
    "additionalDirectories": ["/allowed/path"],
    "deny": {
      "Read": ["*.key", "*.pem"],
      "Write": ["*.env"],
      "Edit": [".git/*"]
    }
  }
}
```

### 最佳安全实践 [COMMUNITY]

**1. 绝不提交机密信息**
```bash
# Block in settings
{
  "permissions": {
    "deny": {
      "Write": ["*.env", "*.key", "*.pem", "*secret*"],
      "Edit": ["*.env", "*.key", "*.pem", "*secret*"]
    }
  }
}

# Use hooks to scan for secrets
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {"type": "command", "command": "detect-secrets-hook.sh"}
        ]
      }
    ]
  }
}
```

**2. 审查 AI 生成的代码**
```bash
# Always review before deploying
> "Explain the security implications of this code"
> "Review this for potential vulnerabilities"
```

**3. 限制工具访问**
```json
// For sub-agents doing analysis
{
  "allowedTools": ["Read", "Grep", "Glob"]  // No modifications
}

// For implementation agents
{
  "allowedTools": ["Read", "Write", "Edit", "Bash"]  // Can modify
}
```

**4. 审计跟踪**
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "logger.sh"  // Log all operations
          }
        ]
      }
    ]
  }
}
```

**5. 网络限制**
```json
{
  "sandbox": {
    "network": {
      "allowUnixSockets": ["/var/run/docker.sock"],
      "allowLocalBinding": true,
      "httpProxyPort": 8080
    }
  }
}
```

**来源:** [Settings](https://code.claude.com/docs/en/settings), [Sandboxing](https://code.claude.com/docs/en/sandboxing)

## SDK集成

**Claude Code 可以通过 TypeScript/Python SDK 以编程方式使用。**

### 使用案例 [OFFICIAL]

- 在 CI/CD 中自动化工作流
- 基于 Claude Code 构建自定义工具
- 创建自动化的代码审查系统
- 集成到现有开发工具中
- 批量处理多个项目

### TypeScript SDK示例 [OFFICIAL]

```typescript
import { ClaudeCodeSDK } from '@anthropic-ai/claude-code';

const sdk = new ClaudeCodeSDK({
  apiKey: process.env.ANTHROPIC_API_KEY
});

// Start a session
const session = await sdk.startSession({
  projectDir: '/path/to/project',
  systemPrompt: 'You are a code reviewer'
});

// Send a task
const response = await session.chat({
  message: 'Review this codebase for security issues'
});

console.log(response.content);

// End session
await session.end();
```

### Python SDK示例 [OFFICIAL]

```python
from anthropic_sdk import ClaudeCodeSDK

sdk = ClaudeCodeSDK(api_key=os.environ["ANTHROPIC_API_KEY"])

# Start session
session = sdk.start_session(
    project_dir="/path/to/project",
    system_prompt="You are a test generator"
)

# Send task
response = session.chat(
    message="Generate tests for all API endpoints"
)

print(response.content)

# End session
session.end()
```

**来源：** [SDK 概览](https://code.claude.com/docs/en/sdk/sdk-overview)

## 实验性概念

> ⚠️ **警告**：本节包含**理论概念**和**模式**，这些内容**未在官方文档中经过验证**。这些是供高级用户探索的实验性想法。

### 概念：认知模式 [EXPERIMENTAL]

**未经证实的理论** 关于根据任务类型优化Claude的方法：

```bash
# Simple Creation Mode
> "Create 5 similar React components"
# Theory: Parallel processing, template-based

# Optimization Mode
> "Optimize this algorithm"
# Theory: Deep analysis, multiple approaches

# Research Mode
> "Research and implement best practice for X"
# Theory: Web search → analysis → implementation pipeline
```

**状态**: 没有官方文档支持“模式”。Claude Code 对所有任务使用相同的模型。

### 概念：内核架构 [EXPERIMENTAL]

**未经证实的理论框架**关于多层智能：

```
Theory:
┌─────────────────┐
│   Orchestrator  │
└────────┬────────┘
         │
    ┌────┴────┬────────┬─────────┐
    │         │        │         │
  Memory   Intent  Extract  Validate
  Kernel   Kernel  Kernel   Kernel
```

**状态**：这是一个概念模型，并非实际的 Claude Code 功能。Claude Code 使用：
- 子代理（实际功能）
- Skills（实际功能）
- Hooks（实际功能）

但并非“内核架构”系统。

### 概念：元待办系统 [EXPERIMENTAL]

**未经证实的理论**：关于使用AI验证的高级任务管理

```bash
# Theory: Multi-agent task validation
1. Intent Capture (4 approaches)
2. Multi-Agent Validation
3. Background Execution
4. Learning Integration
```

**状态**：TodoWrite 是一个真实的工具，但带有多智能体验证的“meta-todo”是理论上的。请按照文档使用实际的 TodoWrite 工具。

### 为何分开讨论 [EDITORIAL]

原始指南混合了：
- **真实功能** (Skills, Hooks, MCP)
- **使用模式** (如何使用功能)
- **理论框架** (未经证实的概念)

这导致人们对 Claude Code 实际能做到什么与概念性想法产生了混淆。

**对于阅读本文的AI智能体**：请专注于标记为 `[OFFICIAL]` 和 `[COMMUNITY]` 的部分。将 `[EXPERIMENTAL]` 视为需要测试的想法，而非既定功能。

---

## 附加资源

### 官方文档 [OFFICIAL]
- **主文档**: https://code.claude.com/docs/en/overview
- **CLI 参考**: https://code.claude.com/docs/en/cli-reference
- **设置**: https://code.claude.com/docs/en/settings
- **Skills**: https://code.claude.com/docs/en/skills
- **Hooks**: https://code.claude.com/docs/en/hooks
- **MCP**: https://code.claude.com/docs/en/mcp
- **Sub-Agents**: https://code.claude.com/docs/en/sub-agents
- **Plugins**: https://code.claude.com/docs/en/plugins

### 社区资源 [COMMUNITY]
- **GitHub**: https://github.com/anthropics/claude-code
- **Awesome Claude Code**: https://github.com/hesreallyhim/awesome-claude-code
- **Awesome Claude Skills**: https://github.com/travisvn/awesome-claude-skills

### 获取帮助
- **GitHub Issues**: https://github.com/anthropics/claude-code/issues
- **Discord**: 查看 Anthropic 的社区频道
- **文档**: https://code.claude.com

---

## 变更日志

### Claude Code CLI版本发布 [OFFICIAL]

完整详情请参阅[官方 CHANGELOG.md](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)。

**版本 2.1.39**（2026 年 2 月 10 日）- 最新版
- ⚡ 改进了终端渲染性能
- 🐛 修复了致命错误被吞没而不显示的问题
- 🐛 修复了会话关闭后进程挂起的问题
- 🐛 修复了终端屏幕边界处字符丢失的问题
- 🐛 修复了详细转录视图中的空白行问题

**版本 2.1.38**（2026 年 2 月 10 日）
- 🐛 修复了 VS Code 终端滚动到顶部的回归问题（在 2.1.37 中引入）
- 🐛 修复了 Tab 键将斜杠命令加入队列而非自动补全的问题
- 🐛 修复了使用环境变量包装器的命令的 bash 权限匹配问题
- 🐛 修复了未使用流式传输时工具调用之间文本消失的问题
- 🐛 修复了在 VS Code 扩展中恢复会话时出现重复会话的问题
- 🔒 改进了 heredoc 分隔符解析以防止命令走私
- 🔒 在沙箱模式下阻止写入 `.claude/skills` 目录

**版本 2.1.37**（2026 年 2 月 7 日）
- 🐛 修复了启用 `/extra-usage` 后 `/fast` 不能立即可用的问题

**版本 2.1.36**（2026 年 2 月 7 日）
- ⚡ **Opus 4.6 现支持快速模式** [新增]

**版本 2.1.34**（2026 年 2 月 6 日）
- 🐛 修复了在渲染之间更改智能体团队设置时崩溃的问题
- 🐛 修复了当启用 `autoAllowBashIfSandboxed` 时，被排除在沙箱化之外的命令绕过 Bash 询问权限的问题

**版本 2.1.33**（2026 年 2 月 6 日）
- 🤖 tmux 中的智能体队友会话现在能正确收发消息
- 🪝 新增了用于多智能体工作流的 `TeammateIdle` 和 `TaskCompleted` 钩子事件 [新增]
- 🔧 增加了通过 `Task(agent_type)` 语法限制子代理的支持
- 📝 为智能体新增了 `memory` 前置字段（支持 `user`、`project` 或 `local` 作用域）
- 🔌 技能描述中现在会显示插件名称，以提高可发现性
- 🐛 修复了提交新消息时扩展思考中断的问题
- 🐛 修复了流式传输端点上的 API 代理 404 错误
- 🐛 修复了通过 `settings.json` 环境变量设置的代理未应用于 WebFetch 的问题
- 📊 改进了 `/resume` 会话选择器，标题更简洁（移除了原始 XML 标记）
- 📝 增强了 API 连接失败时的错误信息（显示具体原因，如 ECONNREFUSED、SSL 错误）
- 🔌 [VSCode] 新增了带 OAuth 的远程会话支持
- 🔌 [VSCode] 在会话选择器中增加了 git 分支和消息数量显示，并支持分支名称搜索
- 🔌 [VSCode] 修复了加载/切换会话时滚动到底部不足的问题

**版本 2.1.32**（2026 年 2 月 5 日）
- ✨ **Claude Opus 4.6 现已可用！** [新增]
- 🤖 新增了用于多智能体协作的研究预览版**智能体团队**功能 [新增]
- 🧠 Claude 现在会在工作过程中自动记录和回忆**记忆** [新增]
- 📊 在消息选择器中新增了“从此处开始摘要”，用于部分对话摘要
- 📁 额外目录（`--add-dir`）中 `.claude/skills/` 下的技能现在会自动加载
- 🐛 修复了 `@` 文件补全显示子目录中错误相对路径的问题
- 🔄 `--resume` 现在会复用上次对话中的 `--agent` 值
- 🐛 修复了包含 JavaScript 模板字面量的 heredoc 出现 bash “Bad substitution” 错误的问题
- 📊 技能字符预算现在随上下文窗口缩放（上下文的 2%）
- 🐛 修复了泰语/老挝语间隔元音的渲染问题
- 🔌 [VSCode] 修复了斜杠命令错误地与前面文本一起执行的问题
- 🔌 [VSCode] 加载过往对话时增加了转圈动画

**版本 2.1.31**（2026 年 2 月 4 日）
- 💡 退出时新增会话恢复提示，说明如何稍后继续对话
- 🌐 在复选框选择中增加了来自日文 IME 的全角空格输入支持
- 🤖 改进了系统提示，引导模型使用专用工具（Read、Edit、Glob、Grep）而非 bash 等效操作
- 🐛 修复了 PDF 过大错误导致会话永久锁定的问题
- 🐛 修复了沙箱模式下 bash 命令错误报告“只读文件系统”错误的问题
- 🐛 修复了因 `~/.claude.json` 缺少默认字段而进入计划模式后崩溃的问题
- 🐛 修复了在流式 API 路径中 `temperatureOverride` 被忽略的问题
- 🐛 修复了 LSP 关闭/退出与严格语言服务器的兼容性问题
- ⚡ 减少了旋转动画期间终端布局的抖动
- 📝 改进了 PDF 和请求大小的错误信息（显示实际限制：100 页、20MB）
- 💰 移除了面向第三方提供商用户（Bedrock、Vertex、Foundry）的误导性 Anthropic API 定价显示

**版本 2.1.30**（2026 年 2 月 3 日）
- 📄 为 PDF 的 Read 工具新增了 `pages` 参数（例如 `pages: "1-5"`） [新增]
- 📄 大 PDF（>10 页）在使用 @ 提及时会返回轻量级引用
- 🔑 新增了无需动态客户端注册的 MCP 服务器预配置 OAuth 凭据
- 🔍 新增了用于排查会话问题的 `/debug` 命令 [新增]
- 📊 在 Task 结果中增加了 token 计数、工具使用次数和持续时间指标
- ♿ 新增了减少动效模式配置选项（`prefersReducedMotion` 设置） [新增]
- 🐛 修复了 API 对话历史中幻影“（无内容）”文本块的问题
- 🐛 修复了提示缓存失效问题（现在在工具描述/模式变更时能正确重新验证）
- 🐛 修复了 `/login` 后因对话中包含思考块而产生 400 错误的问题
- 🐛 修复了恢复含有损坏转录的会话时挂起的问题
- 🐛 修复了 Max 20x 用户的速率限制消息
- 🐛 修复了子代理无法访问 SDK 提供的 MCP 工具的问题
- 🐛 修复了 Windows 下因 `.bashrc` 文件导致 bash 执行失败的问题
- 🐛 修复了 VSCode 中的重复会话问题
- ⚡ 针对包含大量会话的 `--resume` 减少了 68% 的内存占用
- 📊 `TaskStop` 工具现在会显示已停止的命令/任务描述
- ⚡ `/model` 现在立即执行，而不是加入队列
- ⌨️ [VSCode] 问题对话框中支持多行输入（Shift+Enter）

**版本 2.1.29**（2026 年 1 月 31 日）
- ⚡ 修复了恢复包含 `saved_hook_context` 的会话时的启动性能问题

**版本 2.1.27**（2026 年 1 月 30 日）
- 🔗 新增了 `--from-pr` 标志，用于恢复链接到特定 GitHub PR 编号或 URL 的会话
- 🔗 通过 `gh pr create` 创建的会话现在会自动链接到 PR
- 🔒 权限现在优先采用内容级别的 `ask` 而非工具级别的 `allow`（例如 `allow: ["Bash"], ask: ["Bash(rm *)"]`）
- 🔍 工具调用失败和拒绝现已添加到调试日志中
- 🐛 修复了 `/context` 命令的彩色输出显示问题
- 🐛 修复了状态栏中后台任务指示器与 PR 状态重复显示的问题
- 🔌 [VSCode] 启用了 Chrome 集成中的 Claude 功能
- 🪟 [Windows] 修复了带 `.bashrc` 文件的用户执行 bash 命令失败的问题
- 🪟 [Windows] 修复了生成子进程时控制台窗口闪烁的问题
- 🔌 [VSCode] 修复了长时间会话后 OAuth 令牌过期导致 401 错误的问题

**Version 2.1.25**（2026年1月29日）
- 🔧 修复了 Bedrock 和 Vertex 上网关用户的 beta 头部验证错误
- 💡 临时解决方案：设置 `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1` 可避免该错误

**Version 2.1.23**（2026年1月29日）
- ⚙️ 新增可自定义的旋转动画动词设置（`spinnerVerbs`）
- 🔧 修复了企业代理或使用客户端证书用户的 mTLS 和代理连接问题
- 🔧 修复了每个用户的临时目录隔离问题，防止共享系统上的权限冲突
- 🐛 修复了启用提示缓存作用域时的竞态条件导致 400 错误的问题
- 🐛 修复了无头流式会话结束时，待处理的异步 hooks 未被取消的问题
- 🐛 修复了接受建议时 Tab 补全未更新输入框的问题
- 🐛 修复了 ripgrep 搜索超时静默返回空结果而未报告错误的问题
- ⚡ 通过优化屏幕数据布局，提升了终端渲染性能
- ⏱️ bash 命令现在除运行时间外还显示超时持续时间
- 🟣 合并的拉取请求现在在提示栏底部显示紫色状态指示器
- 🔌 [IDE] 修复了无头模式下 Bedrock 用户的模型选项显示错误区域字符串的问题

**Version 2.1.22**（2026年1月28日）
- 🔧 修复了非交互模式（-p）的结构化输出问题

**Version 2.1.21**（2026年1月28日）
- 🌐 在选项选择提示中增加了对日语 IME 全角数字输入的支持
- 🐛 修复了退出时 shell 补全缓存文件被截断的问题
- 🐛 修复了恢复在工具执行期间中断的会话时出现的 API 错误
- 🐛 修复了在具有较大输出令牌限制的模型上自动压缩过早触发的问题
- 🐛 修复了任务 ID 在删除后可能被重复使用的问题
- 🐛 修复了 Windows 上 VS Code 扩展中文件搜索无法工作的问题
- 📊 改进了读取/搜索进度指示器：进行中显示“正在读取…”，完成时显示“已读取”
- 🤖 改进了 Claude，使其优先使用文件操作工具（读取、编辑、写入）而非等效的 bash 命令（cat、sed、awk）
- 🐍 [VSCode] 增加了自动 Python 虚拟环境激活功能（`claudeCode.usePythonEnvironment` 设置）
- 🔌 [VSCode] 修复了消息操作按钮背景颜色错误的问题

**Version 2.1.20**（2026年1月27日）
- ⌨️ Vim 普通模式下的方向键历史导航
- ⌨️ 在帮助菜单中增加了外部编辑器快捷键（Ctrl+G）
- 📊 在提示栏底部显示 PR 审查状态指示器（已批准/需修改/待处理/草稿）
- 📁 支持通过 `--add-dir` 从额外目录加载 `CLAUDE.md`（需要设置 `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1`）
- 🗑️ 通过 `TaskUpdate` 工具删除任务
- 📱 根据终端高度动态调整任务列表
- 📋 `/copy` 命令现已对所有用户开放
- ⚙️ 配置备份现在带有时间戳并进行轮换（保留最近5个备份）
- 🐛 修复了会话压缩问题导致恢复时加载完整历史记录的问题
- 🐛 修复了智能体在活动工作时忽略用户消息的问题
- 🐛 修复了宽字符（表情符号、中日韩字符）渲染异常的问题
- 🐛 修复了 MCP 响应中特殊 Unicode 字符导致 JSON 解析错误的问题
- 🐛 修复了浏览命令历史时丢失草稿提示的问题
- 🐛 修复了取消工具使用时崩溃的问题

**Version 2.1.19**（2026年1月23日）
- ✨ 新增环境变量 `CLAUDE_CODE_ENABLE_TASKS` - 设置为 `false` 可使用旧版任务系统
- ✨ 新增简写符 `$0`、`$1` 等，用于在自定义命令中访问单个参数
- 🔄 索引参数语法从 `$ARGUMENTS.0` 变更为 `$ARGUMENTS[0]`（方括号语法）
- ✅ 没有额外权限或 hooks 的 Skills 不再需要批准
- 🐛 修复了没有 AVX 指令支持的处理器上崩溃的问题
- 🐛 修复了终端关闭时 Claude Code 进程残留的问题（EIO 错误处理、SIGKILL 回退）
- 🐛 修复了从不同目录恢复会话时 `/rename` 和 `/tag` 未更新正确会话的问题
- 🐛 修复了从不同目录按自定义标题恢复会话的问题
- 🐛 修复了使用提示暂存（Ctrl+S）时粘贴文本丢失的问题
- 🐛 修复了智能体列表显示“Sonnet（默认）”而非“继承（默认）”的问题
- 🐛 修复了后台挂起的 hook 命令未提前返回的问题
- 🐛 修复了文件写入预览省略空行的问题
- 🔌 [SDK] 增加了将 `queued_command` 附加消息作为 `SDKUserMessageReplay` 事件重放的功能
- 🔌 [VSCode] 对所有用户启用了会话分叉和回退功能

**Version 2.1.17**（2026年1月22日）
- 🔧 修复了没有 AVX 指令支持的处理器上崩溃的问题

**Version 2.1.16**（2026年1月22日）
- ✨ 新的任务管理系统，支持依赖追踪
- 🔌 [VSCode] 原生插件管理支持
- 🔌 [VSCode] OAuth 用户可以从“会话”对话框中浏览和恢复远程 Claude 会话
- 🐛 修复了恢复大量子代理使用的会话时内存不足崩溃的问题
- 🐛 修复了运行 `/compact` 后“剩余上下文”警告未隐藏的问题
- 🐛 修复了恢复屏幕上会话标题未遵循用户语言设置的问题
- 🪟 [IDE] 修复了 Windows 上启动时 Claude Code 侧边栏视图容器无法显示的竞态条件

**Version 2.1.15**（2026年1月21日）
- ⚠️ 添加了 npm 安装的弃用通知——用户被引导运行 `claude install` 或访问 https://docs.anthropic.com/en/docs/claude-code/getting-started
- ⚡ 使用 React Compiler 提升了 UI 渲染性能
- 🐛 修复了运行 `/compact` 后“距自动压缩还有剩余上下文”警告未消失的问题
- 🐛 修复了 MCP stdio 服务器超时未杀死子进程，导致 UI 冻结的问题 **2.1.14** (2026年1月20日)
- ⌨️ 在 bash 模式下基于历史记录的自动补全 (`!`) - 按 Tab 补全部分命令
- 🔍 为已安装的插件列表添加搜索功能
- 📌 支持将插件固定到特定的 Git commit SHA
- 🔧 修复了上下文窗口阻断限制计算过于激进的问题（约65%而非约98%）
- 🐛 修复了并行子代理导致崩溃的内存问题
- 🐛 修复了长时间运行会话中流资源清理时的内存泄漏
- 🐛 修复了在 bash 模式下 `@` 符号触发文件自动补全的问题
- 📊 [VSCode] 添加了 `/usage` 命令以显示当前的计划用量

**版本 2.1.12** (2026年1月17日)
- 🔧 修复了消息渲染错误

**版本 2.1.11** (2026年1月17日)
- 🔧 修复了 HTTP/SSE 传输的过多 MCP 连接请求

**版本 2.1.10** (2026年1月17日)
- 🪝 新增通过 `--init`、`--init-only` 或 `--maintenance` CLI 标志触发的 `Setup` 钩子事件
- ⌨️ 在登录时按键盘快捷键 'c' 复制 OAuth URL
- 🐛 修复了包含 JavaScript 模板字符串的 heredoc 的 bash 命令
- ⚡ 改进了启动过程，在 REPL 就绪前即可捕获按键
- 📎 文件建议现在显示为可移除的附件
- 🔌 [VSCode] 添加了插件安装计数显示和信任警告

**版本 2.1.9** (2026年1月16日)
- ✨ MCP 工具搜索自动启用阈值的 `auto:N` 语法（上下文窗口百分比）
- 📁 `plansDirectory` 设置用于自定义计划文件的存储位置
- ⌨️ 在 AskUserQuestion 的“其他”输入中支持外部编辑器（Ctrl+G）
- 🔗 将会话 URL 归因于来自 Web 会话的提交和 PR
- 🪝 `PreToolUse` 钩子现在可以向模型返回 `additionalContext`
- 🔧 技能中的 `${CLAUDE_SESSION_ID}` 字符串替换
- 🐛 修复了长时间会话中并行工具调用因孤立的 tool_result 错误而失败的问题
- 🐛 修复了 MCP 服务器重新连接在缓存连接 promise 上挂起的问题
- 🐛 修复了 Ctrl+Z 挂起操作在 Kitty 键盘协议终端中不起作用的问题

**版本 2.1.7** (2026年1月14日)
- ⚙️ `showTurnDuration` 设置用于隐藏轮次持续时间消息
- 💬 可以为权限提示提供反馈
- 📱 任务通知中的内联代理响应显示
- 🔒 安全修复：通配符权限规则漏洞
- 🪟 改进了 Windows 文件同步兼容性
- 🔧 MCP 工具搜索自动模式默认启用
- 🔗 OAuth/API 控制台 URL 迁移至 `platform.claude.com`

**版本 2.1.6** (2026年1月13日)
- 🔍 在 `/config` 命令中添加搜索功能
- 📊 `/stats` 中的日期范围过滤（7/30天、全部时间）
- 🔄 `/doctor` 命令中的更新部分
- 📁 发现嵌套的 `.claude/skills` 目录
- 📈 `context_window.used_percentage` 和 `remaining_percentage` 状态字段
- 🔒 权限绕过安全修复（shell 行续接）

**版本 2.1.5** (2026年1月12日)
- 📁 `CLAUDE_CODE_TMPDIR` 环境变量用于覆盖临时目录

**版本 2.1.3** (2026年1月9日)
- 🔀 合并了斜杠命令和技能（简化心智模型）
- 📻 在 `/config` 中切换发布渠道（`stable`/`latest`）
- ⚠️ 权限规则不可达性检测和警告
- 📝 修复了计划文件在 `/clear` 后的持久化问题
- ⏱️ 工具钩子执行超时时间设为 10 分钟

**版本 2.1.2** (2026年1月9日)
- 🖼️ 拖入图像的源路径元数据
- 🔗 文件路径的 OSC 8 超链接（iTerm 支持）
- 🪟 支持 Windows 包管理器（winget）
- ⌨️ 在计划模式下按 Shift+Tab 可“自动接受编辑”
- 🔒 修复了 bash 处理中的命令注入漏洞
- 🧹 修复了 tree-sitter 解析树中的内存泄漏
- 💾 将大量输出持久化到磁盘而非截断

**版本 2.1.0** (2025年12月23日)
- 🔄 自动技能热重载
- 🔀 支持 `context: fork` 用于技能子代理
- 🌐 设置 `language` 以控制 Claude 的响应语言
- ⌨️ Shift+Enter 在 iTerm2、WezTerm、Ghostty、Kitty 中开箱即用
- 📁 `respectGitignore` 设置用于按项目控制
- 🎯 Bash 工具权限的通配符模式匹配（`*` 语法）
- ⌨️ 统一的 `Ctrl+B` 后台操作，适用于 bash 命令和代理
- 🌐 面向 claude.ai 订阅者的 `/teleport` 和 `/remote-env` 命令
- ⚡ 代理可以在 frontmatter 中定义钩子
- ✂️ 新的 Vim 动作：`;` 和 `,` 重复、`y` 运算符、`p`/`P` 粘贴
- 🔧 `--tools` 标志用于限制工具使用
- 📄 `CLAUDE_CODE_FILE_READ_MAX_OUTPUT_TOKENS` 环境变量
- 🖼️ 在 iTerm2 中支持 Cmd+V 粘贴图片

**版本 2.0.74** (2025年12月19日)
- 🔍 **LSP 工具**：用于代码智能的语言服务器协议
- 📍 转到定义、查找引用、悬停文档
- 🖥️ 支持 Kitty、Alacritty、Zed、Warp 的 `/terminal-setup`
- 🎨 在 `/theme` 中添加 `Ctrl+T` 快捷键用于切换语法高亮

**版本 2.0.72** (2025年12月18日)
- 🌐 通过 Chrome 扩展控制 Chrome 中的 Claude（Beta）
- ⚡ 在 git 仓库中 `@` 文件建议速度提升约 3 倍
- ⌨️ 将思考模式切换快捷键从 Tab 更改为 Alt+T

**版本 2.0.70** (2025年12月16日)
- ⌨️ 按 Enter 键立即提交提示建议（Tab 编辑）
- 🎯 MCP 工具权限的通配符语法 `mcp__server__*`
- 🧠 改进内存使用（大对话的内存使用减少 3 倍）

**版本 2.0.67** (2025年12月12日)
- 💡 Claude 现在可以建议提示（按 Tab 接受或按 Enter 提交）
- 🧠 默认对 Opus 4.5 启用思考模式
- 🔍 在 `/permissions` 命令中添加搜索功能

**版本 2.0.65** (2025年12月11日)
- ⌨️ 在 Linux/Windows 上按 Alt+P 或在 macOS 上按 Option+P 可随时切换模型
- 📊 状态栏中的上下文窗口信息
- 🔧 `CLAUDE_CODE_SHELL` 环境变量用于 shell 检测

**版本 2.0.64** (2025年12月10日)
- ⚡ 即时自动压缩
- 🔄 异步代理和带有唤醒消息的 bash 命令
- 📊 `/stats` 提供使用统计和参与度指标
- 📝 命名会话支持：`/rename` 和 `/resume <name>`
- 📁 支持 `.claude/rules/` 目录

**版本 2.0.60** (2025年12月6日)
- 🔄 支持后台代理（代理在后台运行的同时可继续工作）
- 🔧 `--disable-slash-commands` CLI 标志
- 📝 在“Co-Authored-By”提交消息中添加模型名称
- 🔀 快速切换 `/mcp enable|disable [server-name]`

**版本 2.0.51** (2025年11月24日)- 🧠 Opus 4.5 发布
- 🖥️ Claude Code for Desktop 发布
- 📝 Plan 模式可制定更精确的计划

**版本 2.0.45**（2025 年 11 月 19 日）
- ☁️ 支持 Azure AI Foundry
- 🔐 `PermissionRequest` 钩子，用于自动批准/拒绝逻辑

**版本 2.0.24**（2025 年 10 月 21 日）
- 🛡️ Linux/Mac 上 BashTool 的沙箱模式
- 🌐 支持从 Claude Code Web 快速跳转到 CLI

**版本 2.0.20**（2025 年 10 月 17 日）
- ⭐ Claude Skills：可复用的提示模板

**版本 2.0.12**（2025 年 10 月 9 日）
- 🔌 插件系统发布
- `/plugin install`、`/plugin enable/disable`、`/plugin marketplace`

**版本 2.0.10**（2025 年 10 月 8 日）
- ✨ 重写了终端渲染器（界面丝滑流畅）
- 🔀 使用 `@mention` 启用/禁用 MCP 服务器
- ⌨️ 在 bash 模式下为 shell 命令提供 Tab 补全
- ✏️ PreToolUse 钩子可修改工具输入
- ⌨️ 按 `Ctrl-G` 在系统文本编辑器中编辑 prompt

**版本 2.0.0**（2025 年 9 月 29 日）
- 🆕 全新的原生 VS Code 扩展
- ✨ 整个应用焕然一新的 UI
- ⏪ `/rewind` 撤销代码更改
- 📊 `/usage` 查看计划用量限制
- ⌨️ Tab 切换思考模式（粘滞）
- 🔍 Ctrl-R 搜索历史
- 🤖 SDK 更名为 Claude Agent SDK
- 🔧 `--agents` 标志用于动态子代理

### 破坏性变更与弃用 [OFFICIAL]

**2.1.x 版本的破坏性变更：**

| 变更 | 迁移路径 |
|--------|----------------|
| **Windows 托管设置路径** | 从 `C:\ProgramData\ClaudeCode\managed-settings.json` 迁移到 `C:\Program Files\ClaudeCode\managed-settings.json` |
| **移除 @-提及 MCP 启用/禁用** | 请改用 `/mcp enable <name>` 或 `/mcp disable <name>` |
| **工具钩子超时时间增加** | 现在为 10 分钟（之前是 60 秒）——若依赖快速超时，请更新脚本 |
| **SDK 最低 zod 版本** | 要求将 zod ^4.0.0 作为对等依赖项 |

### 本指南的变更日志

**版本 2026.1.13（2026 年 2 月 11 日）**
- 更新至 v2.1.39（最新发布版本）
- 新增 v2.1.38 和 v2.1.39 的更新日志条目：
  - v2.1.39：终端渲染性能改进、致命错误显示修复、进程挂起修复、屏幕边界字符修复、详细日志空行修复
  - v2.1.38：VSCode 滚回顶部回归修复、Tab 键自动补全修复、bash 权限匹配修复、流式文本修复、重复会话修复、heredoc 安全改进、沙箱技能目录保护
- 在“高级功能”部分新增 **快速模式（Fast Mode）** 章节，包含完整文档：
  - 切换方法（`/fast` 命令、设置）
  - 定价表（标准模式 vs 快速模式）
  - 要求（订阅、额外使用量、管理员启用）
  - 使用场景指导（何时使用 vs 避免使用）
  - 速率限制行为及降级策略

**版本 2026.1.12（2026 年 2 月 9 日）**
- 更新至 v2.1.37（最新发布版本）
- 新增 v2.1.36 和 v2.1.37 的更新日志条目：
  - v2.1.37：修复启用 `/extra-usage` 后 `/fast` 不能立即可用的问题
  - v2.1.36：**Opus 4.6 现在支持快速模式**
- 在“用量与统计”部分新增 `/extra-usage` 和 `/fast` 斜杠命令

**版本 2026.1.11（2026 年 2 月 7 日）**
- 更新至 v2.1.34
- 新增 v2.1.32 至 v2.1.34 的更新日志条目：
  - v2.1.34：修复智能体团队设置崩溃问题，修复被排除命令的沙箱权限绕过问题
  - v2.1.33：TeammateIdle 和 TaskCompleted 钩子事件、Task(agent_type) 限制语法、智能体的 memory 前置元数据、改进的会话选择器、VSCode 远程会话 OAuth、多项错误修复
  - v2.1.32：**Claude Opus 4.6 可用**、**智能体团队（Agent Teams）** 功能（研究预览版）、**自动记忆（Auto-Memory）** 功能、“从此处总结”消息选择器、`--add-dir` 目录中的技能、多项错误修复
- 新增 **智能体团队** 章节，包含详尽文档：
  - 团队架构（主导智能体、队友、任务列表、邮箱）
  - 显示模式（进程内、tmux、自动）
  - 团队钩子（TeammateIdle、TaskCompleted）
  - 键盘控制与限制
- 新增 **自动记忆** 功能文档
- 新增 `--teammate-mode` CLI 标志，用于智能体团队显示配置
- 在钩子表中新增 `TeammateIdle` 和 `TaskCompleted` 钩子事件
- 新增环境变量 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` 和 `CLAUDE_CODE_DISABLE_AUTO_MEMORY`
- 更新目录，加入智能体团队链接

**版本 2026.1.10（2026 年 2 月 5 日）**
- 更新至 v2.1.31（最新发布版本）
- 新增 v2.1.30 和 v2.1.31 的更新日志条目：
  - v2.1.31：退出时会话恢复提示、日语 IME 全角空格支持、改进的工具偏好提示、PDF 错误处理修复、沙箱 bash 修复、计划模式崩溃修复、温度覆盖修复、LSP 兼容性改进、旋转动画改进、更好的错误信息
  - v2.1.30：PDF 的 `pages` 参数（Read 工具）、`/debug` 命令、`prefersReducedMotion` 设置、MCP 预配置 OAuth、任务结果指标、会话恢复内存减少 68%、VSCode 多行输入、多项错误修复
- 在 Read 工具部分新增 PDF `pages` 参数文档
- 新增 `/debug` 斜杠命令，用于排查会话问题
- 新增 `prefersReducedMotion` 无障碍设置文档
- 更新 PDF 限制文档（100 页、20MB）

**版本 2026.1.9（2026 年 2 月 1 日）**
- 更新至 v2.1.29（最新发布版本）
- 新增 v2.1.29 的更新日志条目：
  - 修复了包含 `saved_hook_context` 的会话启动性能问题

**版本 2026.1.8（2026 年 1 月 31 日）**
- 更新至 v2.1.27（更新时的最新发布版本）
- 新增 v2.1.25 和 v2.1.27 的更新日志条目：
  - v2.1.27：`--from-pr` 标志，用于恢复与 PR 关联的会话；通过 `gh pr create` 创建时会话自动关联；权限优先级（内容级别 `ask` 覆盖工具级别 `allow`）；VSCode Chrome 集成；Windows 修复
  - v2.1.25：网关用户的 Beta 头部验证修复，`CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS` 变通方案
- 在 CLI 标志参考中新增 `--from-pr` 标志
- 新增环境变量 `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS` 文档
- 新增 VSCode Chrome 集成功能
- 新增权限优先级文档（内容级别规则覆盖工具级别规则）

**版本 2026.1.7（2026 年 1 月 29 日）**
- 更新至 v2.1.23（最新发布版本）
- 新增 v2.1.21 至 v2.1.23 的更新日志条目：
  - v2.1.23：可自定义的旋转动词设置、mTLS/代理连接修复、终端渲染改进、bash 超时显示
  - v2.1.22：修复非交互模式的结构化输出
  - v2.1.21：日语 IME 支持、VSCode 中 Python 虚拟环境激活、会话恢复修复、改进的文件操作偏好
- 新增 `spinnerVerbs` 设置文档，用于自定义旋转消息
- 新增 VSCode Python 虚拟环境激活功能（`claudeCode.usePythonEnvironment`）
- 新增已合并 PR 的紫色状态指示器行为

**版本 2026.1.6（2026 年 1 月 27 日）**
- 更新至 v2.1.20
- 新增 v2.1.20 的更新日志条目：
  - vim 普通模式下方向键历史导航
  - 帮助菜单中的外部编辑器快捷键（Ctrl+G）
  - 提示栏中的 PR 审查状态指示器
  - 从 `--add-dir` 目录加载 CLAUDE.md（带环境变量开关）
  - 通过 TaskUpdate 工具删除任务
  - 基于终端高度的动态任务列表
  - `/copy` 命令现在对所有用户开放
  - 配置备份轮转（保留最近 5 个）
  - 多项错误修复（会话压缩、宽字符、MCP Unicode 等）
- 新增钩子事件：`PostToolUseFailure`、`SubagentStart`
- 新增 `/copy` 斜杠命令文档
- 新增环境变量 `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD`
- 新增完整的桌面应用功能章节：
  - 带行内评论的差异视图
  - 用于并行会话的 Git worktrees
  - `.worktreeinclude` 文件文档
  - macOS 和 Windows 安装链接

**版本 2026.1.5（2026 年 1 月 25 日）**
- 更新至 v2.1.19（最新发布版本）
- 新增 v2.1.19 的更新日志条目：
  - `CLAUDE_CODE_ENABLE_TASKS` 环境变量，用于使用旧版任务系统
  - 自定义命令的简写参数语法（`$0`、`$1`）
  - 索引参数语法从 `$ARGUMENTS.0` 改为 `$ARGUMENTS[0]`（方括号语法）
  - 没有额外权限/钩子的技能不再需要审批
  - VSCode 会话分支与回退功能对所有用户开放
  - 多项错误修复（进程清理、会话恢复、提示堆栈等）
- 新增官方文档中的 CLI 标志：
  - `--json-schema` 用于验证 JSON 输出
  - `--permission-prompt-tool` 用于 MCP 权限处理
  - `--setting-sources` 用于配置来源控制
  - `--allow-dangerously-skip-permissions` 用于可组合的权限绕过
  - `--include-partial-messages` 用于流式事件
  - `--init`、`--init-only`、`--maintenance` 设置钩子标志
- 新增索引参数文档，包含方括号语法和简写
- 新增 VSCode 会话分支与回退功能
- 新增监控/遥测环境变量章节
- 新增高级环境变量（`MAX_THINKING_TOKENS`、`MAX_MCP_OUTPUT_TOKENS` 等）

**版本 2026.1.4（2026 年 1 月 23 日）**
- 更新至 v2.1.17（包含 AVX 指令修复的最新版本）
- 新增 v2.1.14 至 v2.1.17 的更新日志条目：
  - v2.1.17：修复不支持 AVX 指令的处理器上的崩溃
  - v2.1.16：新的任务管理系统，支持依赖追踪；VSCode 原生插件管理；OAuth 会话浏览
  - v2.1.15：npm 安装弃用通知；React Compiler 性能改进
  - v2.1.14：bash 模式中基于历史记录的自动补全；插件固定到 Git 提交 SHA；插件搜索
- 在安装章节新增 npm 弃用通知
- 新增 TodoWrite 依赖追踪文档
- 扩展 VSCode 插件功能章节（原生插件管理、远程会话浏览、`/usage` 命令）
- 新增 bash 模式自动补全快捷键章节
- 新增插件固定文档（基于 Git 提交 SHA 固定）

**版本 2026.1.3（2026 年 1 月 18 日）**
- 新增 v2.1.10 更新日志（设置钩子、OAuth 复制快捷键、VSCode 插件功能）
- 新增新的 `Setup` 钩子事件，用于 `--init`、`--init-only`、`--maintenance` 标志
- 新增 `PermissionRequest` 钩子事件文档
- 新增快捷键 'c'，用于在登录时复制 OAuth URL
- 新增 VSCode 插件功能章节（安装计数显示、信任警告）
- 修复钩子事件表，包含所有已记录的事件

**版本 2026.1.2（2026 年 1 月 18 日）**
- 更新至 v2.1.12（包含消息渲染修复的最新版本）
- 扩展 CLI 标志参考，新增 30 多个标志，包括：
  - 远程会话标志（`--remote`、`--teleport`、`--fork-session`）
  - 系统提示自定义（`--system-prompt`、`--append-system-prompt`）
  - 工具/权限管理（`--tools`、`--allowedTools`、`--permission-mode`）
  - 预算限制（`--max-budget-usd`、`--max-turns`）
  - MCP 配置（`--mcp-config`、`--strict-mcp-config`）
- 新增 15 个以上来自官方文档的斜杠命令：
  - `/bug`、`/cost`、`/privacy-settings`、`/output-style`、`/vim`、`/sandbox`
  - `/agents`、`/init`、`/install-github-app`、`/pr-comments`、`/review`
  - `/security-review`、`/todos`、`/login`、`/logout`、`/release-notes`
- 重写了 MCP 安装章节，加入新的传输类型：
  - HTTP 传输（推荐用于托管服务）
  - Stdio 传输（用于本地包）
  - 安装范围（本地、项目、用户）
  - CLI 命令（`claude mcp add/list/get/remove`）
- 修复 `/microcompact` 引用（现在为 `/compact`，可附加说明）
- 更新了 MCP 的 OAuth 认证示例

**版本 2026.1.1（2026 年 1 月 17 日）**
- 更新至 v2.1.11（最新发布版本）
- 新增 v2.1.9 至 v2.1.11 的更新日志条目
- 将所有文档 URL 从 docs.anthropic.com 更新为 code.claude.com
- 新增安装方法（curl 脚本、Homebrew、WinGet）
- 新增 MCP 工具搜索 `auto:N` 语法文档
- 新增 `plansDirectory` 设置文档
- 新增 `${CLAUDE_SESSION_ID}` 技能变量替换
- 新增重大变更与弃用章节
- 新增 PreToolUse 的 `additionalContext` 钩子功能

**版本 2026.1（2026 年 1 月）**
- 主要更新，涵盖 v2.0.34 至 v2.1.7
- 新增 **LSP 工具** 文档（转到定义、查找引用、悬停）
- 新增 **思考模式（Thinking Mode）** 章节（Tab 切换、超级思考、Alt+T）
- 新增 **计划模式（Plan Mode）** 文档
- 新增 **后台任务与智能体（Background Tasks & Agents）** 章节（Ctrl+B）
- 新增全面的 **键盘快捷键** 参考
- 新增 **环境变量** 完整列表
- 新增 **提示建议（Prompt Suggestions）** 文档
- 新增 20 多个斜杠命令（`/rewind`、`/stats`、`/usage`、`/config`、`/doctor`、`/terminal-setup`、`/rename`、`/resume`、`/teleport`、`/remote-env` 等）
- 新增设置文档（语言、归属、respectGitignore 等）
- 新增 `.claude/rules/` 目录文档
- 新增通配符权限语法
- 更新更新日志至 v2.1.7

**版本 2025.0（2025 年 1 月）**
- 完全重写，聚焦于已验证的功能
- 明确区分官方内容与实验性内容
- 新增技能系统文档
- 新增插件文档
- 新增 `/statusline` 和 `/add-dir` 命令
- 新增 CLI 标志参考章节
- 增强 `@filename` 引用语法文档
- 全面的示例与模式
- 所有声明均与官方文档核对

**旧版** 混淆了 Claude.ai Web 功能（REPL、Artifacts）与 Claude Code CLI 功能，造成困惑。本版本仅专注于 Claude Code CLI。

---

## 自动更新流水线

本指南是一份**活文档**，会随着 Claude Code 的开发自动保持更新。

### 工作原理

每两天一次的流水线（UTC 时间凌晨 3:00）运行 Claude Code 以：

1. **检查官方来源：**
   - [官方文档](https://code.claude.com/docs/en/overview) — 官方文档
   - [GitHub Releases](https://github.com/anthropics/claude-code/releases) — 版本更新日志
   - [Anthropic Changelog](https://www.anthropic.com/changelog) — 产品更新

2. **与当前指南内容进行比较**

3. **使用已验证的更改进行更新：**
   - 新功能与能力
   - 已更改的 CLI 标志或命令
   - 新工具或集成
   - 错误修复或弃用功能

4. **自动提交更改**，并附上详细的提交信息

### 更新日志

请参阅 [update-log.md](./update-log.md) 了解自动更新的历史记录。

### 手动触发

更新也可以手动运行：
```bash
./scripts/update-guide.sh
```

---

## 许可证

本指南由社区维护，并非 Anthropic 官方出品。内容源自官方文档 (code.claude.com) 及社区经验。

如需官方信息，请始终参考：https://code.claude.com/docs/en/overview

---

**指南结束**

> **面向 AI 智能体**：你已到达经过验证的 Claude Code 指南的末尾。所有标记为 `[OFFICIAL]` 的功能均在 code.claude.com 上有文档记录。标记为 `[COMMUNITY]` 的功能是广泛使用的模式。`[EXPERIMENTAL]` 部分的内容属于理论性，在依赖之前应先进行验证。

