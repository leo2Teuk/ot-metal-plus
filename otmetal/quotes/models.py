from django.db import models


class Quote(models.Model):
    number = models.CharField(max_length=40, unique=True)
    date = models.DateField()
    city = models.CharField(max_length=100, default='Yaoundé')
    client_name = models.CharField(max_length=160)
    telephone = models.CharField(max_length=40, blank=True)
    address = models.CharField(max_length=220, blank=True)
    products = models.JSONField(default=list)
    discount = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    discount_type = models.CharField(max_length=7, choices=[('fcfa', 'FCFA'), ('percent', '%')], default='fcfa')
    payment_terms = models.CharField(max_length=180, blank=True)
    delivery_time = models.CharField(max_length=180, blank=True)
    observations = models.CharField(max_length=220, blank=True)
    subtotal = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    vat = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.number} - {self.client_name}'
