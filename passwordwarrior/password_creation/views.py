from passwordwarrior.settings import SECRET_KEY
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    CreateView,
    UpdateView,
    ListView,
    DeleteView
)
from .forms import CharLongForm, PasswordCreationForm
from .models import Passwords
import base64
import secrets
from cryptography.fernet import Fernet


def password_generator(request):
    if request.method == 'rePOST':
        form = CharLongForm(request.POST)
        if form.is_valid():
            return redirect("password-success")
    else:
        form = CharLongForm()
    context = {
        'form': form
    }
    return render(request, 'password_creation/password_generator.html', context)


def password_success(request):
    password = secrets.token_hex(int(request.POST['char_long']))
    context = {
        'password': password
    }
    return render(request, 'password_creation/password_success.html', context)


def password_decrypter(password):
    key = base64.urlsafe_b64encode(SECRET_KEY.encode())
    f = Fernet(key)
    decrypted_password = f.decrypt(password.encode())
    return decrypted_password.decode()


@login_required
def personal_passwords(request):
    personal_passwords_context_data = []
    user_personal_passwords = Passwords.objects.filter(
        user=request.user)
    for personal_password_object in user_personal_passwords:
        personal_password_data = {
            'password': password_decrypter(personal_password_object.password),
            'app_name': personal_password_object.app_name,
            'id': personal_password_object.id,
        }
        personal_passwords_context_data.append(personal_password_data)
    context = {
        'personal_passwords': personal_passwords_context_data,
    }
    return render(request, 'password_creation/personal_passwords.html', context)


class PersonalPasswordCreateView(LoginRequiredMixin, CreateView):
    model = Passwords
    form_class = PasswordCreationForm
    template_name = 'password_creation/personal_password_creation.html'
    success_url = reverse_lazy('personal-passwords')
    view_var = 'Save a Password'
    view_button_var = 'Save'

    def get_context_data(self, **kwargs):
        context = super(PersonalPasswordCreateView,
                        self).get_context_data(**kwargs)
        context.update({'view_var': self.view_var,
                        'view_button_var': self.view_button_var})
        return context

    def form_valid(self, form):
        password = form.cleaned_data.get('password')
        key = base64.urlsafe_b64encode(SECRET_KEY.encode())
        f = Fernet(key)
        password = f.encrypt(password.encode())
        form.instance.password = password.decode()
        form.instance.user = self.request.user
        return super().form_valid(form)


class PersonalPasswordUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Passwords
    form_class = PasswordCreationForm
    template_name = 'password_creation/personal_password_creation.html'
    success_url = reverse_lazy('personal-passwords')
    view_var = 'Update a Password'
    view_button_var = 'Update'

    def get_context_data(self, **kwargs):
        context = super(PersonalPasswordUpdateView,
                        self).get_context_data(**kwargs)
        context.update({'view_var': self.view_var,
                        'view_button_var': self.view_button_var})
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Passwords, pk=self.kwargs['pk'])

    def get_initial(self):
        initial = super(PersonalPasswordUpdateView, self).get_initial()
        self.object = self.get_object()
        key = base64.urlsafe_b64encode(SECRET_KEY.encode())
        f = Fernet(key)
        decrypted_password = self.object.password
        decrypted_password = f.decrypt(decrypted_password.encode())
        initial['password'] = decrypted_password.decode()
        return initial

    def form_valid(self, form):
        password = form.cleaned_data.get('password')
        key = base64.urlsafe_b64encode(SECRET_KEY.encode())
        f = Fernet(key)
        password = f.encrypt(password.encode())
        form.instance.password = password.decode()
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        personal_password = self.get_object()
        if self.request.user == personal_password.user:
            return True
        return False


class PersonalPasswordDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Passwords
    success_url = reverse_lazy('personal-passwords')

    def test_func(self):
        personal_password = self.get_object()
        if self.request.user == personal_password.user:
            return True
        return False
