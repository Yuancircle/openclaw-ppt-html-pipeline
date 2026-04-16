# PPT HTML Pipeline

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
