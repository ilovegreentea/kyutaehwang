# Squarespace-lite CMS controls

This patch keeps GitHub Pages + Pages CMS, but moves much more visual control into **Website Content**.

## Upload / overwrite

Upload these files to the repository root, preserving the folder paths:

- `.pages.yml` — overwrite
- `index.html` — overwrite
- `.github/workflows/cv-sync.yml` — keep/overwrite
- `scripts/sync_cv.py` — keep/overwrite

**Do not overwrite `data.json`.**
**Do not delete your `CNAME` file.**
**Do not replace your photos or CV while installing this patch.**

## What is editable in Website Content

### Site Design & Layout
- Color preset
- Custom accent/background/card/text/border colors
- Page width
- Section spacing
- Card corner style
- Body font and heading font
- Hero layout
- Sticky navigation
- Animations
- Overall text size and navigation text size
- Section order and section visibility

### Hero
- Existing text/photo/CV/email
- Main button text and destination
- CV button text
- Email button text
- Floating profile card on/off
- Name size
- Intro size

### Each content section
The relevant section now contains its own labels, headings, font sizes, display limits, image toggles, and layout controls where appropriate.

Examples:
- Research: 2/3 columns, show/hide images, max cards, heading/card font sizes
- Selected Work: show/hide feature image, heading/title/body font sizes
- Presentations: max items and font sizes
- Data & Methods: card columns, max resources, panel titles and font sizes
- Photos: max photos, captions on/off, heading/caption size
- Contact: navigation label, button labels, font sizes

## Section ordering

Go to:

**Website Content → Site Design & Layout → Section order & visibility**

Drag the section items to reorder them. Turn **Show section** off to hide one.

The hero remains the top section.

## Defaults and backward compatibility

Existing `data.json` content is preserved.

New fields have defaults in Pages CMS. Older font values stored under the previous `design` object are still used as fallbacks until you save the new per-section controls.

## CV sync

CV → website sync is unchanged. It preserves all new visual settings because the parser only updates selected structured content fields.
