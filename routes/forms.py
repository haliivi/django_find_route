from django import forms
from cities.models import *
from trains.models import *
from .models import *
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


class RouteModalForm(forms.ModelForm):
    name = forms.CharField(label='Название маршрута', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите название маршрута',
    }))
    from_city = forms.ModelChoiceField(queryset=City.objects.all(), widget=forms.HiddenInput())
    to_city = forms.ModelChoiceField(queryset=City.objects.all(), widget=forms.HiddenInput())
    trains = forms.ModelMultipleChoiceField(label='Куда', queryset=Train.objects.all(), widget=forms.SelectMultiple(attrs={
        'class': 'form-control d-none',
    }))
    travel_time = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = Route
        fields = '__all__'
