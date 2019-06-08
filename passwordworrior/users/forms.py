from allauth.account.forms import LoginForm
from django import forms


class CustomLoginForm(LoginForm):

    def login(self, *args, **kwargs):
        self.fields['login'].widget = forms.TextInput(
            attrs={'type': 'email', 'placeholder': 'Enter email or username !'})
        self.fields['password'].widget = forms.PasswordInput(
            attrs={'type': 'password', 'placeholder': 'Enter password !'})
        return super(CustomLoginForm, self).login(*args, **kwargs)
