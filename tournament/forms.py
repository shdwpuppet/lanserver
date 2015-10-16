from django.forms import ModelForm, Textarea, TextInput, CheckboxInput, Select, SelectMultiple
from tournament.models import Tournament, Server


class TournamentForm(ModelForm):

    class Meta:
        model = Tournament
        fields = ['name', 'description', 'location', 'game', 'status', 'map_pool']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'class': "form-control", 'rows': "3"}),
            'location': TextInput(attrs={'class': 'form-control'}),
            'game': TextInput(attrs={'class': 'form-control'}),
            'status': Select(attrs={'class': 'form-control'}),
            'map_pool': SelectMultiple(attrs={'class': 'form-control'}),
            }


class ServerForm(ModelForm):

    class Meta:
        model = Server
        fields = ['name', 'ip', 'port']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'ip': Textarea(attrs={'class': "form-control"}),
            'port': TextInput(attrs={'class': 'form-control'}),
            }
