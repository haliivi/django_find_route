from django import forms
from cities.models import *
__all__ = [
    'RouteForm',
]


class RouteForm(forms.Form):
    from_city = forms.ModelChoiceField(label='Откуда', queryset=City.objects.all(), widget=forms.Select(attrs={
        'class': 'form-control select-single',
    }))
    to_city = forms.ModelChoiceField(label='Куда', queryset=City.objects.all(), widget=forms.Select(attrs={
        'class': 'form-control select-single',
    }))
    cities = forms.ModelMultipleChoiceField(label='Через города', queryset=City.objects.all(), required=False, widget=forms.SelectMultiple(attrs={
        'class': 'form-control select-multiple',
    }))
    travel_time = forms.IntegerField(label='Время в пути', widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите время в пути',
    }))
