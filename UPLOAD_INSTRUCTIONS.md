# Design controls + CV sync patch

Upload the CONTENTS of this folder to the repository root.

## Files to overwrite/add

- `index.html` — overwrite the current root file
- `.pages.yml` — overwrite the current root file
- `design.json` — new file in the root
- `.github/workflows/cv-sync.yml` — new workflow
- `scripts/sync_cv.py` — new parser

Do not overwrite or delete your current `data.json`.
Do not replace your photos or CV while installing this patch.

## Font-size controls

In Pages CMS, open **Design Settings**.

Recommended ranges:

- Overall text size: `0.90`–`1.10`
- Main name size: `0.85`–`1.10`
- Section heading size: `0.90`–`1.10`

`1.00` means the current redesign size.

## CV → website semi-automatic sync

1. In Pages CMS, update **Website Content → Hero → CV file** with a `.docx` CV.
2. Save it.
3. Click the repository-level action **Sync website from CV**.
4. Confirm **Create review PR**.
5. GitHub Actions parses the CV and opens a Pull Request.
6. Open the Pull Request and review the `data.json` diff.
7. Merge only if the suggested updates are correct.

The sync intentionally reads only structured public information:

- email
- current manuscript citation/status/year
- presentations
- computational toolkit
- GEO / Zenodo identifiers
- matching trajectory date ranges

It intentionally ignores phone number, references, reference emails, leadership/military service, grants, academic service, and manually curated narrative text.

## One-time GitHub setting if PR creation is blocked

If the workflow can push the review branch but cannot open a Pull Request:

GitHub repository → Settings → Actions → General → Workflow permissions

Enable **Allow GitHub Actions to create and approve pull requests** and save.

Then run **Sync website from CV** again.

## Current parser format

The included parser supports `.docx` CV files. PDF can still be used as the downloadable CV, but automatic CV parsing is not enabled for PDF in this patch.
