# Batch Example

## Existing workspace example

A concrete batch controller already exists here:
- `/root/.openclaw/workspace/tools/batch_build_salon_04_10_and_bundle.py`

That script demonstrates how to:
1. define page task packages in Python
2. write one markdown task file per page
3. call `ppt_page_pipeline.py` for each page
4. skip already completed pages
5. collect per-page results
6. bundle many finished pages into one HTML

## Recommended batch pattern

For each page, keep a separate work directory, for example:
- `tmp/ppt-pipeline/page-04`
- `tmp/ppt-pipeline/page-05`
- `tmp/ppt-pipeline/page-06`

Recommended outputs:
- page-by-page detailed requirement drafts in a dedicated requirements directory
- final page HTML files in a dedicated html/output directory
- logs and stage artifacts in `tmp/ppt-pipeline/<page>/`

## Recommended orchestration pattern

A good batch controller should do this in order:
1. read one detailed requirement draft per page
2. call `ppt_page_pipeline.py` for each page independently
3. skip already finished pages when allowed
4. keep a per-page result/state summary
5. only surface pages that need intervention

## Controller responsibilities

The batch controller should own:
- page discovery
- per-page input path mapping
- output path assignment
- isolated work-dir assignment
- skip / resume / retry policy
- final status collection

The controller should not join the normal internal pipeline stages when those stages are passing cleanly. Its job is orchestration and exception surfacing.

## Bundle pattern

If the user wants a combined preview file, a practical pattern is:
- read each finished page HTML
- escape it into `iframe srcdoc`
- render one wrapper HTML that shows all pages vertically

This keeps each page style isolated enough for preview while still shipping a single file.

## Known failure modes

### 1. Review verdict parsing drift
If review text changes formatting, inspect `validators.py`, especially `parse_review_verdict()`.

### 2. Weak detailed requirement draft -> weak blueprint
If the blueprint uses placeholders like `...`, the root cause is usually the detailed requirement draft being under-specified.
Fix the detailed requirement draft first.

### 3. HTML output polluted by explanation text
If the model returns markdown fences or explanation text mixed into HTML, patch extraction / cleanup rather than manually trimming every page.

### 4. Controller interferes too early
If the controller keeps inserting manual steps even though parse/review/build stages are passing, the orchestration layer is too heavy.
The controller should only step in when a stage is blocked, fails, or review does not pass.

## Good default

Prefer strengthening the controller, detailed requirement drafts, prompt assets, and validators so future agents can reuse the same path reliably, instead of hand-fixing each page one by one.
