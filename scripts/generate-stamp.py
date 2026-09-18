#!/usr/bin/env python3
"""Generate Urban Zaika restaurant stamp designs (3 variants on one sheet).

Each stamp carries:
  - English name "URBAN ZAIKA" + katakana "アーバンザイカ"
  - Address: 5 Chome-14-6 Kamijujo 竹内荘, Kita-ku, Tokyo 114-0034
  - Phone:   03-5879-4679
"""

import math
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

pdfmetrics.registerFont(UnicodeCIDFont('HeiseiKakuGo-W5'))
JP_FONT = 'HeiseiKakuGo-W5'

OUTPUT = '/Users/pk/Downloads/Urban_Zaika_Stamp.pdf'

INK = HexColor('#9d1f1f')
BG_WHITE = white

NAME_EN = 'URBAN ZAIKA'
NAME_JP = 'アーバンザイカ'
TAGLINE = 'HALAL  \u2022  INDIAN  \u2022  PAKISTANI'
ADDR_L1 = '5 Chome-14-6 Kamijujo'
BLDG_JP = '竹内荘'
ADDR_L2 = 'Kita-ku, Tokyo 114-0034'
TEL = 'TEL  03-5879-4679'
EMAIL = 'info@urban-zaika.com'
ESTD = 'EST. 2025'


def draw_mixed_string(c, x, y, parts, size, centred=False):
    """Draw a horizontal sequence of (text, font) pieces sharing a baseline."""
    widths = [(t, f, c.stringWidth(t, f, size)) for t, f in parts]
    total = sum(w for _, _, w in widths)
    cx = x - total / 2 if centred else x
    for t, f, w in widths:
        c.setFont(f, size)
        c.drawString(cx, y, t)
        cx += w


def draw_circular_text(c, cx, cy, radius, text, font, size,
                       start_angle_deg, arc_deg, clockwise=True):
    c.setFont(font, size)
    n = len(text)
    if n == 0:
        return
    per_char = arc_deg / max(n - 1, 1) if n > 1 else 0
    for i, ch in enumerate(text):
        angle = (start_angle_deg - i * per_char) if clockwise \
            else (start_angle_deg + i * per_char)
        rad = math.radians(angle)
        x = cx + radius * math.cos(rad)
        y = cy + radius * math.sin(rad)
        c.saveState()
        c.translate(x, y)
        c.rotate(angle - 90 if clockwise else angle + 90)
        c.drawCentredString(0, 0, ch)
        c.restoreState()


def draw_halal_mark(c, cx, cy, r, ink=INK, bg=BG_WHITE):
    """Crescent moon + small 5-point star (classic halal symbol)."""
    c.setFillColor(ink)
    c.circle(cx, cy, r, fill=1, stroke=0)
    c.setFillColor(bg)
    c.circle(cx + r * 0.38, cy + r * 0.05, r * 0.85, fill=1, stroke=0)

    star_cx = cx + r * 1.35
    star_cy = cy
    star_r = r * 0.55
    c.setFillColor(ink)
    path = c.beginPath()
    for i in range(10):
        theta = math.pi / 2 + i * math.pi / 5
        rr = star_r if i % 2 == 0 else star_r * 0.4
        x = star_cx + rr * math.cos(theta)
        y = star_cy + rr * math.sin(theta)
        if i == 0:
            path.moveTo(x, y)
        else:
            path.lineTo(x, y)
    path.close()
    c.drawPath(path, fill=1, stroke=0)


def draw_round_stamp(c, cx, cy, r_outer=24*mm):
    c.setStrokeColor(INK)
    c.setFillColor(INK)
    c.setLineWidth(1.3)
    c.circle(cx, cy, r_outer, stroke=1, fill=0)
    c.setLineWidth(0.6)
    c.circle(cx, cy, r_outer - 1.8*mm, stroke=1, fill=0)
    c.circle(cx, cy, r_outer - 10.5*mm, stroke=1, fill=0)

    draw_circular_text(c, cx, cy, r_outer - 5.0*mm,
                       NAME_EN, 'Helvetica-Bold', 9,
                       start_angle_deg=135, arc_deg=90, clockwise=True)
    draw_circular_text(c, cx, cy, r_outer - 5.0*mm,
                       TAGLINE, 'Helvetica-Bold', 5.2,
                       start_angle_deg=-135, arc_deg=90, clockwise=False)

    c.setFillColor(INK)
    c.setFont(JP_FONT, 7)
    c.drawCentredString(cx, cy + 5*mm, NAME_JP)

    c.setFont('Helvetica-Bold', 5.5)
    c.drawCentredString(cx, cy + 1.2*mm, 'TOKYO')

    draw_mixed_string(c, cx, cy - 2*mm, [
        ('5-14-6 Kamijujo  ', 'Helvetica'),
        (BLDG_JP, JP_FONT),
    ], 4.5, centred=True)
    c.setFont('Helvetica', 4.5)
    c.drawCentredString(cx, cy - 4.5*mm, 'Kita-ku  114-0034')
    c.setFont('Helvetica-Bold', 5)
    c.drawCentredString(cx, cy - 7.5*mm, 'TEL 03-5879-4679')


def draw_square_stamp(c, cx, cy, size=40*mm):
    half = size / 2
    c.setStrokeColor(INK)
    c.setFillColor(INK)
    c.setLineWidth(1.4)
    c.rect(cx - half, cy - half, size, size, stroke=1, fill=0)
    c.setLineWidth(0.6)
    c.rect(cx - half + 1.2*mm, cy - half + 1.2*mm,
           size - 2.4*mm, size - 2.4*mm, stroke=1, fill=0)

    c.setFillColor(INK)
    c.setFont('Helvetica-Bold', 9)
    c.drawCentredString(cx, cy + 9*mm, 'URBAN ZAIKA')

    c.setFont(JP_FONT, 7.5)
    c.drawCentredString(cx, cy + 4.5*mm, NAME_JP)

    c.setFont('Helvetica', 5)
    c.drawCentredString(cx, cy + 0.8*mm, 'HALAL  \u2022  INDIAN & PAKISTANI')

    c.setLineWidth(0.4)
    c.line(cx - half + 3*mm, cy - 1.5*mm, cx + half - 3*mm, cy - 1.5*mm)

    draw_mixed_string(c, cx, cy - 4.5*mm, [
        (ADDR_L1 + '  ', 'Helvetica'),
        (BLDG_JP, JP_FONT),
    ], 5.5, centred=True)
    c.setFont('Helvetica', 5.5)
    c.drawCentredString(cx, cy - 7*mm, ADDR_L2)
    c.setFont('Helvetica-Bold', 6)
    c.drawCentredString(cx, cy - 10.5*mm, 'TEL  03-5879-4679')


def draw_rect_stamp(c, cx, cy, w=100*mm, h=35*mm):
    c.setStrokeColor(INK)
    c.setFillColor(INK)
    c.setLineWidth(1.3)
    c.rect(cx - w/2, cy - h/2, w, h, stroke=1, fill=0)
    c.setLineWidth(0.4)
    c.rect(cx - w/2 + 1.1*mm, cy - h/2 + 1.1*mm,
           w - 2.2*mm, h - 2.2*mm, stroke=1, fill=0)

    c.setFillColor(INK)
    c.setFont('Helvetica-Bold', 12)
    c.drawString(cx - w/2 + 3.5*mm, cy + h/2 - 6*mm, 'Urban Zaika')

    c.setFont(JP_FONT, 8)
    c.drawString(cx - w/2 + 3.5*mm, cy + h/2 - 11.5*mm, NAME_JP)

    c.setFont('Helvetica', 6)
    c.drawString(cx + 3*mm, cy + h/2 - 11*mm,
                 'HALAL  \u2022  INDIAN & PAKISTANI')

    c.setLineWidth(0.4)
    c.line(cx - w/2 + 3.5*mm, cy + h/2 - 14*mm,
           cx + w/2 - 3.5*mm, cy + h/2 - 14*mm)

    draw_mixed_string(c, cx - w/2 + 3.5*mm, cy + h/2 - 17.5*mm, [
        (ADDR_L1 + '  ', 'Helvetica'),
        (BLDG_JP, JP_FONT),
    ], 6.5)
    c.setFont('Helvetica', 6.5)
    c.drawString(cx - w/2 + 3.5*mm, cy + h/2 - 20.5*mm, ADDR_L2)
    c.setFont('Helvetica-Bold', 6.5)
    c.drawString(cx - w/2 + 3.5*mm, cy + h/2 - 24*mm, TEL)
    c.setFont('Helvetica', 6.5)
    c.drawString(cx + 4*mm, cy + h/2 - 24*mm, EMAIL)


def draw_label(c, cx, y, text):
    c.setFillColor(HexColor('#333333'))
    c.setFont('Helvetica', 8)
    c.drawCentredString(cx, y, text)


def main():
    c = canvas.Canvas(OUTPUT, pagesize=A4)
    page_w, page_h = A4

    c.setFillColor(HexColor('#1a1a1a'))
    c.setFont('Helvetica-Bold', 16)
    c.drawCentredString(page_w/2, page_h - 20*mm,
                        'Urban Zaika \u2014 Stamp Designs')
    c.setFillColor(HexColor('#666666'))
    c.setFont('Helvetica', 9)
    c.drawCentredString(page_w/2, page_h - 26*mm,
                        'Three variants \u2014 English, katakana, address '
                        '& phone (traditional red ink).')

    draw_round_stamp(c, page_w/2 - 55*mm, page_h - 70*mm, r_outer=24*mm)
    draw_label(c, page_w/2 - 55*mm, page_h - 100*mm,
               '1. Round Seal  \u2014  48mm dia.  \u2014  '
               'for receipts / packaging')

    draw_square_stamp(c, page_w/2 + 55*mm, page_h - 70*mm, size=40*mm)
    draw_label(c, page_w/2 + 55*mm, page_h - 100*mm,
               '2. Square Stamp  \u2014  40mm  \u2014  '
               'for official documents')

    draw_rect_stamp(c, page_w/2, page_h - 140*mm, w=100*mm, h=35*mm)
    draw_label(c, page_w/2, page_h - 164*mm,
               '3. Address Rubber Stamp  \u2014  100x35mm  \u2014  '
               'for invoices / forms')

    c.setFillColor(HexColor('#333333'))
    c.setFont('Helvetica-Bold', 10)
    c.drawString(22*mm, 70*mm, 'Business Details (as designed):')
    c.setFont('Helvetica', 9)
    info_y = 63*mm
    lines = [
        ('Name (EN):  ', 'Urban Zaika  \u2013  Halal Indian & Pakistani Restaurant'),
        ('Name (JP):  ', NAME_JP, JP_FONT),
        ('Address:    ', f'{ADDR_L1}  {BLDG_JP}, {ADDR_L2}', JP_FONT),
        ('Phone:      ', '03-5879-4679'),
        ('Email:      ', 'info@urban-zaika.com'),
        ('Ink color:  ', 'Traditional Japanese red (#9d1f1f)'),
    ]
    for entry in lines:
        c.setFont('Helvetica', 9)
        c.drawString(22*mm, info_y, entry[0])
        if len(entry) == 3:
            c.setFont(entry[2], 9)
        c.drawString(42*mm, info_y, entry[1])
        info_y -= 5*mm

    c.setFillColor(HexColor('#999999'))
    c.setFont('Helvetica', 7)
    c.drawCentredString(page_w/2, 15*mm,
                        'Designs are vector, scale without quality loss. '
                        'Take to any hanko / rubber stamp shop in Tokyo.')

    c.showPage()
    c.save()
    print(f"Generated: {OUTPUT}")


if __name__ == '__main__':
    main()
