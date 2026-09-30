from django.urls import path
from . import views

urlpatterns = [
    path('', views.new_quote, name='new_quote'),
    path('historique/', views.history, name='history'),
    path('devis/<int:quote_id>/pdf/', views.quote_pdf, name='quote_pdf'),
    path('devis/<int:quote_id>/dupliquer/', views.duplicate_quote, name='duplicate_quote'),
    path('devis/<int:quote_id>/supprimer/', views.delete_quote, name='delete_quote'),
]
