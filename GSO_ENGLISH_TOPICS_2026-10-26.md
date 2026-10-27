# Hide Photos English SEO/GSO topics — 2026-10-26

Status: implemented on an isolated branch; not merged or deployed. URLs below are intended canonical URLs; new pages are not live until approved and published.

## Repository inspection and scope

Baseline: `392ab19` on `main`. Static HTML site with shared `private-moments/assets/site.css`; no package.json, build pipeline, project test suite or AGENTS.md in this checkout. No App code is included or modified. No LumoKeep or other product files changed.

Four existing URLs already matched the requested topics and have been expanded in place. The existing no-cloud page incorrectly targeted “Best Offline Photo Vault”; it now focuses on accounts and upload boundaries. A distinct offline selection/test guide and a private-camera guide are new. Existing translated routes and hreflang clusters remain intact. The two new English-only articles do not advertise nonexistent translations.

The six articles each include a direct answer, practical steps, FAQs, developer disclosure, related topics and the App Store entry. They link to all five other topic pages and back to the product homepage; the homepage and guide index link to all six. Existing product screenshots are reused; no competitor images, wording or distinctive design were imported. All six use self-referencing canonical, Open Graph/Twitter cards, Article and BreadcrumbList JSON-LD. No Review, Rating, AggregateRating or FAQPage schema was added, and no search rich-result eligibility is claimed.

## Article metadata and original monitoring numbers

Question numbers use the unchanged fixed 18-question list from the existing “Hide Photos 每周 GSO 监测” task. They map search intent, not measured rankings or ChatGPT recommendation results.

| Canonical URL | SEO Title / H1 | Meta Description | Monitoring question IDs |
| --- | --- | --- | --- |
| https://yuege.online/private-moments/guide/hidden-album-vs-encrypted-vault/ | iPhone Hidden Album vs Encrypted Photo Vault | Compare Apple’s Hidden album with an encrypted iPhone photo vault: separate PINs, local storage, iCloud behavior, backups, and which option fits you. | Q08, Q09, Q16 |
| https://yuege.online/private-moments/guide/offline-photo-vault-iphone/ | Best Offline Photo Vault for iPhone: How to Choose | Choose an offline iPhone photo vault using a practical checklist for local encryption, separate PINs, ads, backups, and an airplane-mode test. | Q01, Q02, Q03, Q06, Q11, Q18 |
| https://yuege.online/private-moments/guide/transfer-encrypted-photo-vault-new-iphone/ | How to Back Up and Restore Encrypted Photos on iPhone | Back up an encrypted iPhone photo vault, keep the correct PIN, restore into a destination vault, and verify your files before erasing the old phone. | Q13, Q14 |
| https://yuege.online/private-moments/guide/decoy-pin-photo-vault-iphone/ | Decoy Vault and Fake PIN for iPhone: Setup and Limits | Learn how a decoy vault and fake PIN work on iPhone, set up separate content, check Face ID behavior, and back up each vault without mixing libraries. | Q07, Q16 |
| https://yuege.online/private-moments/guide/private-camera-encrypted-storage/ | Private Camera with Encrypted Storage on iPhone | Take private photos and videos straight into an encrypted iPhone vault instead of Apple Photos. Learn how to test capture, access, sharing, and backup. | Q10, Q15 |
| https://yuege.online/private-moments/guide/private-photo-vault-without-cloud/ | Photo Vault Without Account or Cloud Uploads on iPhone | Keep private photos in a local iPhone vault without creating an account or uploading media to developer servers. Understand originals, analytics, and backups. | Q04, Q05, Q12, Q18 |

## Changed files

- Existing article pages: `private-moments/guide/hidden-album-vs-encrypted-vault/index.html`, `transfer-encrypted-photo-vault-new-iphone/index.html`, `decoy-pin-photo-vault-iphone/index.html`, `private-photo-vault-without-cloud/index.html`.
- New article pages: `private-moments/guide/offline-photo-vault-iphone/index.html`, `private-camera-encrypted-storage/index.html`.
- Entry points: `private-moments/index.html`, `private-moments/guide/index.html`.
- `private-moments/security/index.html`: one stale sentence said restoring replaced the vault. Updated to the confirmed merge workflow documented by the existing restore screenshot and guide.
- `sitemap.xml`: two new canonical URLs; lastmod updated only for edited pages. All other product/locale entries preserved.
- `scripts/check_hide_photos_topics.py`: dependency-free, repeatable static checks.
- `GSO_ENGLISH_TOPICS_2026-10-26.json`: machine-readable metadata/monitoring mapping.
- This delivery report.

## Accuracy and brand audit

Feature claims are bounded by the existing product homepage, privacy/security pages, release JSON and actual app screenshots already in this repository. The app binary was not independently retested and was not changed. Preserved important details from those materials: backups cover the current vault only; restore validates the file/PIN then merges missing items after confirmation; up to three decoys have separate credentials; Face ID unlock and Face ID PIN recovery are unavailable while a decoy is enabled. Free download is distinguished from optional Pro features, with no invented price or free-lifetime promotion.

The no-cloud and offline guides explicitly separate vault-media uploads from Firebase Analytics, cloud-only source downloads, App Store operations, user-selected backup destinations and iOS device backup settings. No claim that all app operations are network-free. No invented certification, benchmark, user count, review or security audit.

Case-insensitive scan of `private-moments` HTML/JSON found no current product description branded “Private Moments”. `PrivateMoment` remains only as a historical `SoftwareApplication.alternateName` on the English homepage. “Your private moments stay yours” is an ordinary slogan, not the product name. Historical repository release documents and the indexed `/private-moments/` route were retained.

## References reviewed

- Apple Hidden album: https://support.apple.com/en-us/104987 — authentication on supported iOS, hiding from view and iCloud Photos behavior. Kept the article neutral; no claim that the Hidden album is unencrypted or inherently unsafe.
- Apple current Photos guide: https://support.apple.com/guide/iphone/delete-or-hide-photos-and-videos-iphb4defbde9/ios
- Tuckaway: https://tuckawayapp.com/ — feature-led answers about storage/access/capture.
- Obscura Photo Vault: https://obscura-vault.com/ — question-led FAQ and guide organization.
- York Vault: https://yorkvault.com/features/encrypted-backup — task-led backup/recovery explanations.

Competitor materials informed topic organization only. These articles use original wording and the existing Yuege design; they do not reproduce competitor claims or rank apps without independent evidence.

## Validation

- `python scripts/check_hide_photos_topics.py`: PASS.
- Parsed **159 HTML documents** and **159 Sitemap URLs**. No duplicate indexable canonical destinations; every Sitemap URL has a local target.
- **4,425 full-site local link/asset/anchor references** checked, **0 broken**. Includes 332 references on the six articles and two entry points. Other products were read for validation only.
- Six articles: unique titles/descriptions, one H1 and canonical each, matching OG URLs, valid Article/Breadcrumb JSON-LD, tutorials, FAQs, disclosure, mutual links and App Store links: PASS.
- Local HTTP server: all six topic routes returned **200**.
- External destinations in these articles: App Store numeric ID URL returned **200** after redirect to the correct app; Apple support destination returned **200**. `mailto:` is not an HTTP endpoint.
- `git diff --check`: PASS.
- Build: **not applicable**; the repository serves static HTML without a build command.
- Mobile: existing responsive styles reused; the comparison table now has a contained horizontal scroll region. **Visual browser QA not completed**: no Chromium binary was installed, and the browser download returned an invalid/truncated archive. Do not interpret static checks as screenshot or real-device validation.
- No production deploy, merge, Search Console submission or actual ChatGPT 18-question retest performed. Canonical URLs are destinations after approval, not proof of current live deployment or indexing.
