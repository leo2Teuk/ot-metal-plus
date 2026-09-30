from decimal import Decimal, ROUND_HALF_UP

VAT_RATE = Decimal('19.25')


def money(value):
    return Decimal(str(value or 0)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


def calculate_quote(products, discount, discount_type):
    clean_products = []
    subtotal = Decimal('0')
    for product in products[:15]:
        designation = str(product.get('designation', '')).strip()
        quantity = money(product.get('quantity', 0))
        unit_price = money(product.get('unit_price', 0))
        if not designation and quantity == 0 and unit_price == 0:
            continue
        line_total = money(quantity * unit_price)
        subtotal += line_total
        clean_products.append({'designation': designation, 'quantity': str(quantity), 'unit_price': str(unit_price), 'total': str(line_total)})
    requested_discount = money(discount)
    discount_amount = money(subtotal * requested_discount / 100) if discount_type == 'percent' else requested_discount
    discount_amount = min(discount_amount, subtotal)
    taxable = subtotal - discount_amount
    vat = money(taxable * VAT_RATE / 100)
    return clean_products, money(subtotal), discount_amount, vat, money(taxable + vat)
