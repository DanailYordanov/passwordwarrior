from django import forms
from .models import Passwords


INTEGER_CHOICES = [tuple([x, x]) for x in range(16, 34, 2)]


class CharLongForm(forms.Form):
    char_long = forms.ChoiceField(widget=forms.Select(
        attrs={'class': 'custom-select mr-sm-2 centered', 'id': 'inlineFormCustomSelect'}), choices=INTEGER_CHOICES, required=True)


class PasswordCreationForm(forms.ModelForm):
    unhide_password = forms.BooleanField(widget=forms.CheckboxInput(
        attrs={'id': 'PasswordUnhide', 'onclick': 'passwordunhide();'}), required=False)

    class Meta:
        model = Passwords
        fields = ['app_name', 'password']
        widgets = {
            'app_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'AppNameInput', 'placeholder': 'Enter app name'}),
            'password': forms.TextInput(attrs={'type': 'password', 'class': 'form-control', 'id': 'AppPasswordInput', 'placeholder': 'Enter app password'}),
        }
