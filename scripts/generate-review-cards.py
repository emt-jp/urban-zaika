"""
Print-ready Google review cards for both Urban Zaika branches.

Each branch gets an A4 sheet of 8 cards (85 x 55 mm, business-card size) carrying a QR code
that opens the Google review form for that branch directly. Cut along the crop marks and put
them on tables, in takeaway bags, or with the bill.

Review links come from the branch's Business Profile ("Get more reviews"), so the QR opens the
star-rating dialog straight away rather than the listing.

Usage:
    .venv-tools/bin/python scripts/generate-review-cards.py
    -> review-cards-edogawa.pdf, review-cards-kita-ku.pdf

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
GREY = HexColor('#6B6B6B')

CARD_W, CARD_H = 85 * mm, 55 * mm
COLS, ROWS = 2, 4

BRANCHES = [
    {
        'slug': 'edogawa',
        'name_ja': 'Urban Zaika 上一色店',
        'name_en': 'Urban Zaika Kamiisshiki',
        'area_ja': '江戸川区上一色1-8-21',
        'tel': '03-5879-4679',
        # Business Profile → Get more reviews
        'review_url': 'https://g.page/r/Cc_Q4VyB6-cyEBM/review',
    },
    {
        'slug': 'kita-ku',
        'name_ja': 'Urban Zaika 十条店',
        'name_en': 'Urban Zaika Jujo',
        'area_ja': '北区上十条5-14-6',
        'tel': '080-3480-6994',
        'review_url': 'https://g.page/r/CVF5aEwTWcDQEBM/review',
    },
]


def qr_image(url):
    """QR as an ImageReader, sized for print (error correction H so a logo-free centre still scans)."""
    qr = segno.make(url, error='h')
    buf = io.BytesIO()
    qr.save(buf, kind='png', scale=20, border=1, dark='#1A1A1A', light='#FFFFFF')
    buf.seek(0)
    return ImageReader(buf)


def draw_card(c, x, y, branch, qr):
    """One card with its origin at the bottom-left corner."""
    c.setFillColor(white)
    c.rect(x, y, CARD_W, CARD_H, stroke=0, fill=1)

    # gold rule along the top
    c.setFillColor(GOLD)
    c.rect(x, y + CARD_H - 3 * mm, CARD_W, 3 * mm, stroke=0, fill=1)

    # QR on the right
    qr_size = 34 * mm
    qr_x = x + CARD_W - qr_size - 6 * mm
    qr_y = y + (CARD_H - qr_size) / 2 - 1 * mm
    c.drawImage(qr, qr_x, qr_y, qr_size, qr_size, mask='auto')

    # text block on the left
    tx = x + 7 * mm
    c.setFillColor(BURGUNDY)
    c.setFont('HeiseiMin-W3', 10)
    c.drawString(tx, y + CARD_H - 13 * mm, branch['name_ja'])

    c.setFillColor(CHARCOAL)
    c.setFont('HeiseiKakuGo-W5', 9.5)
    c.drawString(tx, y + CARD_H - 23 * mm, 'クチコミを')
    c.drawString(tx, y + CARD_H - 30 * mm, 'お願いします')

    c.setFillColor(GREY)
    c.setFont('Helvetica', 7.5)
    c.drawString(tx, y + CARD_H - 37.5 * mm, 'Scan to leave a Google review')

    c.setFillColor(CHARCOAL)
    c.setFont('HeiseiKakuGo-W5', 6.5)
    c.drawString(tx, y + 7 * mm, branch['area_ja'])
    c.setFont('Helvetica', 6.5)
    c.drawString(tx, y + 3.5 * mm, f"TEL {branch['tel']}  ·  urban-zaika.com")


def crop_marks(c, x, y):
    c.setStrokeColor(HexColor('#CCCCCC'))
    c.setLineWidth(0.3)
    m = 3 * mm
    for (px, py) in ((x, y), (x + CARD_W, y), (x, y + CARD_H), (x + CARD_W, y + CARD_H)):
        c.line(px - m, py, px - m / 3, py)
        c.line(px + m / 3, py, px + m, py)
        c.line(px, py - m, px, py - m / 3)
        c.line(px, py + m / 3, px, py + m)


def build(branch):
    pdfmetrics.registerFont(UnicodeCIDFont('HeiseiKakuGo-W5'))
    pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3'))

    out = f"review-cards-{branch['slug']}.pdf"
    c = canvas.Canvas(out, pagesize=A4)
    page_w, page_h = A4
    qr = qr_image(branch['review_url'])

    grid_w, grid_h = COLS * CARD_W, ROWS * CARD_H
    ox, oy = (page_w - grid_w) / 2, (page_h - grid_h) / 2

    for row in range(ROWS):
        for col in range(COLS):
            x = ox + col * CARD_W
            y = oy + (ROWS - 1 - row) * CARD_H
            draw_card(c, x, y, branch, qr)
            crop_marks(c, x, y)

    c.setFillColor(GREY)
    c.setFont('Helvetica', 7)
    c.drawCentredString(page_w / 2, 10 * mm, f"{branch['name_en']} — Google review cards — {branch['review_url']}")
    c.save()
    return out


if __name__ == '__main__':
    for b in BRANCHES:
        print('wrote', build(b))
