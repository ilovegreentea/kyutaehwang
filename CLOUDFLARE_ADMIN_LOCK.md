# Protecting /admin with Cloudflare Access

This package hardens the visual editor, but the actual login gate is enforced by Cloudflare Access.

## What changes in this build

- The GitHub write token is stored in `sessionStorage`, not `localStorage`.
- Closing the browser tab removes the token automatically.
- The admin page includes `noindex,nofollow,noarchive`.
- The top bar includes an **관리자 로그아웃** button.
- When Cloudflare Access is active, that button signs out through `/cdn-cgi/access/logout`.

## Important timing

Do not change DNS while GitHub Pages is still waiting to issue the HTTPS certificate for `kyutaehwang.com`.

First wait until GitHub Settings → Pages shows that the certificate is issued and **Enforce HTTPS** can be enabled. Turn that on and confirm `https://kyutaehwang.com` works normally.

## Cloudflare Access setup

1. Create or sign in to a Cloudflare account.
2. Add `kyutaehwang.com` as a Cloudflare zone.
3. Copy every existing DNS record from Squarespace to Cloudflare before changing nameservers.
   - Keep the four GitHub Pages A records for `@`.
   - Keep the `www` CNAME pointing to `ilovegreentea.github.io`.
   - Keep all existing MX/TXT verification and email records.
4. In Squarespace Domains, change the domain nameservers to the two nameservers Cloudflare gives you.
5. After Cloudflare reports the zone as active, proxy the web records through Cloudflare.
6. Open Zero Trust → Access controls → Applications.
7. Create a **Self-hosted and private** application.
8. Add public hostname:
   - Domain: `kyutaehwang.com`
   - Path: `/admin/*`
9. Create an **Allow** policy for only your identity.
   - Simplest option for a new Zero Trust account: Cloudflare account member.
   - Alternative: enable One-time PIN and allow only your exact email address.
10. Leave all other users denied. Access applications are deny-by-default.
11. Visit `https://kyutaehwang.com/admin/` in a private browser window to verify that login is required.

## Result

Public website:
`https://kyutaehwang.com/`
→ remains public.

Admin editor:
`https://kyutaehwang.com/admin/`
→ Cloudflare login required.

The GitHub token is still required for saving because Cloudflare Access authenticates the person opening the editor; it does not grant GitHub repository write permission.
