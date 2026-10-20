# Hide Photos — GSO/SEO release verification (2026-10-20)

This checklist separates **repository changes** from **production verification**. A merged PR is not proof that the public site is reachable or indexed.

## Implemented in this PR

- Standardized the displayed app name to **Hide Photos** across the English, Japanese, and Simplified Chinese product pages, guides, legal and support pages, and the parent landing page. Historical app-name aliases remain only in `SoftwareApplication.alternateName` to help with previous-name discovery.
- Kept existing `/private-moments/` URLs, canonical links and hreflang destinations so indexed URLs do not change.
- Normalized App Store links for app ID `6812803369` to numeric-ID URLs, preserving country codes.
- Added English and Simplified Chinese `SoftwareApplication` JSON-LD and corrected the Japanese software application's name. Offers with price `0` mean **free app download**, not free Pro; optional in-app purchases are disclosed.
- Explicitly allowlisted `OAI-SearchBot` in `robots.txt` while preserving access for regular crawlers.
- Updated `sitemap.xml` lastmod for edited pages.

## Production checks — must run AFTER the PR is merged/deployed

1. DNS: `dig +short yuege.online A`, `dig +short yuege.online AAAA`, `dig +short www.yuege.online CNAME`. Compare with GitHub Pages domain settings. Do not assume which records exist before checking.
2. TLS and HTTP: `curl -Iv https://yuege.online/private-moments/` and `curl -sSIL https://yuege.online/private-moments/`; verify a valid certificate, final 200 response, and no unexpected login/challenge/redirect.
3. Robots: `curl -fsSL https://yuege.online/robots.txt` should explicitly allow `OAI-SearchBot`. Also use `curl -sSIL -A 'OAI-SearchBot' https://yuege.online/private-moments/` to spot obvious user-agent blocking. A successful fake-UA request does **not** prove actual OpenAI crawler IPs are accepted.
4. Sitemap: `curl -fsSL https://yuege.online/sitemap.xml`; validate XML and open the listed EN/JA/zh-CN URLs.
5. Indexability: inspect the final HTML to confirm each page has its self-referencing canonical and no `noindex`/blocked `X-Robots-Tag`. Check `hreflang` and confirm JSON-LD matches visible copy.
6. Search Console / Bing Webmaster Tools: run URL Inspection / request indexing for `https://yuege.online/private-moments/`, `/ja/`, `/zh-CN/` after deployment. Monitor coverage and impressions; no guarantee of indexing or ChatGPT citation.

## Apple App Store Connect — manual action required

There is no App Store Connect editing action used in this change. Check all storefront metadata for `PrivateMoment`, `Private Moments`, and branded `Photo Vault` references (title, subtitle, description, promotional text, screenshots, localization). Use the live App Store listing for exact current availability and in-app purchase pricing; do not imply the free download includes Pro.

Suggested first sentence (English, confirm against shipping features before publishing):

> Hide Photos is an offline private photo vault for iPhone with local AES-GCM encryption, a six-digit PIN, optional Face ID, and a decoy vault. No account required and no ads. The app is free to download, with optional Pro purchases.

Privacy nuance: vault media is not uploaded to the developer's server. Imported originals can remain in Apple Photos/iCloud Photos unless the user removes them separately. Do not claim that *all* app data or analytics never leaves the device.

## Open items / limitations

- Production DNS/HTTPS/live user-agent responses were not verifiable in the editing environment.
- An allowlisted `robots.txt` makes crawling possible, not guaranteed. A CDN/WAF can still block published crawler IPs.
- Site copy does not itself change App Store Connect metadata, app binary, subscription prices, or app availability.
