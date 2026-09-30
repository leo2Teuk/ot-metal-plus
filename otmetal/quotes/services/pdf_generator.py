from io import BytesIO
from decimal import Decimal
from pathlib import Path
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas
from pypdf import PdfReader, PdfWriter

PAGE_W, PAGE_H = 595.30, 841.90
TEMPLATE_PATH = Path(__file__).resolve().parents[3] / 'templates' / 'Devis_OT_Metal_Plus_demo.pdf'

# Coordinates are native PDF points. Text top positions were measured from the supplied A4 template.
PDF_POSITIONS = {
    'number': (82, 237), 'date': (245, 237), 'city': (407, 237),
    'client_name': (101, 310), 'telephone': (101, 329), 'address': (101, 348),
    'conditions': (138, 64), 'delivery': (138, 84), 'observations': (125, 104),
}
TABLE = {'designation_x': 70, 'quantity_x': 312, 'unit_x': 365, 'total_x': 455, 'first_baseline': 410, 'row_step': 18.7}
TOTALS = {'subtotal': (475, 713), 'discount': (475, 733), 'vat': (475, 753), 'total': (475, 773)}


def _fit(text, max_width, size=8):
    value = str(text or '')
    while size > 5 and stringWidth(value, 'Helvetica', size) > max_width:
        size -= 0.5
    return value[:120], size


def _text(pdf, value, x, top, max_width=200, size=8, bold=False):
    value, size = _fit(value, max_width, size)
    pdf.setFillColorRGB(0.05, 0.10, 0.17)
    pdf.setFont('Helvetica-Bold' if bold else 'Helvetica', size)
    pdf.drawString(x, PAGE_H - top, value)


def _cover(pdf, x, top, width, height=13):
    pdf.setFillColorRGB(1, 1, 1)
    pdf.rect(x, PAGE_H - top - height, width, height, fill=1, stroke=0)


def build_pdf(data):
    overlay = BytesIO()
    pdf = canvas.Canvas(overlay, pagesize=(PAGE_W, PAGE_H))
    pdf.setFillColorRGB(0.05, 0.10, 0.17)
    for key, width in [('number', 125), ('date', 125), ('city', 115)]:
        x, top = PDF_POSITIONS[key]
        _cover(pdf, x - 3, top - 12, width, 18)
    _text(pdf, data['number'], *PDF_POSITIONS['number'], 115, 8.5, True)
    _text(pdf, data['date'], *PDF_POSITIONS['date'], 115, 8.5, True)
    _text(pdf, data['city'], *PDF_POSITIONS['city'], 105, 8.5)
    for key, width in [('client_name', 210), ('telephone', 200), ('address', 220)]:
        x, top = PDF_POSITIONS[key]
        _cover(pdf, x - 2, top - 10, width, 13)
        _text(pdf, data.get(key, ''), x, top, width, 8.5)
    for index, product in enumerate(data.get('products', [])):
        top = TABLE['first_baseline'] + index * TABLE['row_step']
        _text(pdf, product['designation'], TABLE['designation_x'], top, 230, 7.5)
        _text(pdf, product['quantity'], TABLE['quantity_x'], top, 34, 7.5)
        _text(pdf, product['unit_price'], TABLE['unit_x'], top, 78, 7.5)
        _text(pdf, product['total'], TABLE['total_x'], top, 68, 7.5)
    for key, value in [('subtotal', data['subtotal']), ('discount', data['discount']), ('vat', data['vat']), ('total', data['total'])]:
        x, top = TOTALS[key]
        _cover(pdf, x - 5, top - 9, 78, 12)
        formatted = f'{Decimal(str(value or 0)):,.0f}'.replace(',', ' ')
        _text(pdf, formatted, x, top, 72, 8, key == 'total')
    pdf.showPage()
    for key in ['conditions', 'delivery', 'observations']:
        x, top = PDF_POSITIONS[key]
        _cover(pdf, x - 2, top - 10, 330, 13)
        _text(pdf, data.get(key, ''), x, top, 325, 8)
    pdf.save()
    overlay.seek(0)
    original = PdfReader(str(TEMPLATE_PATH))
    layer = PdfReader(overlay)
    original.pages[0].merge_page(layer.pages[0])
    original.pages[1].merge_page(layer.pages[1])
    result = BytesIO()
    writer = PdfWriter()
    for page in original.pages:
        writer.add_page(page)
    writer.write(result)
    result.seek(0)
    return result
