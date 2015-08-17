from django import forms

class RegisterForm(forms.Form):
    username = forms.CharField(label='Choose a Username', max_length=25)