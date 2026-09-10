# Easy Visual Editor — installation

This version is designed for non-technical editing.

## Upload these files

Upload the contents of this ZIP to the repository root:

- `index.html` — overwrite
- `.pages.yml` — overwrite
- `admin/index.html` — overwrite/add
- `admin/config.js` — add
- `.github/workflows/cv-sync.yml` — keep/overwrite
- `scripts/sync_cv.py` — keep/overwrite

Do **not** overwrite or delete:

- `data.json`
- `CNAME`
- `media/`
- your existing photos
- your existing CV

## New editor

After GitHub Pages deploys, open:

`https://kyutaehwang.com/admin/`

The editor loads the current `data.json` automatically.

### Editing

- Use the left menu to choose a section.
- Font-size sliders live inside each section.
- Drag a slider and the live preview changes immediately.
- Click a `+ Add photo` box to select an image.
- Add/delete Research cards, timeline items, presentations, resources, and gallery photos.
- Drag section rows under `Layout & Colors` to reorder page sections.
- Click `Save website` once when finished.

## Why font sizing is different now

The previous implementation multiplied a global scale by section scales. Small values could compound and make text unexpectedly tiny.

This version uses direct pixel values per section and keeps the browser root size at 16px.

Default values:

- Hero name: 112px
- Hero introduction: 19px
- Section headings: 58px
- About body: 18px
- Research card title/body: 20px / 16px
- Selected Work title/body: 48px / 16px
- Trajectory title/body: 18px / 16px
- Presentation title/meta: 16px / 14px
- Methods panel/list: 19px / 16px
- Gallery caption: 14px
- Contact heading/body: 64px / 17px

Old `overallFontScale`, `nameScale`, `headingScale`, and similar values are ignored by the new website renderer.

## GitHub connection — one-time setup per browser

The editor can preview changes without credentials.

To save changes, click `GitHub 연결` or `Save website` and paste a **fine-grained personal access token**.

Recommended token permissions:

1. Repository access: **Only select repositories**
2. Select: `ilovegreentea/kyutaehwang`
3. Repository permissions → **Contents: Read and write**
4. No other repository permissions are required for normal visual-editor saving.

The token is stored only in that browser's `localStorage`. It is not written to the repository or `data.json`.

For a shared/public computer, click **GitHub 연결 → 연결 해제** after editing.

## Pages CMS

Pages CMS remains available as a backup/advanced editor. Its native numeric field is a normal number input, not a draggable range control, so the new `/admin/` page is the recommended day-to-day editor.

## CV sync

The existing CV sync workflow is preserved. Use the previous Pages CMS/GitHub Actions workflow when you want to generate structured update suggestions from a DOCX CV.
