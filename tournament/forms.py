from django.forms import ModelForm, Textarea, TextInput, CheckboxInput, Select
from tournament.models import Tournament


class TournamentForm(ModelForm):

    class Meta:
        model = Tournament
        fields = ['name', 'description', 'location', 'game', 'status']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'class': "form-control", 'rows': "3"}),
            'location': TextInput(attrs={'class': 'form-control'}),
            'game': TextInput(attrs={'class': 'form-control'}),
            'status': Select(attrs={'class': 'form-control'}),
            }
