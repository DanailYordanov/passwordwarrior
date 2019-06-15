from django import forms
from .models import Passwords


INTEGER_CHOICES = [tuple([x, x]) for x in range(16, 34, 2)]


class CharLongForm(forms.Form):
    char_long = forms.CharField(widget=forms.Select(choices=INTEGER_CHOICES))


class PasswordCreationForm(forms.ModelForm):

    class Meta:
        model = Passwords
        fields = ['app_name', 'password']
