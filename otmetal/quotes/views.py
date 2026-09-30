import json
from datetime import date
from decimal import Decimal
from django.contrib import messages
from django.http import FileResponse
from django.shortcuts import get_object_or_404, redirect, render
from .forms import QuoteForm
from .models import Quote
from .services.calculations import calculate_quote
from .services.pdf_generator import build_pdf


def next_number():
    return f'DEV-{date.today().year}-{Quote.objects.count() + 1:03d}'


def quote_payload(quote):
    return {'number': quote.number, 'date': quote.date.strftime('%d / %m / %Y'), 'city': quote.city,
            'client_name': quote.client_name, 'telephone': quote.telephone, 'address': quote.address,
            'products': quote.products, 'subtotal': quote.subtotal, 'discount': quote.discount,
            'vat': quote.vat, 'total': quote.total, 'conditions': quote.payment_terms,
            'delivery': quote.delivery_time, 'observations': quote.observations}


def new_quote(request):
    initial = {'number': next_number(), 'date': date.today(), 'city': 'Yaoundé', 'discount': 0, 'discount_type': 'fcfa'}
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            try:
                products = json.loads(request.POST.get('products', '[]'))
                clean, subtotal, discount, vat, total = calculate_quote(products, form.cleaned_data['discount'], form.cleaned_data['discount_type'])
            except (ValueError, TypeError, json.JSONDecodeError):
                form.add_error(None, 'Les lignes de produits sont invalides.')
            else:
                if request.GET.get('preview') == '1':
                    payload = {'number': form.cleaned_data['number'], 'date': form.cleaned_data['date'].strftime('%d / %m / %Y'), 'city': form.cleaned_data['city'], 'client_name': form.cleaned_data['client_name'], 'telephone': form.cleaned_data['telephone'], 'address': form.cleaned_data['address'], 'products': clean, 'subtotal': subtotal, 'discount': discount, 'vat': vat, 'total': total, 'conditions': form.cleaned_data['payment_terms'], 'delivery': form.cleaned_data['delivery_time'], 'observations': form.cleaned_data['observations']}
                    return FileResponse(build_pdf(payload), content_type='application/pdf')
                quote = Quote.objects.create(number=form.cleaned_data['number'], date=form.cleaned_data['date'], city=form.cleaned_data['city'], client_name=form.cleaned_data['client_name'], telephone=form.cleaned_data['telephone'], address=form.cleaned_data['address'], products=clean, discount=discount, discount_type=form.cleaned_data['discount_type'], payment_terms=form.cleaned_data['payment_terms'], delivery_time=form.cleaned_data['delivery_time'], observations=form.cleaned_data['observations'], subtotal=subtotal, vat=vat, total=total)
                messages.success(request, 'Devis enregistré avec succès.')
                return redirect('quote_pdf', quote_id=quote.id)
    else:
        form = QuoteForm(initial=initial)
    return render(request, 'quotes/new_quote.html', {'form': form, 'today': date.today().isoformat(), 'next_number': initial['number']})


def history(request):
    return render(request, 'quotes/history.html', {'quotes': Quote.objects.all()})


def quote_pdf(request, quote_id):
    quote = get_object_or_404(Quote, id=quote_id)
    response = FileResponse(build_pdf(quote_payload(quote)), content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="Devis_{quote.number}.pdf"'
    return response


def duplicate_quote(request, quote_id):
    quote = get_object_or_404(Quote, id=quote_id)
    quote.pk = None
    quote.number = next_number()
    quote.save()
    return redirect('new_quote')


def delete_quote(request, quote_id):
    if request.method == 'POST':
        get_object_or_404(Quote, id=quote_id).delete()
    return redirect('history')
