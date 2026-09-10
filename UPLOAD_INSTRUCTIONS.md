# Website Content font controls patch

This version moves all typography controls into **Website Content**.

## Upload / overwrite

Upload these paths to the repository root:

- `index.html` — overwrite
- `.pages.yml` — overwrite
- `.github/workflows/cv-sync.yml` — overwrite/add if needed
- `scripts/sync_cv.py` — overwrite/add if needed

Do NOT overwrite `data.json`.

The old `design.json` can stay in the repository. It is only used as a fallback until you save values inside Website Content.

## Where to change font sizes

Pages CMS → Website Content → Display / Font Sizes

Each value is a scale:

- `1.00` = default
- `0.90` = about 10% smaller
- `1.10` = about 10% larger

You can independently adjust:

- overall text
- navigation
- hero name and intro
- About heading/body
- Research heading/card title/card body
- Selected Work heading/title/body
- Trajectory heading/title/body
- Presentations heading/title/meta
- Methods heading/panel title/list
- Photos heading/caption
- Contact heading/body

Blank fields behave as `1.00`, so you do not need to fill every setting.

## CV sync

The CV → website review workflow is unchanged and still preserves the `design` object in `data.json`.
