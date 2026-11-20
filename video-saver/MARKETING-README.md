# Vidkiva promotion website: deployment and attribution

## Status
- Site is intentionally static and works without analytics infrastructure.
- iOS download points to the verified product id `6829142265`.
- **Do not put a guessed Apple provider token in production**; by default links go directly to the store, with no Apple campaign parameters.
- Android button must remain unpublished until the actual Google Play production listing is live.
- No tracking cookies, user IDs, raw IP addresses, saved video URLs or browsing history are collected by this implementation.
- The site-level analytics endpoint is empty until you deploy and configure the optional first-party Worker.
- Page visuals are **illustrative CSS**, not forged app captures.

## Attribution convention
Share the landing page with these URL parameters:

| Field | Description | Example |
|---|---|---|
| `utm_source` | site/platform | reddit, youtube, tiktok, xiaohongshu |
| `utm_medium` | marketing channel | community, video, organic_social |
| `utm_campaign` | campaign / batch | launch_202611 |
| `utm_content` | creative ID | watch_later_01 |

Example:
`https://yuege.online/video-saver/?utm_source=reddit&utm_medium=community&utm_campaign=launch_202611&utm_content=watch_later_01`

Values are sanitized and stored as **first-touch values in sessionStorage** for the current tab; no cookie or third-party profile is created. The homepage and Press Kit preserve that attribution when navigating via marked links. The analytics counts are **events**, not unique people or installations.

## Activate official App Store campaign tracking
1. In App Store Connect → Analytics → Acquisition → Campaigns, generate a campaign link once.
2. Copy its **real** `pt` provider token.
3. Edit `video-saver/assets/marketing.js`, setting `CONFIG.appleProviderToken` to those digits.
4. The site then adds `pt`, `ct`, `mt=8` to outbound iOS links. `ct` derives from sanitized first-touch campaign/source/content and is subject to Apple reporting thresholds.
5. Verify navigation and campaign parameters before deploying. Apple reporting is delayed and not equivalent to verified installs per click.

## Activate first-party site EVENT counts (optional)
An example Cloudflare Worker lives at `video-saver/analytics-worker/worker.js`. Schema:
`video-saver/analytics-worker/schema.sql`.

1. Confirm actual hosting and DNS/Cloudflare account availability; this repository cannot infer them.
2. Create a D1 database, apply schema.sql, bind it as `MARKETING_DB`.
3. Deploy the Worker behind a valid HTTPS URL, ideally `https://yuege.online/video-saver/api/marketing/event`, but choose routing according to the existing hosting.
4. Add a Cloudflare rate limit/bot rule. Origin checks alone do **not** prevent forged requests. Counts are approximate.
5. Set `CONFIG.analyticsEndpoint` to the live endpoint. Verify POST returns 204 and the D1 aggregate increases.
6. Update/review the public Privacy Policy **before activating new analytics**. Document what is counted and its retention.
7. Configure a retention policy and validate real events vs bots. No per-user tracking is implemented.

Do not enable analytics by simply replacing the endpoint without deploying the Worker and updating privacy disclosures.

## QA
- English and Chinese landing pages load on mobile and desktop, with no 'Coming soon'.
- iOS button opens `https://apps.apple.com/app/id6829142265` when provider token is blank.
- Invalid/overlong UTM values are ignored, and there is no open redirect from any user input.
- Press Kit only lists media that exists; when screenshots and a recording are produced, replace the 'request originals' blocks with real downloads.
- Accessibility checks: keyboard focus, headings, alt for *real* screenshots, reduced-motion behavior.
- Static HTML links: all Press Kit, Terms, Privacy, App Store, and home URLs resolve.
- Add public pages to sitemap and check canonical/OG data.
- No website PR merge/deploy or Store submission is automatic.

## Assets to import from app repository
The authentic 1024×1024 app icon has already been copied to `video-saver/assets/icon-1024.png` and can be downloaded from the Press Kit. Only screenshot/recording/ZIP imports remain.
See `bensgo/video_download` marketing asset checklist and tooling. Generate high-resolution raw captures, verify release version, and export assets. After verifying ownership/accuracy, commit icon, real screenshots and ZIP into `video-saver/assets/` in a separate media PR. Do not use CSS illustration as a press screenshot.

## Known manual steps
Apple provider token; Android Play URL after live release; optional Cloudflare Worker/D1/routing; real app-recorded demo and screenshots; privacy/legal verification; review and merge/deploy.
