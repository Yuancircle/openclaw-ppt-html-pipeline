# PPT HTML Pipeline

[English](#ppt-html-pipeline) | [中文](#ppt-html-pipeline-中文版)

Build **presentation-grade PPT-style HTML slides** with a **blueprint -> review -> HTML -> review** pipeline.

Designed for teams who want **serious slide pages**, not generic landing pages or dashboard-like web UI.

## Why this exists

Most AI-generated "HTML slides" still look like:
- landing pages
- dashboards
- card-based web layouts
- overly empty modern UI

This project is built for a different target:

> **HTML pages that feel like real presentation slides — dense, structured, reviewable, and ready for serious reporting.**

## What makes it different

Instead of generating HTML in one shot, this pipeline uses a staged workflow:

```text
Detailed page draft
-> blueprint generation
-> blueprint review
-> HTML generation
-> HTML review
-> final single-page HTML
```

This gives you:
- better layout stability
- clearer page hierarchy
- stronger PPT feel
- fewer "web page looking" outputs
- easier review and rework


## What this skill automates

This skill is meant to reduce the manual burden of preparing page drafts from scratch. It can help you:
- turn a rough presentation idea into page-by-page draft requirements
- generate the detailed markdown drafts needed for the pipeline
- run the pipeline automatically once the deck shape is clear
- keep the final HTML aligned with the intended reporting style

## Why not generate HTML in one shot?

Because one-shot generation often drifts in exactly the places that matter for presentation pages:
- layout hierarchy becomes unstable
- content blocks lose priority order
- slide density becomes too sparse or too web-like
- visual style drifts away from the original reporting intent

This repository treats slide generation more like **page construction** than raw prompting.

That is why it separates:
- structure planning
- structure review
- HTML building
- HTML review

## Best fit

Use this when you need:
- executive presentation pages
- strategy / reporting slides
- structured proposal pages
- high-density single-page HTML with strong visual hierarchy
- production-style page-by-page generation workflows

Not ideal if you only want:
- generic web pages
- landing pages
- lightweight modern UI cards
- casual single-shot mockups

## Quick value summary

- **Blueprint-first**: structure before HTML
- **Built-in review loops**: check quality before delivery
- **PPT-feel oriented**: optimized for serious presentation pages
- **Controller-friendly**: works with page-by-page draft workflows
- **OpenClaw-ready**: designed as a reusable production skill / pipeline

## What this skill helps you do

This skill is designed to help you go from a rough presentation need to a page-by-page production workflow.

It can help you:
- clarify the overall presentation goal
- turn rough ideas into page-level requirements
- generate or refine detailed markdown drafts page by page
- call the blueprint / review / HTML pipeline automatically
- keep the final output aligned with the original reporting intent

You do **not** need to prepare a perfect detailed draft before starting. A rough topic, audience, and desired outcome is enough to begin.

## Quick start

Typical workflow:

1. Describe the deck goal, audience, and page count
2. Let the skill help generate page-by-page detailed drafts
3. Run the pipeline page by page
4. Review blueprint output before HTML finalization
5. Deliver the reviewed final HTML pages

At minimum, the skill will try to clarify or produce:
- page number
- page title
- page goal
- previous / next page relation
- style requirements
- forbidden items
- core content
- hard rules
- output path

## Example use cases

This pipeline is especially useful for:
- leadership reporting decks
- strategy proposal pages
- technical architecture presentations
- project milestone reviews
- product planning / roadmap pages
- AI-assisted PPT-like HTML production systems

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

## Input style

The skill works best when it can start from a rough brief and then help fill in the page-level details.

Useful starting signals include:
- the overall topic
- target audience
- expected number of pages
- preferred tone / style
- any must-include or must-avoid elements

If page-level details are missing, the skill should help generate them first, then run the pipeline.

## Ideal workflow

1. Confirm the deck goal and audience with the user
2. Let the skill generate or refine page-by-page draft markdown
3. Run the pipeline page by page
4. Let blueprint / review / HTML / review happen automatically
5. Only intervene when the pipeline blocks or review fails
6. Deliver reviewed final page HTML files

## Preview

> Add screenshots / before-after comparisons here for better conversion.

Recommended assets:
- 1 full-page screenshot
- 1 zoomed-in detail screenshot
- 1 before/after comparison between generic HTML and PPT-style reviewed HTML

## Status

This project already contains the core workflow, prompts, validators, and controller-facing conventions needed for a strong first production system.

It is especially strong when the goal is:

> **produce extremely high-quality PPT-style HTML pages, not ordinary web pages**

## Positioning

If you want HTML that merely "looks modern," many tools can do that.

If you want HTML that feels like:
- a real presentation slide
- a serious report page
- a page a leader can review on screen

this pipeline is built for that job.

## Next improvements

Recommended next assets for stronger conversion:
- real screenshot gallery
- before / after comparisons
- one minimal example page draft
- one minimal generated output example
- short demo GIF or walkthrough video

---

# PPT HTML Pipeline 中文版

[返回 English](#ppt-html-pipeline)

把 **PPT 风格 HTML 页面生成** 从“一把梭直接出网页”改成一条更稳定的流水线：

**逐页详细需求稿 -> 施工图 -> 审核 -> HTML -> 审核 -> 最终单页 HTML**

这个仓库面向的不是普通网页生成，而是：

> **生成真正像正式汇报页、像演示页、像领导可直接看的单页 HTML。**

## 为什么会有这个项目

大多数 AI 生成的“HTML 幻灯片”最后仍然很像：
- 落地页
- 仪表盘
- 卡片网站
- 留白过多的现代网页 UI

而这个项目明确追求的是：
- 更强的页面层级
- 更成熟的 PPT 感
- 更适合投屏的字号与密度
- 更像正式汇报页的视觉语言
- 更少无意义留白
- 更低的网页感

## 它为什么不一样

它不是一把梭直接生成 HTML，而是走分阶段流程：

```text
逐页详细需求稿
-> 施工图生成
-> 施工图审核
-> HTML 生成
-> HTML 审核
-> 最终单页 HTML
```

这样做的好处是：
- 页面结构更稳
- 视觉重心更清楚
- PPT 感更强
- 更少生成出“像网页不像汇报页”的结果
- 更方便审核和返工

## 为什么不直接一把梭生成 HTML？

因为一把梭生成最容易在这些关键点上跑偏：
- 页面层级不稳
- 信息主次顺序被打乱
- 页面密度太稀或者太像网页
- 风格逐渐偏离原始汇报意图

这个仓库把页面生成当成一种**页面施工过程**，而不是一次性提示词输出。

所以它会明确拆开：
- 结构规划
- 结构审核
- HTML 构建
- HTML 审核

## 最适合什么场景

适合：
- 领导汇报页
- 战略方案页
- 项目 / 产品阶段汇报页
- 结构化提案页
- 高信息密度的单页展示
- 按页批量生产的正式汇报页面流程

不太适合：
- 普通网页
- 落地页
- 轻量卡片式现代 UI 页面
- 随手快速出一个网页草稿

## 一句话价值总结

- **先施工图，后 HTML**：先把结构定住
- **自带审核闭环**：不是只生成，还会审
- **明确追求 PPT 感**：不是泛泛的网页生成
- **适合逐页生产**：适合和详细页面草稿配合
- **适合 OpenClaw 工作流**：可以作为生产级 skill / pipeline 使用

## 这个 skill 会帮你做什么

这个 skill 的目标，是把一个粗略的汇报需求，逐步变成可以执行的逐页生产流程。

它可以帮你：
- 明确整套汇报的目标和对象
- 把粗略想法整理成逐页需求
- 生成或补全每页的详细 markdown 草稿
- 自动调用施工图 / 审核 / HTML 流水线
- 保持最终结果不偏离原始汇报意图

你**不需要**一开始就自己准备完美的详细需求稿；只要有一个大致主题、受众和目标，就可以先开始。

## 快速开始

典型使用方式：

1. 先说明整套汇报的目标、受众和页数
2. 让 skill 帮你生成或补全逐页详细草稿
3. 逐页运行流水线
4. 先审施工图，再进入最终 HTML
5. 输出审核后的最终页面

最低建议输入包括：
- 整体主题
- 目标受众
- 预计页数
- 期望风格
- 必须包含或必须避免的内容

## 示例场景

这条流水线特别适合：
- 领导汇报页面
- 战略方案页面
- 技术架构展示页
- 项目阶段总结页
- 产品规划 / 路线图页面
- AI 辅助 PPT 风 HTML 生产系统

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

## 输入风格

这个 skill 最适合先从粗略 brief 开始，再逐步补齐页级细节。

如果页面细节还不够完整，skill 会先帮助补齐，再进入流水线。

有用的起始信息包括：
- 整体主题
- 目标受众
- 预计页数
- 期望语气 / 风格
- 必须包含或必须避免的元素

## 理想使用方式

1. 先确认整套 PPT 结构
2. 让 skill 帮你生成或补全逐页详细草稿
3. 逐页运行流水线
4. 让施工图 / 审核 / HTML / 审核自动执行
5. 只有在阻塞或审核失败时才人工介入
6. 最终交付逐页审核后的 HTML

## 预览建议

> 后续建议在这里补截图 / before-after 对比图。

最值得补的素材：
- 1 张整页效果图
- 1 张局部细节图
- 1 张“普通 HTML vs PPT 风 HTML”对比图

## 当前定位

这个项目已经具备：
- 核心流程
- 提示词
- 校验器
- 面向主控的流程约定

如果你只是想做“看起来现代”的 HTML，很多工具都能做。

但如果你要的是：
- 真正像汇报页
- 真正像演示页
- 真正像可以拿来讲方案的页面

那这条流水线就是为这件事设计的。

## 下一步最值得补什么

如果你想让仓库更容易被理解、被转发、被 star，最值得继续补的是：
- 真实效果截图
- before / after 对比图
- 一份最小输入示例
- 一份最小输出示例
- 一个简短演示 GIF 或视频
