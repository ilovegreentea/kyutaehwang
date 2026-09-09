# KyuTae Hwang — Interactive GitHub Pages site

## Files
- `index.html`: public website
- `data.json`: editable site content
- `admin/index.html`: browser-based GitHub editor
- `KyuTae_Hwang_CV.docx`: CV

## Install
Upload/replace these files in the root of the `ilovegreentea/kyutaehwang` repository:

```text
index.html
data.json
KyuTae_Hwang_CV.docx
admin/index.html
```

After GitHub Pages publishes, the editor will be available at:

`https://ilovegreentea.github.io/kyutaehwang/admin/`

## GitHub token
Create a fine-grained personal access token restricted to the `kyutaehwang` repository.

Required repository permission:
- Contents: Read and write

The editor does not save the token to localStorage, cookies, or the repository. You enter it each browser session.

## Workflow
1. Open `/admin/`.
2. Enter your GitHub token.
3. Click **Load from GitHub**.
4. Edit fields.
5. Click **Commit changes to GitHub**.
6. GitHub Pages redeploys from the new `data.json`.

## Important
This admin page is public because it is hosted by GitHub Pages, but editing still requires a valid GitHub token with repository write permission. Never hard-code the token into `admin/index.html`.
