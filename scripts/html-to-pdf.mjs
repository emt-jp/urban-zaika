/**
 * Print a local HTML file to PDF through the CDP Chrome.
 *
 * ReportLab cannot shape Urdu or Bengali, and our flyers carry both. Chrome can, so anything
 * print-bound that needs real typography is authored as HTML with an @page rule and rendered
 * here. Page size and margins come from the document's own CSS.
 *
 *   node scripts/html-to-pdf.mjs marketing/flyers/shop-flyer-kita-ku.html out.pdf
 *
 * Needs the debug Chrome described in scripts/gbp-post.mjs, and playwright-core resolvable from
 * wherever this is run.
 */
import { chromium } from 'playwright-core'
import { pathToFileURL } from 'node:url'
import { resolve } from 'node:path'
import { writeFileSync } from 'node:fs'

const [input, output] = process.argv.slice(2)
if (!input || !output) {
  console.error('usage: node scripts/html-to-pdf.mjs <input.html> <output.pdf>')
  process.exit(1)
}

const browser = await chromium.connectOverCDP(process.env.CDP_URL || 'http://localhost:9333')
const page = await browser.contexts()[0].newPage()

await page.goto(pathToFileURL(resolve(input)).href, { waitUntil: 'load', timeout: 30000 })
// webfonts decide the line breaks; printing before they land gives a different document
await page.evaluate(() => document.fonts.ready)
await page.waitForTimeout(1200)

const cdp = await page.context().newCDPSession(page)
const { data } = await cdp.send('Page.printToPDF', {
  printBackground: true,
  preferCSSPageSize: true,
  marginTop: 0, marginBottom: 0, marginLeft: 0, marginRight: 0,
})

writeFileSync(output, Buffer.from(data, 'base64'))
console.log(`wrote ${output}`)

await page.close()
await browser.close().catch(() => {})
