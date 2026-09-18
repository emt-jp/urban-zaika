/**
 * Create a Google Ads Search campaign from a config file — everything PAUSED so
 * nothing spends until a human enables it in the UI.
 *
 * Ported from tdc/ads/create-campaign.mjs, extended for local restaurants:
 *   - radius (proximity) targeting around each branch
 *   - ad schedule (only serve while the branch is open)
 *   - Maximize Clicks with a CPC ceiling (for accounts with no conversion history)
 *   - call asset
 *   - --check mode: validates ad copy lengths with no credentials and no API calls
 *
 * Validate copy (no creds needed):
 *   node create-campaign.mjs --check ./campaign.kamiisshiki.mjs
 *
 * Create (needs Google Ads API access — see README.md):
 *   npm init -y && npm i google-ads-api
 *   GADS_DEVELOPER_TOKEN=... GADS_CLIENT_ID=... GADS_CLIENT_SECRET=... \
 *   GADS_REFRESH_TOKEN=... GADS_CUSTOMER_ID=1234567890 \
 *   node create-campaign.mjs ./campaign.kamiisshiki.mjs
 *
 * Safety: status PAUSED. Re-running creates duplicates — NOT idempotent.
 */

const args = process.argv.slice(2)
const checkOnly = args.includes('--check')
const cfgPath = args.find((a) => !a.startsWith('--'))
if (!cfgPath) {
  console.error('Usage: node create-campaign.mjs [--check] ./campaign.<branch>.mjs')
  process.exit(1)
}
const cfg = (await import(new URL(cfgPath, import.meta.url))).default

// Google counts full-width characters (Japanese, full-width symbols) as 2.
const isWide = (cp) =>
  (cp >= 0x1100 && cp <= 0x115f) || (cp >= 0x2e80 && cp <= 0xa4cf) || (cp >= 0xac00 && cp <= 0xd7a3) ||
  (cp >= 0xf900 && cp <= 0xfaff) || (cp >= 0xfe30 && cp <= 0xfe4f) || (cp >= 0xff00 && cp <= 0xff60) ||
  (cp >= 0xffe0 && cp <= 0xffe6)
const adsWidth = (s) => [...s].reduce((n, ch) => n + (isWide(ch.codePointAt(0)) ? 2 : 1), 0)

function validate() {
  const errors = []
  const limit = (label, text, max) => {
    const w = adsWidth(text)
    if (w > max) errors.push(`${label} too long (${w}/${max}): ${text}`)
  }
  for (const ag of cfg.adGroups) {
    if (ag.headlines.length < 3 || ag.headlines.length > 15) errors.push(`${ag.name}: need 3–15 headlines`)
    if (ag.descriptions.length < 2 || ag.descriptions.length > 4) errors.push(`${ag.name}: need 2–4 descriptions`)
    ag.headlines.forEach((h) => limit(`${ag.name} headline`, h, 30))
    ag.descriptions.forEach((d) => limit(`${ag.name} description`, d, 90))
    ;(ag.path || []).forEach((p) => limit(`${ag.name} path`, p, 15))
    if (new Set(ag.headlines).size !== ag.headlines.length) errors.push(`${ag.name}: duplicate headlines`)
  }
  for (const s of cfg.sitelinks || []) {
    limit('sitelink text', s.text, 25)
    limit('sitelink desc1', s.desc1, 35)
    limit('sitelink desc2', s.desc2, 35)
  }
  ;(cfg.callouts || []).forEach((c) => limit('callout', c, 25))
  ;(cfg.structuredSnippet?.values || []).forEach((v) => limit('snippet value', v, 25))
  return errors
}

const errors = validate()
if (errors.length) {
  console.error(`✗ ${cfg.campaignName}\n  ${errors.join('\n  ')}`)
  process.exit(1)
}
const kwCount = cfg.adGroups.reduce((n, ag) => n + ag.keywords.length, 0)
console.log(`✓ ${cfg.campaignName}: ${cfg.adGroups.length} ad groups, ${kwCount} keywords — copy lengths OK`)
if (checkOnly) process.exit(0)

const required = ['GADS_DEVELOPER_TOKEN', 'GADS_CLIENT_ID', 'GADS_CLIENT_SECRET', 'GADS_REFRESH_TOKEN', 'GADS_CUSTOMER_ID']
const missing = required.filter((k) => !process.env[k])
if (missing.length) {
  console.error(`Missing env: ${missing.join(', ')}`)
  process.exit(1)
}

const { GoogleAdsApi, enums, ResourceNames, toMicros } = await import('google-ads-api')

const customerId = process.env.GADS_CUSTOMER_ID
const client = new GoogleAdsApi({
  client_id: process.env.GADS_CLIENT_ID,
  client_secret: process.env.GADS_CLIENT_SECRET,
  developer_token: process.env.GADS_DEVELOPER_TOKEN,
})
const customer = client.Customer({
  customer_id: customerId,
  login_customer_id: process.env.GADS_LOGIN_CUSTOMER_ID || undefined,
  refresh_token: process.env.GADS_REFRESH_TOKEN,
})

const MATCH = {
  EXACT: enums.KeywordMatchType.EXACT,
  PHRASE: enums.KeywordMatchType.PHRASE,
  BROAD: enums.KeywordMatchType.BROAD,
}
const DAYS = {
  MON: enums.DayOfWeek.MONDAY, TUE: enums.DayOfWeek.TUESDAY, WED: enums.DayOfWeek.WEDNESDAY,
  THU: enums.DayOfWeek.THURSDAY, FRI: enums.DayOfWeek.FRIDAY, SAT: enums.DayOfWeek.SATURDAY,
  SUN: enums.DayOfWeek.SUNDAY,
}

function bidding() {
  if (cfg.bidding?.strategy === 'MAXIMIZE_CLICKS') {
    return { target_spend: { cpc_bid_ceiling_micros: toMicros(cfg.bidding.maxCpcYen) } }
  }
  return { maximize_conversions: {} }
}

async function run() {
  console.log(`\nCreating campaign "${cfg.campaignName}" in account ${customerId} (PAUSED)…\n`)

  // 1. Budget
  const [budgetRes] = await customer.campaignBudgets.create([
    {
      name: `${cfg.campaignName} — budget`,
      amount_micros: toMicros(cfg.dailyBudgetYen),
      delivery_method: enums.BudgetDeliveryMethod.STANDARD,
      explicitly_shared: false,
    },
  ])
  const budget = budgetRes.resource_name
  console.log(`✓ budget: ¥${cfg.dailyBudgetYen}/day`)

  // 2. Campaign — Search only, PAUSED, presence-only location targeting.
  const [campRes] = await customer.campaigns.create([
    {
      name: cfg.campaignName,
      status: enums.CampaignStatus.PAUSED,
      advertising_channel_type: enums.AdvertisingChannelType.SEARCH,
      campaign_budget: budget,
      ...bidding(),
      network_settings: {
        target_google_search: true,
        target_search_network: false,
        target_content_network: false,
        target_partner_search_network: false,
      },
      geo_target_type_setting: {
        positive_geo_target_type: enums.PositiveGeoTargetType.PRESENCE,
      },
    },
  ])
  const campaign = campRes.resource_name
  console.log(`✓ campaign: ${campaign}`)

  // 3. Location (region IDs and/or radius) + language + ad schedule
  const criteria = []
  for (const id of cfg.geoTargetIds || []) {
    criteria.push({ campaign, location: { geo_target_constant: ResourceNames.geoTargetConstant(id) } })
  }
  if (cfg.radius) {
    const { lat, lng, address, km } = cfg.radius
    criteria.push({
      campaign,
      proximity: {
        radius: km,
        radius_units: enums.ProximityRadiusUnits.KILOMETERS,
        ...(lat != null
          ? { geo_point: { latitude_in_micro_degrees: Math.round(lat * 1e6), longitude_in_micro_degrees: Math.round(lng * 1e6) } }
          : { address: { ...address, country_code: 'JP' } }),
      },
    })
  }
  for (const id of cfg.languageIds) {
    criteria.push({ campaign, language: { language_constant: ResourceNames.languageConstant(id) } })
  }
  for (const s of cfg.adSchedule || []) {
    for (const day of s.days) {
      criteria.push({
        campaign,
        bid_modifier: s.bidModifier ?? 1,
        ad_schedule: {
          day_of_week: DAYS[day],
          start_hour: s.start, start_minute: enums.MinuteOfHour.ZERO,
          end_hour: s.end, end_minute: enums.MinuteOfHour.ZERO,
        },
      })
    }
  }
  await customer.campaignCriteria.create(criteria)
  console.log(`✓ ${criteria.length} location/language/schedule criteria`)

  // Campaign-level negatives (shared across ad groups)
  if (cfg.campaignNegatives?.length) {
    await customer.campaignCriteria.create(
      cfg.campaignNegatives.map((text) => ({
        campaign,
        negative: true,
        keyword: { text, match_type: enums.KeywordMatchType.BROAD },
      })),
    )
    console.log(`✓ ${cfg.campaignNegatives.length} campaign negatives`)
  }

  // 4. Ad groups + keywords + negatives + RSAs
  for (const ag of cfg.adGroups) {
    const [agRes] = await customer.adGroups.create([
      {
        campaign,
        name: ag.name,
        status: enums.AdGroupStatus.ENABLED,
        type: enums.AdGroupType.SEARCH_STANDARD,
      },
    ])
    const adGroup = agRes.resource_name

    const kwCriteria = ag.keywords.map((k) => ({
      ad_group: adGroup,
      status: enums.AdGroupCriterionStatus.ENABLED,
      keyword: { text: k.text, match_type: MATCH[k.match] },
    }))
    const negCriteria = (ag.negatives || []).map((text) => ({
      ad_group: adGroup,
      negative: true,
      keyword: { text, match_type: enums.KeywordMatchType.BROAD },
    }))
    await customer.adGroupCriteria.create([...kwCriteria, ...negCriteria])

    await customer.adGroupAds.create([
      {
        ad_group: adGroup,
        status: enums.AdGroupAdStatus.ENABLED,
        ad: {
          final_urls: [ag.finalUrl],
          responsive_search_ad: {
            headlines: ag.headlines.map((text) => ({ text })),
            descriptions: ag.descriptions.map((text) => ({ text })),
            path1: ag.path?.[0],
            path2: ag.path?.[1],
          },
        },
      },
    ])
    console.log(`✓ ad group "${ag.name}": ${ag.keywords.length} kw, ${negCriteria.length} neg, 1 RSA`)
  }

  // 5. Assets (sitelinks, callouts, structured snippet, call) linked to the campaign.
  try {
    const assetOps = []
    const fieldTypes = []
    for (const s of cfg.sitelinks || []) {
      assetOps.push({
        sitelink_asset: { link_text: s.text, description1: s.desc1, description2: s.desc2 },
        final_urls: [s.url],
      })
      fieldTypes.push(enums.AssetFieldType.SITELINK)
    }
    for (const text of cfg.callouts || []) {
      assetOps.push({ callout_asset: { callout_text: text } })
      fieldTypes.push(enums.AssetFieldType.CALLOUT)
    }
    if (cfg.structuredSnippet) {
      assetOps.push({
        structured_snippet_asset: { header: cfg.structuredSnippet.header, values: cfg.structuredSnippet.values },
      })
      fieldTypes.push(enums.AssetFieldType.STRUCTURED_SNIPPET)
    }
    if (cfg.phone) {
      assetOps.push({ call_asset: { country_code: 'JP', phone_number: cfg.phone } })
      fieldTypes.push(enums.AssetFieldType.CALL)
    }
    const assetResults = await customer.assets.create(assetOps)
    await customer.campaignAssets.create(
      assetResults.map((r, i) => ({ campaign, asset: r.resource_name, field_type: fieldTypes[i] })),
    )
    console.log(`✓ ${assetOps.length} assets linked`)
  } catch (e) {
    console.warn(`! assets step failed (campaign + ads are fine, add assets in UI): ${e.message}`)
  }

  console.log(`\nDone. Campaign is PAUSED. Link the branch's Business Profile location asset in the UI, review, then enable.`)
}

run().catch((e) => {
  console.error('Failed:', e.errors ? JSON.stringify(e.errors, null, 2) : e.message)
  process.exit(1)
})
