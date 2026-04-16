# PPT HTML Pipeline

[English](#ppt-html-pipeline) | [中文](#ppt-html-pipeline-中文版)

Build **presentation-grade PPT-style HTML slides** with a **blueprint -> review -> HTML -> review** workflow.

Designed for serious slide pages, not generic landing pages or dashboard-like web UI.

## Why this exists

Most AI-generated "HTML slides" still look like web pages. This project focuses on HTML that feels like a real presentation slide: dense, structured, reviewable, and ready for reporting.

## What it does

This pipeline helps you:
- turn a rough presentation idea into page-by-page draft requirements
- generate or refine the detailed markdown drafts needed for the workflow
- run blueprint / review / HTML / review automatically
- keep the final output aligned with the original reporting intent

## Why not one-shot generation?

One-shot HTML generation often drifts in layout hierarchy, content priority, density, and style. This repository treats slide generation more like **page construction** than raw prompting.

## Best fit

Use this when you need:
- executive presentation pages
- strategy / reporting slides
- structured proposal pages
- high-density single-page HTML with strong visual hierarchy
- production-style page-by-page generation workflows

Not ideal for:
- generic web pages
- landing pages
- lightweight modern UI cards
- casual single-shot mockups

## Quick start

1. Describe the deck goal, audience, page count, and style.
2. Let the skill help generate or refine page-by-page drafts.
3. Run the pipeline page by page.
4. Review blueprint output before HTML finalization.
5. Deliver the reviewed final HTML pages.

## What this skill automates

- rough idea -> page-level requirements
- page drafts -> pipeline execution
- reporting intent -> reviewed final HTML

## Example use cases

- leadership reporting decks
- strategy proposal pages
- technical architecture presentations
- project milestone reviews
- product planning / roadmap pages

## Optional assets to add later

- screenshot gallery
- before / after comparisons
- minimal example page draft
- minimal generated output example
- short demo GIF or walkthrough video

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

## 中文版

把 **PPT 风格 HTML 页面生成** 从“一把梭直接出网页”改成更稳定的流水线：

**逐页详细需求稿 -> 施工图 -> 审核 -> HTML -> 审核 -> 最终单页 HTML**

这个 skill 的作用是：
- 把粗略汇报需求补成逐页草稿
- 自动调用施工图 / 审核 / HTML 流水线
- 保持最终结果像正式汇报页，而不是普通网页

## 为什么不一样

它把页面生成当成**页面施工过程**，不是一次性提示词输出。这样更稳，也更像正式汇报页。

## 最适合什么场景

- 领导汇报页
- 战略方案页
- 项目 / 产品阶段汇报页
- 结构化提案页
- 高信息密度单页展示

## 输入建议

只要先给出：
- 整体主题
- 目标受众
- 预计页数
- 期望风格
- 必须包含 / 必须避免的元素

skill 就可以先帮你补齐逐页草稿，再跑流水线。
