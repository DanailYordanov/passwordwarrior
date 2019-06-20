from allauth.account.forms import LoginForm, SignupForm
from django import forms


class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].widget = forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'Enter email or username'})
        self.fields['password'].widget = forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Enter password'})


class CustomSignUpForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(CustomSignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Enter username'})
        self.fields['email'].widget = forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'Enter email'})
        self.fields['password1'].widget = forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Enter password'})
        self.fields['password2'].widget = forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Enter password again'})
