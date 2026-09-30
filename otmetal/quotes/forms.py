from django import forms


class QuoteForm(forms.Form):
    number = forms.CharField(max_length=40)
    date = forms.DateField(
        input_formats=['%Y-%m-%d', '%d/%m/%Y', '%d/%m/%y'],
        widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
    )
    city = forms.CharField(max_length=100)
    client_name = forms.CharField(max_length=160)
    telephone = forms.CharField(max_length=40, required=False)
    address = forms.CharField(max_length=220, required=False)
    discount = forms.DecimalField(min_value=0, max_digits=14, decimal_places=2, initial=0)
    discount_type = forms.ChoiceField(choices=[('fcfa', 'FCFA'), ('percent', '%')])
    payment_terms = forms.CharField(max_length=180, required=False)
    delivery_time = forms.CharField(max_length=180, required=False)
    observations = forms.CharField(max_length=220, required=False)
