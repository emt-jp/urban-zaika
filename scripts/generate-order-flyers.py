"""
Delivery-bag flyers: turn platform customers into direct customers.

Uber Eats, Demaecan and Rocket Now take 28-35% commission. A customer who reorders by
LINE, phone or WhatsApp is worth roughly 1.4x the same order. This prints A5 flyers
(4 per A4 sheet) to drop in every delivery bag, with a LINE QR on one side of the layout
and the branch's phone number spelled out large.

Two offer variants are produced so the owner can pick:
    discount  — 10% off the next direct order
    freeship  — free delivery over 2,000 yen

Usage:
    .venv-tools/bin/python scripts/generate-order-flyers.py
    -> order-flyer-<branch>-<variant>.pdf   (4 variants x 2 branches)

Deps (in .venv-tools): reportlab, segno
"""
import io

import segno
from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfgen import canvas

BURGUNDY = HexColor('#8B1A1A')
GOLD = HexColor('#D4A843')
CHARCOAL = HexColor('#1A1A1A')
GREY = HexColor('#5A5A5A')
LINE_GREEN = HexColor('#06C755')

CARD_W, CARD_H = 105 * mm, 148.5 * mm   # A5, four to an A4 sheet

LINE_URL = 'https://line.me/R/ti/p/@urbanzaika'
WHATSAPP = '+81 90-6658-2838'

BRANCHES = [
    {
        'slug': 'edogawa',
        'name_ja': 'Urban Zaika 上一色店',
        'tel': '03-5879-4679',
        'hours_ja': '毎日 10:30–14:45 / 17:00–22:30',
    },
    {
        'slug': 'kita-ku',
        'name_ja': 'Urban Zaika 十条店',
        'tel': '080-3480-6994',
        'hours_ja': '毎日 11:00–15:00 / 17:00–23:30',
    },
]

VARIANTS = {
    'discount': {
        'headline_ja': '次回はお電話・LINEで',
        'offer_ja': '直接ご注文で 10%OFF',
        'offer_en': '10% off when you order direct',
    },
    'freeship': {
        'headline_ja': '次回はお電話・LINEで',
        'offer_ja': '¥2,000以上で 配達無料',
        'offer_en': 'Free delivery over ¥2,000',
    },
}


def qr_image(url):
    qr = segno.make(url, error='h')
    buf = io.BytesIO()
    qr.save(buf, kind='png', scale=20, border=1, dark='#1A1A1A', light='#FFFFFF')
    buf.seek(0)
    return ImageReader(buf)


def draw_flyer(c, x, y, branch, variant, qr):
    v = VARIANTS[variant]

    c.setFillColor(white)
    c.rect(x, y, CARD_W, CARD_H, stroke=0, fill=1)

    # burgundy header band
    c.setFillColor(BURGUNDY)
    c.rect(x, y + CARD_H - 34 * mm, CARD_W, 34 * mm, stroke=0, fill=1)
    c.setFillColor(GOLD)
    c.rect(x, y + CARD_H - 36 * mm, CARD_W, 2 * mm, stroke=0, fill=1)

    c.setFillColor(white)
    c.setFont('HeiseiMin-W3', 13)
    c.drawCentredString(x + CARD_W / 2, y + CARD_H - 15 * mm, branch['name_ja'])
    c.setFont('HeiseiKakuGo-W5', 9)
    c.drawCentredString(x + CARD_W / 2, y + CARD_H - 24 * mm, 'ご注文ありがとうございました')
    c.setFont('Helvetica', 7.5)
    c.drawCentredString(x + CARD_W / 2, y + CARD_H - 30 * mm, 'Thank you for your order')

    # the offer
    c.setFillColor(CHARCOAL)
    c.setFont('HeiseiKakuGo-W5', 11)
    c.drawCentredString(x + CARD_W / 2, y + CARD_H - 50 * mm, v['headline_ja'])
    c.setFillColor(BURGUNDY)
    c.setFont('HeiseiKakuGo-W5', 16)
    c.drawCentredString(x + CARD_W / 2, y + CARD_H - 62 * mm, v['offer_ja'])
    c.setFillColor(GREY)
    c.setFont('Helvetica', 9)
    c.drawCentredString(x + CARD_W / 2, y + CARD_H - 70 * mm, v['offer_en'])

    # QR to LINE
    qr_size = 34 * mm
    c.drawImage(qr, x + (CARD_W - qr_size) / 2, y + 42 * mm, qr_size, qr_size, mask='auto')
    c.setFillColor(LINE_GREEN)
    c.setFont('Helvetica-Bold', 9)
    c.drawCentredString(x + CARD_W / 2, y + 36 * mm, 'LINE @urbanzaika')

    # phone, big — the whole point of the flyer
    c.setFillColor(CHARCOAL)
    c.setFont('HeiseiKakuGo-W5', 9)
    c.drawCentredString(x + CARD_W / 2, y + 27 * mm, 'お電話でのご注文')
    c.setFont('Helvetica-Bold', 17)
    c.drawCentredString(x + CARD_W / 2, y + 18 * mm, branch['tel'])

    c.setFillColor(GREY)
    c.setFont('Helvetica', 7)
    c.drawCentredString(x + CARD_W / 2, y + 12 * mm, f'WhatsApp {WHATSAPP}')
    c.setFont('HeiseiKakuGo-W5', 7)
    c.drawCentredString(x + CARD_W / 2, y + 7 * mm, branch['hours_ja'])
    c.setFont('Helvetica', 7)
    c.drawCentredString(x + CARD_W / 2, y + 3 * mm, 'urban-zaika.com')


def crop_marks(c, x, y):
    c.setStrokeColor(HexColor('#CCCCCC'))
    c.setLineWidth(0.3)
    m = 3 * mm
    for (px, py) in ((x, y), (x + CARD_W, y), (x, y + CARD_H), (x + CARD_W, y + CARD_H)):
        c.line(px - m, py, px - m / 3, py)
        c.line(px + m / 3, py, px + m, py)
        c.line(px, py - m, px, py - m / 3)
        c.line(px, py + m / 3, px, py + m)


def build(branch, variant):
    pdfmetrics.registerFont(UnicodeCIDFont('HeiseiKakuGo-W5'))
    pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3'))

    out = f"order-flyer-{branch['slug']}-{variant}.pdf"
    c = canvas.Canvas(out, pagesize=A4)
    page_w, page_h = A4
    qr = qr_image(LINE_URL)

    ox, oy = (page_w - 2 * CARD_W) / 2, (page_h - 2 * CARD_H) / 2
    for row in range(2):
        for col in range(2):
            x = ox + col * CARD_W
            y = oy + (1 - row) * CARD_H
            draw_flyer(c, x, y, branch, variant, qr)
            crop_marks(c, x, y)
    c.save()
    return out


if __name__ == '__main__':
    for b in BRANCHES:
        for v in VARIANTS:
            print('wrote', build(b, v))
