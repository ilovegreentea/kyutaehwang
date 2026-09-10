# KyuTae Hwang website — CMS-ready version

This version keeps GitHub Pages for hosting and uses Pages CMS as the no-code editing interface.

## Repository structure

```text
index.html
data.json
.pages.yml
admin/
  index.html
media/
  images/
  files/
    KyuTae_Hwang_CV.docx
```

## First-time installation

1. Open the `ilovegreentea/kyutaehwang` repository on GitHub.
2. Upload **the contents of this folder** to the repository root.
   - `.pages.yml` must be in the repository root.
   - `admin/index.html` must remain inside the `admin` folder.
   - `data.json` and `index.html` must be in the repository root.
3. Commit the files to the branch used by GitHub Pages (normally `main`).
4. Confirm GitHub Pages is configured for that same branch and root folder.
5. Open:
   - Public site: `https://ilovegreentea.github.io/kyutaehwang/`
   - Admin shortcut: `https://ilovegreentea.github.io/kyutaehwang/admin/`
6. From the admin shortcut, open Pages CMS.
7. Sign in with GitHub and install/authorize the Pages CMS GitHub App for the repository.
8. Select `ilovegreentea/kyutaehwang` and the `main` branch.

## What can be edited without code

- Name, email, location, position
- Hero introduction
- Profile photo
- About section
- Research cards, tags, and optional card images
- Selected work and optional feature image
- Career/trajectory entries
- Presentations
- Toolkit and scientific interests
- GEO/Zenodo/resource links
- Photo gallery
- CV document

## Image and file uploads

Pages CMS stores uploads directly in the GitHub repository:

- Images: `media/images/`
- Documents: `media/files/`

The website reads those paths from `data.json`, so uploaded media appears on the public site after GitHub Pages republishes.

## Security

The `/admin/` shortcut page itself is public because GitHub Pages is static hosting. Actual editing requires GitHub authentication and repository authorization in Pages CMS.

Do not store a GitHub personal access token in the repository or in `index.html`.
