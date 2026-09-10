# Upload these files to the repository root

This patch intentionally DOES NOT include `data.json`, so it will not overwrite your current website content.

Upload/overwrite:

- `.pages.yml` -> repository root
- `index.html` -> repository root
- `admin/index.html` -> `admin/`
- `media/images/README.txt` -> `media/images/`

After committing:

1. Confirm the root shows `.pages.yml`.
2. Open https://app.pagescms.org/
3. Sign in with GitHub.
4. Open `ilovegreentea/kyutaehwang`.
5. Edit `Website Content`.
6. Upload a Profile photo under Hero and Save.
7. Wait for GitHub Pages to redeploy, then hard-refresh the public site.

If your computer hides `.pages.yml`, use `UPLOAD_AS_DOT_PAGES_YML.txt` only as a backup:
create a new GitHub file named `.pages.yml` and paste everything after the first three instruction lines.
