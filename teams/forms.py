from .models import Team
from django.forms import ModelForm, Textarea, TextInput, SelectMultiple


class TeamForm(ModelForm):

    class Meta:
        model = Team
        fields = ['name', 'description', 'join_pass', 'website']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'class': "form-control", 'rows': "3"}),
            'map_pool': SelectMultiple(attrs={'class': 'form-control'}),
        }
