from .models import Team
from django.forms import ModelForm, Textarea, TextInput


class TeamForm(ModelForm):

    class Meta:
        model = Team
        fields = ['name', 'description', 'join_pass', 'website']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'class': "form-control", 'rows': "3"}),
            'join_pass': TextInput(attrs={'class': 'form-control'}),
            'website': TextInput(attrs={'class': 'form-control'}),
        }
