/**
 * Publish a Google Business Profile post to one branch.
 *
 * Google's profile panel on the search page renders its editors inside iframes that go stale
 * between clicks — typing into them lands in the Google search box instead. The standalone
 * composer URL below is the same editor as a top-level page, which behaves.
 *
 * Needs a Chrome already signed in to the Business Profile account, started with a dedicated
 * profile directory so the login survives:
 *
 *   "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
 *     --remote-debugging-port=9333 --user-data-dir=/tmp/uz-chrome
 *
 * Usage (playwright-core must be installed wherever you run this):
 *   POST_TEXT="..." node scripts/gbp-post.mjs <locationId> [imagePath]
 *
 * Location IDs come from the profile URL in Business Profile Manager; they are recorded in
 * ads/gbp-audit-2026-09-17.md, which is deliberately untracked.
 */
import { chromium } from 'playwright-core'

const [locationId, imagePath] = process.argv.slice(2)
const text = process.env.POST_TEXT

if (!locationId || !text) {
  console.error('usage: POST_TEXT="..." node scripts/gbp-post.mjs <locationId> [imagePath]')
  process.exit(1)
}

const browser = await chromium.connectOverCDP(process.env.CDP_URL || 'http://localhost:9333')
const page = await browser.contexts()[0].newPage()

await page.goto(`https://www.google.com/local/business/${locationId}/promote/updates/add?hl=en`, {
  waitUntil: 'domcontentloaded',
  timeout: 45000,
})
await page.waitForTimeout(9000)

const description = page.locator('textarea').first()
await description.click()
await page.keyboard.insertText(text)
await page.waitForTimeout(2000)

const typed = await description.inputValue()
if (typed.length < text.length) {
  console.error(`only ${typed.length} of ${text.length} characters landed — aborting rather than posting a truncated update`)
  process.exit(1)
}
console.log(`[gbp-post] ${locationId}: typed ${typed.length} characters`)

if (imagePath) {
  const chooser = page.waitForEvent('filechooser', { timeout: 20000 }).catch(() => null)
  await page.getByRole('button', { name: /Select images and videos/i }).click({ timeout: 10000 })
  const fileChooser = await chooser
  if (!fileChooser) {
    console.error('[gbp-post] no file chooser appeared — posting without the photo')
  } else {
    await fileChooser.setFiles(imagePath)
    // the upload has no completion signal we can read; the Post button stays enabled throughout
    await page.waitForTimeout(18000)
    console.log(`[gbp-post] ${locationId}: attached ${imagePath}`)
  }
}

await page.getByRole('button', { name: /^Post$/ }).click({ timeout: 10000 })
await page.waitForTimeout(16000)

// on success Google redirects to /promote/updates/copy/<postId> offering to copy the post to the
// other profiles on the account — we always want branch-specific copy, so we stop here
const posted = /\/promote\/updates\/copy\//.test(page.url())
console.log(`[gbp-post] ${locationId}: ${posted ? 'published' : `UNCONFIRMED — landed on ${page.url()}`}`)

await page.close()
await browser.close().catch(() => {})
process.exit(posted ? 0 : 1)
