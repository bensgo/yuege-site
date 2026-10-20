# Hide Photos — EN-US App Store metadata audit and proposed copy

Date: 2026-10-20
App ID: 6812803369
Website: https://yuege.online/private-moments/

## Observed public listing (cached search, NOT verified against current App Store Connect)

- Current title seen: `Hide Photos: Secret Album`.
- Subtitle seen: `Lock Photos & Private Vault`.
- Publicly indexed description still refers to the product as `Private Moments` and older in-app purchase display names use that branding.
- Search output showed an older version, so it may be stale. Verify actual fields in App Store Connect before publishing.
- No prices or promotion codes are claimed here.

## Proposed fields (English US)

**App name** (max 30): Hide Photos: Secret Album

**Subtitle** (max 30): Lock Photos & Private Vault

**Promotional Text** (max 170; generally editable without submitting a new version):

Keep your private photos in an encrypted vault on your iPhone. Unlock with PIN or Face ID, use a private camera, and explore Decoy Vault. No account or ads.

**Description** (max 4,000; typically submitted with an editable app version):

Hide Photos is a private photo and video vault for iPhone, built for people who want a separate, encrypted space for personal memories.

Your vault photos and videos are encrypted on your device using AES-GCM. There's no account to create, no ads, and no developer-hosted cloud that stores your vault media.

PRIVATE PHOTO & VIDEO VAULT
• Import selected photos and videos into a protected local space.
• Unlock with a six-digit PIN or optional Face ID.
• Browse and organize private content into albums and folders.
• Automatically lock your vault when appropriate.

PRIVATE CAMERA & MOMENTS
• Capture photos and videos directly into the vault without first saving them to Apple Photos.
• Keep personal Moments with photos, videos and notes, or create text-only Moments.

MORE PRIVACY OPTIONS
• Optional Decoy Vault opens an alternative space with a separate PIN (Pro feature).
• Hide sensitive content in the app switcher.
• Create a user-controlled encrypted backup file for transferring your vault. Backup limits and other advanced features may require Pro.

IMPORTANT TO KNOW
Importing photos does not automatically delete originals from Apple Photos or iCloud Photos. Review and delete existing copies separately if that's what you want.

Hide Photos is free to download, with optional Pro in-app purchases. Features and offers may vary by region and app version.

Privacy Policy: https://yuege.online/private-moments/privacy/
Security: https://yuege.online/private-moments/security/
Terms of Use: https://www.apple.com/legal/internet-services/itunes/dev/stdeula/

## Required follow-up in App Store Connect

1. Check name and subtitle: retain current localized brand where correct.
2. Update EN-US description to remove misleading legacy `Private Moments` references. Confirm every feature against the live build before sending for review.
3. Check Promotional Text separately — it can generally be changed without a new app version.
4. Inspect *all* storefront languages and in-app purchase localizations for legacy names (`PrivateMoment`, `Private Moments`, `Photo Vault`) while retaining legitimate generic terms like “photo vault”.
5. Review screenshots and promotional graphics for expired lifetime giveaway claims or outdated price tags. Do not claim that Pro is free or has a fixed price across regions.
6. Confirm app-version metadata editability and review status; do not interrupt a submission simply to ship marketing changes.
7. Keep website messaging precise: the developer does not upload/store vault photos or videos, but the app may use limited product analytics. Imported originals in Photos/iCloud are not automatically deleted.

## Limits verified on draft

- App name: 25 / 30 characters
- Subtitle: 27 / 30 characters
- Promotional Text: 156 / 170 characters
- Description: 1569 / 4,000 characters

## References

- Apple App Store Connect documentation: https://developer.apple.com/help/app-store-connect/reference/app-information/platform-version-information/
- Apple guide to product pages: https://developer.apple.com/app-store/product-page/
