from Crypto.Hash import SHA256
from django import forms
from .models import Passwords, Decrypter


INTEGER_CHOICES = [tuple([x, x]) for x in range(16, 34, 2)]


class CharLongForm(forms.Form):
    char_long = forms.CharField(widget=forms.Select(choices=INTEGER_CHOICES))


class PasswordCreationForm(forms.ModelForm):

    class Meta:
        model = Passwords
        fields = ['app_name', 'password']


class DecrypterCreationForm(forms.ModelForm):

    class Meta:
        model = Decrypter
        fields = ['decrypt_key']


class CheckDecryptKeyForm(forms.Form):
    decrypt_key = forms.CharField()

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(CheckDecryptKeyForm, self).__init__(*args, **kwargs)

    def clean_decrypt_key(self):
        data = self.cleaned_data.get('decrypt_key')
        hasher = SHA256.new()
        hasher.update(data.encode())
        if self.user.decrypter.decrypt_key != hasher.hexdigest():
            raise forms.ValidationError('Incorrect decrypt key!')
        return data
