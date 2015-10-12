from django.forms import ModelForm, Textarea, TextInput, CheckboxInput, Select, SelectMultiple
from matches.models import Match


class MatchForm(ModelForm):

    class Meta:
        model = Match
        fields = ['home_team', 'away_team', 'map', 'division']
        widgets = {
            'home_team': Select(attrs={'class': 'form-control'}),
            'away_team': Select(attrs={'class': "form-control", 'rows': "3"}),
            'map': Select(attrs={'class': 'form-control'}),
            'division': Select(attrs={'class': 'form-control'}),
            }
