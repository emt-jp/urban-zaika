# Google Business Profile posts — running queue

Posts expire from the profile's prominent slot after about a week, so one post per branch per
week is the cadence that keeps both listings looking active. They are free, they show up in the
Maps panel, and the Edogawa profile alone drew 4,590 monthly views — this is the cheapest
placement we have.

Publish with:

```bash
POST_TEXT="$(sed -n '…')" node scripts/gbp-post.mjs <locationId> images/<photo>.jpg
```

Location IDs are in `ads/gbp-audit-2026-09-17.md` (untracked). Requires the CDP Chrome described
in the script header.

**Rules that matter**

- Write Japanese first, English second. Roughly half the Edogawa searches are English, but the
  people walking past are Japanese.
- Never reuse copy between branches. The hours differ (10:30–14:45 / 17:00–22:30 at 上一色店,
  11:00–15:00 / 17:00–23:30 at 十条店) and Google offers to copy a post to the other profile
  after publishing — decline it.
- Always attach a photo. Posts without one get noticeably less space in the panel.
- No phone numbers in the body; the profile already carries the number, and Ads rejected our ad
  copy for exactly this.
- 1,500 character limit; aim for 150–250.

**Photos on hand:** `butter-chicken`, `karahi`, `chana`, `aloo-matar`, `curry-bowl`,
`chicken-curry-promo`, `fries`. We are short of biryani, naan, kebab and tandoor shots — those
are shots 1, 2, 4 and 6 in `social-content-plan.md` and would serve both channels.

---

## Published

| Date | Branch | Topic | Photo |
|---|---|---|---|
| 2026-09-19 | 上一色店 | Lunch sets ¥650 | butter-chicken |
| 2026-09-19 | 十条店 | Tandoor, near Jujo station | karahi |

---

## Queue

### Week 2

**上一色店** — photo: `karahi.jpg`
> ラホール風カラヒ。トマトとバター、スパイスだけで煮込みます。焼きたてのナンと一緒にどうぞ。国道7号沿い、小岩駅・新小岩駅からバス圏内。
>
> Lahori karahi, slow-cooked with tomato, butter and spice. Best with naan straight from the tandoor. On Route 7, a short bus ride from Koiwa or Shinkoiwa.

**十条店** — photo: `butter-chicken.jpg`
> バターチキンは辛さを調整できます。お子様にはマイルドで。ランチは11:00から、ナンまたはライス付き。
>
> Butter chicken, spiced to your liking — mild for children. Lunch from 11:00 with naan or rice.

### Week 3 — halal and trust

**上一色店** — photo: `curry-bowl.jpg`
> 100%ハラール対応のキッチンです。ベジタリアンメニューもご用意しています。英語・ウルドゥー語でのご注文も承ります。
>
> Fully halal kitchen, with vegetarian dishes on the menu. English and Urdu spoken.

**十条店** — photo: `chana.jpg`
> ベジタリアンの方へ。チャナマサラ、ダル、野菜カレーをご用意しています。ハラール対応、毎日営業。
>
> For vegetarians: chana masala, dal and vegetable curries. Halal kitchen, open daily.

### Week 4 — delivery

**上一色店** — photo: `chicken-curry-promo.jpg`
> Uber Eats・出前館でのデリバリーに対応しています。テイクアウトのご予約はお電話でも承ります。
>
> Delivery on Uber Eats and Demaecan. Takeaway can be ordered ahead by phone.

**十条店** — photo: `curry-bowl.jpg`
> デリバリー・テイクアウト承ります。焼きたてのナンを熱いうちにお届けします。
>
> Delivery and takeaway available. The naan leaves the tandoor as the order goes out.

### Week 5 — weekend and groups

**上一色店** — photo: `butter-chicken.jpg`
> 週末は混み合います。ご家族やグループでのご利用はお早めにご連絡ください。大皿でのご用意も可能です。
>
> Weekends fill up. Call ahead for family and group bookings — we can serve family-style platters.

**十条店** — photo: `aloo-matar.jpg`
> ディナーは23:30まで。仕事帰りにも、遅い夕食にも。十条駅から徒歩圏内です。
>
> Dinner until 23:30 — late enough for after work. Walking distance from Jujo Station.

### Week 6 onward

Rotate the same four themes — lunch, a dish, halal/vegetarian, delivery — with new photos. Once
the biryani, naan and kebab shots exist, lead with those; they are the dishes people search for.

**Seasonal, worth planning now:** Ramadan begins around February 2027. Iftar sets and group packs
get booked weeks in advance and are the single biggest window of the year for a halal restaurant.
Posts should start in January.
