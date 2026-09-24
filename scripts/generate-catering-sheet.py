"""
A4 catering one-pager — the thing you hand to a mosque committee or email to an office.

Catering demand in these wards does not come through Google search: every Japanese catering
keyword we tried came back "rarely served". It comes through committees, halal shops and word of
mouth, all of which need something physical to keep. This is that.

Built as HTML and printed through Chrome, like the shop flyers, because the page carries Urdu and
Bengali and ReportLab cannot shape either.

    .venv-tools/bin/python scripts/generate-catering-sheet.py
    node scripts/html-to-pdf.mjs marketing/flyers/catering-sheet.html out.pdf
"""
import base64
import io
import pathlib

import segno

OUT = pathlib.Path('marketing/flyers')
URL = 'https://urban-zaika.com/catering/?utm_source=catering_sheet'

TEMPLATE = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<title>Urban Zaika — catering</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=Noto+Sans+JP:wght@400;500;700&family=Noto+Nastaliq+Urdu:wght@400&family=Noto+Sans+Bengali:wght@400&display=swap" rel="stylesheet">
<style>
  @page {{ size: A4 portrait; margin: 0; }}
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    width: 210mm; height: 297mm; font-family: 'Noto Sans JP', sans-serif; color: #1A1A1A;
    background: #fff; display: flex; flex-direction: column;
    -webkit-print-color-adjust: exact; print-color-adjust: exact;
  }}
  .top {{ background: #8B1A1A; color: #fff; text-align: center; padding: 8mm 10mm 6mm; }}
  .brand {{ font-family: 'Playfair Display', serif; font-size: 26pt; font-weight: 800; }}
  .cert {{
    display: inline-block; margin-top: 4mm; padding: 1.6mm 6mm; background: #D4A843;
    color: #1A1A1A; font-weight: 700; font-size: 10.5pt; border-radius: 99px;
  }}
  .rule {{ height: 2.5mm; background: #D4A843; }}

  .body {{ flex: 1; padding: 6mm 14mm 0; }}
  h1 {{ font-size: 17pt; color: #8B1A1A; text-align: center; line-height: 1.4; }}
  h1 .en {{ display: block; font-size: 10.5pt; color: #3A3A3A; font-weight: 500; margin-top: 2mm; }}

  .events {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 2.5mm; margin-top: 5mm; }}
  .ev {{ border: 1pt solid #E2D9CB; border-radius: 2.5mm; padding: 2.8mm 2.5mm; text-align: center; }}
  .ev .ja {{ font-size: 10pt; font-weight: 700; color: #8B1A1A; }}
  .ev .en {{ display: block; font-size: 7.6pt; color: #5A5A5A; margin-top: 1mm; }}

  .two {{ display: flex; gap: 6mm; margin-top: 5mm; }}
  .col {{ flex: 1; }}
  .col h2 {{ font-size: 11.5pt; color: #8B1A1A; border-bottom: 1.2pt solid #D4A843; padding-bottom: 1.5mm; }}
  .col ul {{ list-style: none; margin-top: 2.5mm; }}
  .col li {{ font-size: 9pt; line-height: 1.6; }}
  .col li .en {{ color: #5A5A5A; font-size: 8pt; margin-left: 1mm; }}

  /* the line that actually converts a committee - an offer, not a claim */
  .offer {{
    margin-top: 5mm; border: 1.6pt solid #8B1A1A; border-radius: 3mm; padding: 4mm 6mm;
    text-align: center; background: #FDF7EF;
  }}
  .offer .ja {{ font-size: 11.5pt; font-weight: 700; color: #8B1A1A; }}
  .offer .en {{ display: block; font-size: 9pt; color: #3A3A3A; margin-top: 1.5mm; line-height: 1.6; }}
  .halal-note {{ margin-top: 4mm; text-align: center; font-size: 8.6pt; color: #4A4A4A; line-height: 1.7; }}

  .langs {{
    margin-top: 4mm; padding: 2mm 0; text-align: center;
    border-top: 1px solid #E2D9CB; border-bottom: 1px solid #E2D9CB; font-size: 10pt;
  }}
  .langs span {{ margin: 0 3mm; }}
  .ur {{ font-family: 'Noto Nastaliq Urdu', serif; font-size: 12pt; }}
  .bn {{ font-family: 'Noto Sans Bengali', sans-serif; }}

  .foot {{ display: flex; gap: 7mm; align-items: center; padding: 5mm 14mm 4mm; }}
  .qr {{ width: 31mm; height: 31mm; flex: none; }}
  .branches {{ flex: 1; display: flex; gap: 7mm; }}
  .br {{ flex: 1; }}
  .br .nm {{ font-size: 10.5pt; font-weight: 700; color: #8B1A1A; }}
  .br .tel {{ font-size: 17pt; font-weight: 700; margin: 0.8mm 0; }}
  .br .ad {{ font-size: 7.4pt; color: #4A4A4A; line-height: 1.5; }}
  .site {{ text-align: right; font-size: 9pt; font-weight: 700; color: #8B1A1A; }}
</style>
</head>
<body>
  <div class="top">
    <div class="brand">Urban Zaika</div>
    <div class="cert">ハラール認証キッチン · HALAL CERTIFIED KITCHEN</div>
  </div>
  <div class="rule"></div>

  <div class="body">
    <h1>ご宴会・ケータリング承ります
      <span class="en">Halal Indian &amp; Pakistani catering, cooked in our own kitchens</span>
    </h1>

    <div class="events">
      <div class="ev"><span class="ja">結婚式・ワリーマ</span><span class="en">Weddings &amp; walima</span></div>
      <div class="ev"><span class="ja">アキーカ・ミラード</span><span class="en">Aqiqah &amp; milad</span></div>
      <div class="ev"><span class="ja">イード</span><span class="en">Eid gatherings</span></div>
      <div class="ev"><span class="ja">イフタール</span><span class="en">Iftar &amp; Ramadan</span></div>
      <div class="ev"><span class="ja">モスクの行事</span><span class="en">Mosque &amp; community events</span></div>
      <div class="ev"><span class="ja">企業のご会食・忘年会</span><span class="en">Company &amp; year-end parties</span></div>
    </div>

    <div class="two">
      <div class="col">
        <h2>お料理 · What we cook</h2>
        <ul>
          <li>ハイデラバード式ビリヤニ <span class="en">Hyderabadi biryani</span></li>
          <li>ラホール風カラヒ・ニハリ <span class="en">Lahori karahi, nihari</span></li>
          <li>シークカバブ・タンドール料理 <span class="en">Seekh kebab, tandoori</span></li>
          <li>焼きたてナン・ライス <span class="en">Fresh naan and rice</span></li>
          <li>ベジタリアン料理 <span class="en">Full vegetarian selection</span></li>
        </ul>
      </div>
      <div class="col">
        <h2>ご利用について · How it works</h2>
        <ul>
          <li><strong>30〜100名様</strong>まで（1店舗あたり）<span class="en">30–100 guests per kitchen</span></li>
          <li><strong>当日のご注文</strong>にも対応可<span class="en">Same-day orders often possible</span></li>
          <li>それ以上は2店舗で分担<span class="en">Larger events across both branches</span></li>
          <li>北区・江戸川区と周辺区へお届け<span class="en">Delivered across north and east Tokyo</span></li>
          <li>お見積りはお電話で<span class="en">Call us for a quote</span></li>
        </ul>
      </div>
    </div>

    <div class="offer">
      <span class="ja">まずは無料の試食をご用意いたします</span>
      <span class="en">We will gladly cook a free tasting for your committee or your team, so you can
        judge the food before you book anything.</span>
    </div>

    <div class="halal-note">
      両店舗ともハラール認証を取得したキッチンです。肉類はすべてハラール処理されたものを使用し、豚肉は一切取り扱っておりません。<br>
      <span style="color:#6B6B6B">Both kitchens are halal certified. All meat is halal-slaughtered; no pork is handled.</span>
    </div>

    <div class="langs">
      <span>日本語</span>·<span>English</span>·<span class="ur">اردو</span>·<span class="bn">বাংলা</span>
      <span style="font-size:8.4pt;color:#5A5A5A">でご注文いただけます</span>
    </div>
  </div>

  <div class="foot">
    <img class="qr" src="data:image/png;base64,{qr}" alt="QR">
    <div class="branches">
      <div class="br">
        <div class="nm">上一色店 · Kamiisshiki</div>
        <div class="tel">03-5879-4679</div>
        <div class="ad">〒133-0041 東京都江戸川区上一色1-8-21<br>毎日 10:30–14:45 / 17:00–22:30</div>
      </div>
      <div class="br">
        <div class="nm">十条店 · Jujo</div>
        <div class="tel">080-3480-6994</div>
        <div class="ad">〒114-0034 東京都北区上十条5-14-6 竹内荘<br>毎日 11:00–15:00 / 17:00–23:30</div>
      </div>
    </div>
  </div>
  <div class="site" style="padding:0 14mm 6mm">urban-zaika.com/catering</div>
</body>
</html>
"""


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    buf = io.BytesIO()
    segno.make(URL, error='h').save(buf, kind='png', scale=12, border=1,
                                    dark='#1A1A1A', light='#FFFFFF')
    path = OUT / 'catering-sheet.html'
    path.write_text(TEMPLATE.format(qr=base64.b64encode(buf.getvalue()).decode()), encoding='utf-8')
    print('wrote', path)


if __name__ == '__main__':
    main()
