from decimal import Decimal
import json
from django.test import TestCase
from django.urls import reverse
from .models import Quote
from .services.calculations import calculate_quote


class CalculationTests(TestCase):
    def test_quote_totals(self):
        products, subtotal, discount, vat, total = calculate_quote([{'designation': 'Tôle bac', 'quantity': 20, 'unit_price': 8500}], 20000, 'fcfa')
        self.assertEqual(subtotal, Decimal('170000.00'))
        self.assertEqual(discount, Decimal('20000.00'))
        self.assertEqual(vat, Decimal('28875.00'))
        self.assertEqual(total, Decimal('178875.00'))

    def test_empty_and_maximum_rows(self):
        products, subtotal, discount, vat, total = calculate_quote([{}] * 15, 0, 'fcfa')
        self.assertEqual((products, subtotal, discount, vat, total), ([], Decimal('0.00'), Decimal('0.00'), Decimal('0.00'), Decimal('0.00')))

    def test_percentage_discount_cannot_exceed_subtotal(self):
        _, subtotal, discount, vat, total = calculate_quote([{'designation': 'Acier', 'quantity': 1, 'unit_price': 100000}], 150, 'percent')
        self.assertEqual(discount, Decimal('100000.00'))
        self.assertEqual(vat, Decimal('0.00'))
        self.assertEqual(total, Decimal('0.00'))


class QuoteSubmissionTests(TestCase):
    def test_submission_saves_and_redirects_to_pdf(self):
        response = self.client.post(reverse('new_quote'), {
            'number': 'DEV-TEST-001',
            'date': '2026-08-26',
            'city': 'Yaoundé',
            'client_name': 'Jean Dupont',
            'telephone': '690000000',
            'address': 'Yaoundé',
            'discount': '0',
            'discount_type': 'fcfa',
            'payment_terms': '',
            'delivery_time': '',
            'observations': '',
            'products': json.dumps([{'designation': 'Tôle bac', 'quantity': 20, 'unit_price': 8500}]),
        })
        quote = Quote.objects.get(number='DEV-TEST-001')
        self.assertRedirects(response, reverse('quote_pdf', args=[quote.id]))

    def test_submission_accepts_localized_display_date(self):
        response = self.client.post(reverse('new_quote'), {
            'number': 'DEV-TEST-002', 'date': '26/08/2026', 'city': 'Yaoundé',
            'client_name': 'Client test', 'telephone': '', 'address': '',
            'discount': '0', 'discount_type': 'fcfa', 'payment_terms': '',
            'delivery_time': '', 'observations': '', 'products': '[]',
        })
        self.assertEqual(response.status_code, 302)
