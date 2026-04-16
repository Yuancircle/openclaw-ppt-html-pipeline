# PPT HTML Pipeline

[English](#ppt-html-pipeline) | [中文](#ppt-html-pipeline-中文版)

Build **exceptionally polished PPT-style HTML slides** from page-by-page detailed requirement drafts.

This repository packages a production-oriented pipeline for turning **single-slide planning docs** into **reviewed, presentation-grade HTML pages** with a strong PPT feel rather than generic web-page aesthetics.

## What it does

PPT HTML Pipeline is designed for teams who want HTML slides that feel like:
- mature executive presentation pages
- projection-friendly report slides
- high-density, high-clarity visual pages
- structured, reviewable slide production outputs

Instead of directly prompting for HTML in one shot, this pipeline uses a staged flow:

```text
Detailed page draft
-> blueprint generation
-> blueprint review
-> HTML generation
-> HTML review
-> final single-page HTML
```

It also includes a controller-oriented front-door flow:

```text
LLM client preflight / bootstrap / repair
-> page-by-page detailed requirement drafts
-> per-page pipeline execution
-> reviewed final HTML pages
```

## Why it is different

Most "HTML slide" generators produce something that still looks like:
- landing pages
- dashboards
- card-based websites
- over-spaced modern web UI

This project is explicitly optimized for **PPT-feel HTML**:
- stronger page hierarchy
- denser but controlled layouts
- presentation-safe typography
- executive-report visual language
- fewer meaningless empty areas
- less “website” feeling, more “serious slide” feeling

## Core strengths

### 1. Page-by-page detailed requirement input
The pipeline starts from **detailed page drafts**, not vague prompts.
That means each slide can preserve:
- page role in the deck
- previous / next page relation
- required information blocks
- style direction
- forbidden patterns
- hard rules

### 2. Blueprint-first workflow
Before HTML is generated, the pipeline first creates a **construction blueprint** for the page.
This forces structure and reduces layout drift.

### 3. Review loops built into the pipeline
The system does not just generate.
It also reviews:
- blueprint quality
- HTML quality
- PPT feeling
- projection readability
- consistency with page intent

### 4. Automatic LLM client preflight
Before the main slide workflow starts, the pipeline can:
- check whether an LLM client is already ready
- bootstrap one from the host OpenClaw default model config
- run smoke tests
- repair adapter selection internally
- cache working client/adapters for reuse

### 5. Better fit for real reporting scenarios
This repository is especially useful when you need HTML pages for:
- leadership reporting
- internal strategy presentations
- product / project milestone reviews
- technical architecture reporting
- structured proposal decks

## Repository structure

```text
.
├── README.md
├── SKILL.md
├── prompts/
│   └── ppt_pipeline/
│       ├── blueprint_maker.system.md
│       ├── blueprint_reviewer.system.md
│       ├── html_builder.system.md
│       └── html_reviewer.system.md
├── references/
│   └── batch-example.md
└── scripts/
    ├── ppt_page_pipeline.py
    └── validators.py
```

## Expected input shape

Each page should be described in a markdown draft using explicit fields such as:
- page number
- page title
- page goal
- previous / next page relation
- style requirements
- forbidden items
- core content
- hard rules
- output path

The richer the page draft, the stronger the final result.

## Ideal workflow

1. Confirm the deck structure with the user
2. Create one detailed draft markdown per page
3. Run pipeline per page
4. Let blueprint / review / HTML / review happen automatically
5. Only intervene when the pipeline blocks or review fails
6. Deliver reviewed final page HTML files

## Status

This project already contains the core workflow, prompts, validators, and controller-facing conventions needed for a strong first production system.

It is especially strong when the goal is:
> **produce extremely high-quality PPT-style HTML pages, not ordinary web pages**

## Positioning

If you want HTML that merely “looks modern,” many tools can do that.

If you want HTML that feels like:
- a real presentation slide
- a serious report page
- a page a leader can review on screen

this pipeline is built for that job.

---

# PPT HTML Pipeline 中文版

[返回 English](#ppt-html-pipeline)

把**逐页详细需求稿**稳定转成**极高质量的 PPT 风格 HTML 单页**。

这个仓库封装的是一套面向生产的流水线，不是“随便生成个网页页面”，而是把**单页策划稿 / 详细需求稿**转成**经过审核、适合汇报、具有成熟 PPT 感**的 HTML 页面。

## 它能做什么

PPT HTML Pipeline 适合这类目标：
- 做领导汇报页
- 做投屏展示页
- 做结构清晰、信息密度高的单页汇报 HTML
- 做一整套可审查、可返工、可批量生产的页面流程

它不是一把梭直接生成 HTML，而是走分阶段流程：

```text
逐页详细需求稿
-> 施工图生成
-> 施工图审核
-> HTML 生成
-> HTML 审核
-> 最终单页 HTML
```

同时，它还包含主控前置流程：

```text
LLM client 前置检查 / bootstrap / 修复
-> 逐页详细需求稿
-> 逐页执行流水线
-> 输出审核后的最终 HTML
```

## 为什么它和普通 HTML 生成器不一样

大多数“HTML 幻灯片”工具最后做出来的东西仍然很像：
- 落地页
- 仪表盘
- 卡片网站
- 留白很大的现代网页 UI

而这个项目明确追求的是：
- 更强的页面层级
- 更成熟的 PPT 感
- 适合投屏的字号与密度
- 更像领导汇报页的视觉语言
- 减少无意义留白
- 明显降低“网页感”

## 核心优势

### 1）逐页详细需求稿驱动
流水线从**逐页详细需求稿**出发，而不是从一句模糊提示词出发。

这样每一页都能保留：
- 页面在整套汇报中的角色
- 上下页关系
- 必须出现的信息块
- 风格方向
- 禁止项
- 特殊硬规则

### 2）先施工图，后 HTML
在生成 HTML 之前，流水线会先生成**施工图 / blueprint**。

这样能明显减少页面跑偏，先把：
- 结构
- 视觉重心
- 阅读路径
- 版面骨架

先定下来，再进入 HTML 制作。

### 3）自带审核闭环
这套系统不只是“生成”，还会审核：
- 施工图质量
- HTML 质量
- PPT 感
- 投屏可读性
- 是否忠实原页面意图

### 4）自动化 LLM client 前置处理
在正式生成页面前，系统会先做：
- 检查是否已有可用 LLM client
- 按宿主 OpenClaw 默认模型自动 bootstrap
- 做 smoke test
- 在内部修复 adapter 选择
- 缓存可复用的 client / adapter

### 5）更适合真实汇报场景
这个仓库特别适合：
- 领导汇报
- 战略方案汇报
- 产品/项目进展汇报
- 技术架构汇报
- 结构化方案演示

## 仓库结构

```text
.
├── README.md
├── SKILL.md
├── prompts/
│   └── ppt_pipeline/
│       ├── blueprint_maker.system.md
│       ├── blueprint_reviewer.system.md
│       ├── html_builder.system.md
│       └── html_reviewer.system.md
├── references/
│   └── batch-example.md
└── scripts/
    ├── ppt_page_pipeline.py
    └── validators.py
```

## 输入要求

每一页建议用 markdown 明确写出这些字段：
- 页码
- 页面标题
- 页面目标
- 上一页关系
- 下一页关系
- 风格要求
- 禁用项
- 核心内容
- 特殊硬规则
- 输出路径

详细需求稿越扎实，最终页面质量越高。

## 理想使用方式

1. 先和用户确认整套 PPT 结构
2. 每页形成一份详细需求稿 markdown
3. 逐页运行流水线
4. 让施工图 / 审核 / HTML / 审核自动进行
5. 只有在阻塞或审核失败时才人工介入
6. 最终交付经过审核的逐页 HTML

## 当前定位

这个项目已经具备：
- 核心流程
- 提示词
- 校验器
- 面向主控的流程约定

适合用来构建一套强质量导向的 PPT HTML 生产系统。

如果你只是想做“看起来现代”的 HTML，很多工具都能做。

但如果你要的是：
- 真正像汇报页
- 像正式演示页
- 像领导可以直接看的页面

那这个流水线就是为这件事设计的。
