from .models import MapPick
from django import forms
from django.forms import ModelForm, TextInput, SelectMultiple, CheckboxInput


class MapPickForm(ModelForm):

    class Meta:
        model = MapPick
        fields = ['team1', 'team2', 'map_pool']
        widgets = {
            'team1': TextInput(attrs={'class': 'form-control', 'placeholder': 'Team 1 Name', }),
            'team2': TextInput(attrs={'class': 'form-control', 'placeholder': 'Team 2 Name', }),
            'map_pool': SelectMultiple(attrs={'class': 'form-control map_select'}),
        }