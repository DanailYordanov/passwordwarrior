from django import forms
from .models import Passwords


INTEGER_CHOICES = [tuple([x, x]) for x in range(16, 34, 2)]


class CharLongForm(forms.Form):
    char_long = forms.ChoiceField(widget=forms.Select(
        attrs={'class': 'custom-select mr-sm-2 centered', 'id': 'inlineFormCustomSelect'}), choices=INTEGER_CHOICES, required=True)


class PasswordCreationForm(forms.ModelForm):

    class Meta:
        model = Passwords
        fields = ['app_name', 'password']
