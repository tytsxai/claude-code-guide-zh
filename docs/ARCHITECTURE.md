# 架构说明 Architecture · claude-code-guide-zh

本文解释「**结构保真**的 LLM Markdown 翻译流水线」是如何工作的 —— 即如何在用大模型翻译技术文档的同时，**不破坏 Markdown 结构、代码块和页内链接**。代码以 [`tools/`](../tools/) 为准。

## 数据流 / Pipeline

```
上游英文仓库 (UPSTREAM_REPO)
        │  git clone --depth / fetch
        ▼
  本地缓存 .cache/upstream
        │  git diff 上次同步 commit..HEAD   (sync.py + state.py)
        ▼
  变更的 .md / .markdown 文件
        │  解析为「标题 / 正文 / 代码」节点   (structured_doc.py)
        ▼
  ┌──────────────┬───────────────────────────┐
  │ 标题 headings │ 正文 prose   │ 代码 code    │
  │ 批量翻译       │ 分块翻译      │ 逐字节保留    │
  │ 层级逐字复制    │ 多 Key 并发   │ 不送入模型    │
  └──────────────┴───────────────────────────┘
        │  glossary 术语提示 + fixups 确定性修订
        │  英文锚点 → 中文标题锚点改写
        ▼
  content/ 镜像目录（写回）+ .sync-state.json 更新
```

## 核心设计 / Key ideas

### 1. 标题 / 正文 / 代码三分离（结构零损失）
`structured_doc.py` 把文档解析为有序节点。**标题单独批量翻译**，重组时 `#` 层级**直接从英文原文逐字复制**，因此标题数量与层级与原文 100% 一致，不会漏标题或改层级。

### 2. 代码块永不进模型（围栏零损坏）
正文按「散文 / 代码」交替切分，**代码块整段逐字节保留、绝不发送给模型**。这从根本上杜绝了「模型改写代码围栏 / 翻译命令 / 破坏缩进」的问题，代码块前后字节完全一致。

### 3. 边界空白保留（防粘连）
大模型常会吞掉段落首尾换行，导致 `---` 与下一个标题、或散文与代码围栏粘连。翻译前剥离片段首尾空白、翻译后**回贴原始空白**，使段落边界对模型行为免疫。

### 4. 锚点自愈（页内链接可跳转）
GitHub 依据标题文本生成锚点；标题译成中文后，原英文锚点（如 `#what-is-claude-code`）会失效。流水线在翻译后**按中文标题重新计算 slug 并改写所有 `](#...)` 链接**，目录因此保持可点击。

### 5. 多 Key 轮询 + 故障转移
`translator.py` 的 `KeyPool` 在多个 DeepSeek Key 间轮询；遇到限流（429/402）或鉴权失败（401/403）自动隔离该 Key 并切换，配合并发翻译显著提速。

### 6. 章节级缓存
按「模型 + 术语表 + 片段内容」哈希缓存翻译结果。未变动段落零成本复用，因此重复运行 / 增量同步几乎不消耗 API。

### 7. 确定性修订层
- `glossary.json`：翻译时作为提示，统一保留英文术语与固定译法。
- `fixups.json`：译后**确定性字符串替换**，沉淀人工确认的术语归一化与定点修正，每次运行自动复用，使流水线对已知问题「自愈」。

## 模块一览 / Modules

| 文件 | 职责 |
|---|---|
| [`tools/sync.py`](../tools/sync.py) | 入口：拉取上游、diff、调度翻译、写回、记录状态/日志 |
| [`tools/translator.py`](../tools/translator.py) | DeepSeek 客户端、多 Key 轮询、并发、缓存、标题/正文翻译编排 |
| [`tools/structured_doc.py`](../tools/structured_doc.py) | 标题/正文/代码解析、GitHub slug、锚点改写 |
| [`tools/markdown_chunker.py`](../tools/markdown_chunker.py) | 按章节切分长文（不切断代码块） |
| [`tools/fixups.py`](../tools/fixups.py) | 应用 `fixups.json` |
| [`tools/config.py`](../tools/config.py) | 全部配置与环境变量（密钥仅来自环境变量） |
| [`tools/state.py`](../tools/state.py) | 记录已同步到的上游 commit |

## 质量校验 / Verification

每次写回后，可对译文做确定性校验：标题数量与层级、代码块逐字节一致性、页内锚点是否全部可解析。初版译文已通过该校验。
