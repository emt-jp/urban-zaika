# Urban Zaika - Website & Business Improvement Plan

## Status Legend
- [ ] Not started
- [x] Completed

---

## HIGH IMPACT - Website Improvements

### 1. Google Maps Embed
**Why:** Customers search "halal food near me" — a map helps them find you and builds trust.

- [x] Add an embedded Google Map in the Contact/Access section
- [x] Use the iframe embed from Google Maps for location: 1-8-21 Kamiisshiki, Edogawa City
- [x] Add bilingual labels (EN/JA) for directions text
- [x] Add nearby station info (最寄り駅) — Shinkoiwa Station (新小岩駅), bus/walk directions
- [x] Make the map responsive for mobile
- [x] Add a "Get Directions" button linking to Google Maps navigation

### 2. Online Ordering / Delivery Platform Links
**Why:** Delivery is a massive revenue channel in Tokyo — no links currently exist on the site.

- [ ] Research and confirm which platforms Urban Zaika is listed on (UberEats, Demaecan, Wolt, menu)
- [ ] Register on platforms not yet listed (prioritize UberEats and Demaecan)
- [x] Add a dedicated "Order Online" section or banner on the website
- [x] Add platform logos with direct links to each ordering page
- [x] Add delivery links to the mobile CTA bar
- [x] Bilingual labels: "デリバリー注文" / "Order Delivery"

### 3. Google Business Profile Link
**Why:** Most Tokyo restaurant discovery happens through Google Maps — this is the #1 local SEO driver.

- [ ] Verify Google Business Profile is claimed and up to date
- [ ] Ensure NAP (Name, Address, Phone) matches the website exactly
- [ ] Add high-quality photos to the profile (interior, exterior, top dishes)
- [ ] Add menu items with prices to the profile
- [ ] Set correct business hours, halal certification, and attributes
- [ ] Add a "Review us on Google" button/link on the website
- [ ] Add the Google Maps "place ID" link to structured data (JSON-LD)
- [ ] Respond to all existing Google reviews (builds engagement)

### 4. WhatsApp / LINE Order Buttons
**Why:** LINE is Japan's #1 messaging app; WhatsApp reaches the international/Muslim community.

- [ ] Create a LINE Official Account for Urban Zaika (if not already done)
- [ ] Set up LINE auto-reply with menu/hours info
- [ ] Get the WhatsApp Business number configured
- [ ] Add LINE and WhatsApp buttons to the mobile CTA bar (already has CTA bar structure)
- [ ] Add floating action buttons (FAB) for LINE/WhatsApp on desktop
- [ ] Use proper deep links: `https://line.me/R/ti/p/@xxxxx` and `https://wa.me/81XXXXXXXXXX`
- [ ] Add LINE QR code in the contact section (common in Japan)
- [ ] Bilingual labels: "LINEで予約" / "Reserve via LINE"

### 5. Photo Gallery Upgrade
**Why:** Only 7 food images — more high-quality photos drive appetite and conversions.

- [ ] Take professional photos of top 15-20 dishes (use natural lighting)
- [ ] Include categories: curries, biryani, kebabs, naan/roti, desserts, drinks
- [ ] Take interior/ambiance shots (halal certificate on wall, seating area)
- [ ] Optimize all images: convert to WebP, compress to <100KB each
- [ ] Add a photo gallery section with lightbox viewer
- [ ] Add `alt` tags in both EN and JA for each image (SEO)
- [ ] Use `srcset` for responsive images (mobile vs desktop sizes)
- [ ] Add photos to Google Business Profile as well

### 6. Speed Optimization
**Why:** 56KB HTML is heavy for a static page — slow load = lost customers, especially on mobile.

- [ ] Audit current page with Google PageSpeed Insights / Lighthouse
- [ ] Minify CSS (35KB) and JS (8KB)
- [ ] Convert all images from JPG to WebP format
- [ ] Implement proper `srcset` and `sizes` attributes for responsive images
- [ ] Add `loading="lazy"` to all below-the-fold images
- [ ] Inline critical CSS, defer non-critical styles
- [ ] Preload hero image and key fonts
- [ ] Add `<link rel="dns-prefetch">` for external domains (Google Fonts)
- [ ] Enable Brotli/gzip compression in Firebase hosting headers
- [ ] Target: Lighthouse score > 90 on mobile

### 7. Japanese SEO
**Why:** Meta tags were English-only — Japanese users searching in Japanese won't find the site.

- [x] Title tag — changed to Japanese-first: `Urban Zaika｜ハラルインド・パキスタン料理｜東京都江戸川区`
- [x] Meta description — Japanese-primary with key search terms
- [x] Keywords — added Japanese terms (ハラルレストラン 東京, インドカレー 東京, etc.)
- [x] Open Graph — locale set to `ja_JP`, title/description in Japanese
- [x] JSON-LD — added `alternateName: アーバンザイカ`, Japanese address, Japanese cuisine names
- [x] Fixed URL inconsistency (`urbanzaika.com` → `urban-zaika.com`)
- [x] Add `<meta name="geo.region" content="JP-13">` and `<meta name="geo.placename" content="Edogawa, Tokyo">`
- [x] Add canonical tag, og:image, og:url meta tags
- [x] Fix JSON-LD image URL to absolute path
- [x] Update copyright year to 2025-2026
- [ ] Submit updated sitemap to Google Search Console
- [ ] Add Japanese alt text to all images
- [ ] Create a Google Search Console property and verify ownership
- [ ] Monitor keyword rankings for: ハラルレストラン 東京, ハラル インド料理 江戸川, パキスタン料理 東京

---

## MEDIUM IMPACT - Website Improvements

### 8. Customer Reviews Section
**Why:** Social proof converts visitors into customers — especially for restaurants.

- [ ] Add a "Reviews / お客様の声" section on the homepage
- [ ] Collect 5-10 real customer testimonials (ask regulars)
- [ ] Display Google review rating badge (star rating + review count)
- [ ] Add a "Write a Review" CTA linking to Google Business Profile
- [ ] Show review snippets with customer name and star rating
- [x] Add review structured data (`@type: Review`) to JSON-LD for rich snippets
- [ ] Bilingual review display (translate if needed)

### 9. Lunch Set Menu Promotion
**Why:** Office workers and nearby residents are the weekday lunch market — price-driven decisions.

- [ ] Create a prominent lunch banner/section on the homepage
- [ ] Design 3-4 lunch sets (¥800-1000 range): curry + naan + drink combos
- [ ] Add lunch hours clearly: ランチタイム 11:00-14:00
- [ ] Highlight value: "ランチセット ¥800から" (Lunch sets from ¥800)
- [ ] Add lunch-specific keywords to meta tags
- [ ] Create a time-based banner that only shows during/before lunch hours (JS)
- [ ] Add lunch menu photos

### 10. Instagram Feed Embed
**Why:** Social proof without extra content effort — keeps the site fresh automatically.

- [ ] Create/verify Instagram business account (@urbanzaika or similar)
- [ ] Post consistently: 3-5 food photos per week with JP+EN hashtags
- [ ] Embed Instagram feed in a "Follow Us / フォローする" section
- [ ] Use Instagram Basic Display API or a widget service (SnapWidget, Elfsight)
- [ ] Add Instagram link to footer and social links
- [ ] Hashtag strategy: #ハラルレストラン #東京グルメ #インドカレー #江戸川区 #halalfoodtokyo #urbanzaika

---

## BUSINESS STRATEGIES (Outside the Website)

### Google Business Profile
- [ ] Claim and verify the profile if not done
- [ ] Complete all fields: hours, menu, photos, attributes (halal, vegetarian options)
- [ ] Post weekly updates (new dishes, lunch specials, events)
- [ ] Respond to every review within 24 hours
- [ ] Add Q&A section answers proactively

### Tabelog / Hot Pepper Gourmet
- [ ] Create listings on Tabelog (食べログ) — Japan's #1 restaurant review site
- [ ] Create listing on Hot Pepper Gourmet (ホットペッパーグルメ)
- [ ] Create listing on Retty
- [ ] Ensure consistent NAP across all platforms
- [ ] Add lunch/dinner course menus with prices

### Halal Media Partnerships
- [ ] Register on HALAL NAVI app (popular with Muslim tourists)
- [ ] Contact Halal Media Japan for a feature/listing
- [ ] Register on Halal Gourmet Japan
- [ ] Register on CrescentRating / HalalTrip
- [ ] Get listed on Tokyo mosque community boards
- [ ] Target inbound tourist keywords: "halal food near Shinkoiwa"

### Delivery Platforms
- [ ] Register on UberEats (ウーバーイーツ) — highest reach in Tokyo
- [ ] Register on Demaecan (出前館) — strong in residential areas like Edogawa
- [ ] Register on Wolt — growing fast in Tokyo
- [ ] Register on menu — another option for coverage
- [ ] Optimize menu for delivery (items that travel well)
- [ ] Set competitive delivery pricing

### Lunch Set Strategy
- [ ] Design 3-4 lunch sets at ¥800-1000 price point
- [ ] Create a physical lunch banner/A-frame sign outside the restaurant
- [ ] Distribute lunch flyers to nearby offices and apartment buildings
- [ ] Offer first-visit lunch discount (LINE coupon)

### Instagram Marketing
- [ ] Post 3-5 times per week with high-quality food photos
- [ ] Use bilingual captions and hashtags
- [ ] Run Instagram Stories for daily specials
- [ ] Collaborate with local food influencers / halal food bloggers
- [ ] Run targeted Instagram ads (Edogawa area, halal food interests)

### Friday Prayer / Mosque Partnerships
- [ ] Identify nearby mosques (Edogawa area, Tokyo Camii)
- [ ] Offer Friday lunch specials / group discounts
- [ ] Distribute flyers at mosque after Friday prayers
- [ ] Offer catering for mosque events (Ramadan iftar, Eid celebrations)

### Catering Service
- [ ] Create a catering menu (party platters, corporate lunch boxes)
- [ ] Add a catering page/section to the website
- [ ] Register on catering platforms
- [ ] Target corporate events, embassy functions, international schools
- [ ] Offer halal bento boxes for office delivery

---

## Priority Order (Recommended Execution)

| Priority | Task | Effort | Impact |
|----------|------|--------|--------|
| 1 | Google Business Profile (claim + optimize) | Low | Highest |
| 2 | Japanese SEO (meta tags) | Low | High |
| 3 | Google Maps embed on website | Low | High |
| 4 | Delivery platform registration (UberEats/Demaecan) | Medium | High |
| 5 | LINE Official Account + website buttons | Medium | High |
| 6 | Lunch set menu creation + promotion | Medium | High |
| 7 | Photo gallery upgrade | Medium | Medium |
| 8 | Customer reviews section | Low | Medium |
| 9 | Speed optimization | Medium | Medium |
| 10 | Instagram setup + feed embed | Medium | Medium |
| 11 | Tabelog / Hot Pepper listings | Low | Medium |
| 12 | Halal media partnerships | Low | Medium |
| 13 | Catering service launch | High | Medium |
| 14 | Mosque partnerships | Low | Low-Medium |
