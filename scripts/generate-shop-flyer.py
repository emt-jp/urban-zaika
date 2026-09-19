"""
A5 flyers to leave in halal groceries and on mosque noticeboards.

Different job from generate-order-flyers.py. Those go in a delivery bag and argue "order direct
next time". These sit on a counter in a shop where every customer is already our audience, so
they argue "we are the halal restaurant down the road, and we cater your events".

Built as HTML and printed through Chrome rather than drawn in ReportLab, because the audience
reads Urdu and Bengali and neither script renders correctly without a shaping engine — ReportLab
would emit disconnected, reversed letterforms. Chrome shapes them properly.

    .venv-tools/bin/python scripts/generate-shop-flyer.py     # writes the HTML
    node scripts/html-to-pdf.mjs <file.html> <out.pdf>        # needs the CDP Chrome running

Two variants, one per branch: the QR and the address point at whichever branch the shop is near.
"""
import io
import pathlib

import segno

OUT = pathlib.Path('marketing/flyers')

BRANCHES = {
    'kita-ku': {
        'name_ja': 'Urban Zaika 十条店',
        'name_en': 'Urban Zaika Jujo',
        'addr_ja': '〒114-0034 東京都北区上十条5-14-6 竹内荘',
        'addr_en': '5-14-6 Kamijujo, Kita-ku — walk from Jujo or Higashi-Jujo',
        'tel': '080-3480-6994',
        'hours_ja': '毎日 11:00–15:00 / 17:00–23:30',
        'hours_en': 'Open daily 11:00–15:00 and 17:00–23:30',
        'url': 'https://urban-zaika.com/kita-ku/?utm_source=shop_flyer',
    },
    'edogawa': {
        'name_ja': 'Urban Zaika 上一色店',
        'name_en': 'Urban Zaika Kamiisshiki',
        'addr_ja': '〒133-0041 東京都江戸川区上一色1-8-21',
        'addr_en': '1-8-21 Kamiisshiki, Edogawa-ku — on Route 7, near Shinkoiwa',
        'tel': '03-5879-4679',
        'hours_ja': '毎日 10:30–14:45 / 17:00–22:30',
        'hours_en': 'Open daily 10:30–14:45 and 17:00–22:30',
        'url': 'https://urban-zaika.com/edogawa/?utm_source=shop_flyer',
    },
}

TEMPLATE = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<title>{name_en} — flyer</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=Noto+Sans+JP:wght@400;500;700&family=Noto+Nastaliq+Urdu:wght@400;600&family=Noto+Sans+Bengali:wght@400;600&display=swap" rel="stylesheet">
<style>
  @page {{ size: A5 portrait; margin: 0; }}
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    width: 148mm; height: 210mm;
    font-family: 'Noto Sans JP', sans-serif;
    color: #1A1A1A; background: #fff;
    display: flex; flex-direction: column;
    -webkit-print-color-adjust: exact; print-color-adjust: exact;
  }}
  .top {{ background: #8B1A1A; color: #fff; text-align: center; padding: 7mm 8mm 5.5mm; }}
  .brand {{ font-family: 'Playfair Display', serif; font-size: 24pt; font-weight: 800; letter-spacing: .5px; }}
  .cert {{
    display: inline-block; margin-top: 3.5mm; padding: 1.4mm 5mm;
    background: #D4A843; color: #1A1A1A; font-weight: 700; font-size: 9.5pt; border-radius: 99px;
  }}
  .gold-rule {{ height: 2mm; background: #D4A843; }}

  .body {{ flex: 1; padding: 5mm 9mm 0; text-align: center; }}
  h1 {{ font-size: 14pt; line-height: 1.35; color: #8B1A1A; font-weight: 700; }}
  h1 .en {{ display: block; font-size: 10.5pt; color: #3A3A3A; font-weight: 500; margin-top: 1.5mm; }}

  .photos {{ display: flex; gap: 2.5mm; margin-top: 4mm; }}
  .photos img {{
    flex: 1; width: 50%; height: 21mm; object-fit: cover; border-radius: 2mm; display: block;
  }}

  .dishes {{ margin-top: 3.5mm; font-size: 10pt; line-height: 1.55; }}
  .dishes .en {{ display: block; font-size: 8.5pt; color: #5A5A5A; }}

  .langs {{
    margin-top: 3.5mm; padding: 2mm 0; border-top: 1px solid #E5DED3; border-bottom: 1px solid #E5DED3;
    font-size: 10pt; display: flex; justify-content: center; gap: 4mm; align-items: baseline;
  }}
  .langs .ur {{ font-family: 'Noto Nastaliq Urdu', serif; font-size: 13pt; direction: rtl; }}
  .langs .bn {{ font-family: 'Noto Sans Bengali', sans-serif; font-size: 10pt; }}

  .catering {{
    margin-top: 3.5mm; border: 1.4pt solid #D4A843; border-radius: 3mm; padding: 3mm 5mm;
  }}
  .catering h2 {{ font-size: 12pt; color: #8B1A1A; }}
  .catering p {{ font-size: 8.5pt; line-height: 1.55; margin-top: 1.5mm; color: #3A3A3A; }}
  .catering .en {{ display: block; font-size: 8pt; color: #5A5A5A; }}

  .foot {{ display: flex; gap: 5mm; align-items: center; padding: 4mm 9mm 4mm; text-align: left; }}
  .qr {{ width: 27mm; height: 27mm; flex: none; }}
  .contact {{ flex: 1; }}
  .branch {{ font-size: 11pt; font-weight: 700; color: #8B1A1A; }}
  .tel {{ font-size: 18pt; font-weight: 700; letter-spacing: .3px; margin: 1mm 0; }}
  .meta {{ font-size: 7.4pt; line-height: 1.5; color: #4A4A4A; }}
  .meta .en {{ color: #6B6B6B; }}
  .site {{ margin-top: 1.5mm; font-size: 8.4pt; font-weight: 700; color: #8B1A1A; }}
</style>
</head>
<body>
  <div class="top">
    <div class="brand">Urban Zaika</div>
    <div class="cert">ハラール認証キッチン · HALAL CERTIFIED</div>
  </div>
  <div class="gold-rule"></div>

  <div class="body">
    <h1>本格インド・パキスタン料理
      <span class="en">Authentic Indian &amp; Pakistani, cooked to order</span>
    </h1>

    <div class="photos">
      <img src="data:image/jpeg;base64,{photo_a}" alt="">
      <img src="data:image/jpeg;base64,{photo_b}" alt="">
    </div>

    <div class="dishes">
      ビリヤニ · カラヒ · ニハリ · ケバブ · 焼きたてナン
      <span class="en">Hyderabadi biryani · Lahori karahi · nihari · seekh kebab · tandoori naan</span>
      ベジタリアン料理もご用意しています
      <span class="en">Full vegetarian selection</span>
    </div>

    <div class="langs">
      <span>日本語</span><span>·</span><span>English</span><span>·</span>
      <span class="ur">اردو</span><span>·</span><span class="bn">বাংলা</span>
    </div>

    <div class="catering">
      <h2>ご宴会・ケータリング承ります</h2>
      <p>結婚式 · アキーカ · イード · モスクの行事 · 企業のご会食<br>
        30〜100名様まで。当日のご注文にも対応できる場合がございます。
        <span class="en">Catering for weddings, aqiqah, Eid, mosque and company events —
          30 to 100 guests, often same day.</span>
      </p>
    </div>
  </div>

  <div class="foot">
    <img class="qr" src="data:image/png;base64,{qr}" alt="QR">
    <div class="contact">
      <div class="branch">{name_ja}</div>
      <div class="tel">{tel}</div>
      <div class="meta">
        {addr_ja}<br>
        <span class="en">{addr_en}</span><br>
        {hours_ja}
      </div>
      <div class="site">urban-zaika.com</div>
    </div>
  </div>
</body>
</html>
"""


def photo_b64(name):
    """Inline the photo so the PDF is self-contained and the file:// render cannot miss it."""
    import base64
    return base64.b64encode(pathlib.Path('images', name).read_bytes()).decode()


def qr_b64(url):
    buf = io.BytesIO()
    segno.make(url, error='h').save(buf, kind='png', scale=12, border=1,
                                    dark='#1A1A1A', light='#FFFFFF')
    import base64
    return base64.b64encode(buf.getvalue()).decode()


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for slug, b in BRANCHES.items():
        path = OUT / f'shop-flyer-{slug}.html'
        html = TEMPLATE.format(qr=qr_b64(b['url']),
                               photo_a=photo_b64('butter-chicken.jpg'),
                               photo_b=photo_b64('karahi.jpg'), **b)
        path.write_text(html, encoding='utf-8')
        print('wrote', path)


if __name__ == '__main__':
    main()
