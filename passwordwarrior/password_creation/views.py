from passwordwarrior.settings import SECRET_KEY
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView
)
from .forms import CharLongForm, PasswordCreationForm, CheckDecryptKeyForm
from .models import Passwords, Decrypter
import secrets


def password_generator(request):
    if request.method == 'POST':
        form = CharLongForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect(reverse("password-success"))
    else:
        form = CharLongForm()
    context = {
        'form': form
    }
    return render(request, 'password_creation/password_generator.html', context)


@login_required
def personal_passwords(request):
    context = {}
    if request.method == 'POST':
        form = CheckDecryptKeyForm(request.POST, user=request.user)
        context['form'] = form
        if form.is_valid():
            personal_passwords_context_data = []
            user_personal_passwords = Passwords.objects.filter(
                user=request.user)
            for personal_password_object in user_personal_passwords:
                personal_password_data = {
                    'password': personal_password_object.password,
                    'app_name': personal_password_object.app_name,
                    'id': personal_password_object.id,
                }
                personal_passwords_context_data.append(personal_password_data)
            context['personal_passwords'] = personal_passwords_context_data
    else:
        form = CheckDecryptKeyForm(user=request.user)
        context['form'] = form
    return render(request, 'password_creation/personal_passwords.html', context)


def password_success(request):
    password = secrets.token_hex(int(request.POST['char_long']))
    context = {
        'password': password
    }
    return render(request, 'password_creation/password_success.html', context)


class PersonalPasswordCreateView(LoginRequiredMixin, CreateView):
    model = Passwords
    fields = ['app_name', 'password']
    template_name = 'password_creation/personal_password_creation.html'
    success_url = reverse_lazy('personal-passwords')

    def form_valid(self, form):
        user_decrypt_key = 
        password = form.cleaned_data.get('password')
        cipher = AES.new(key)
        form.instance.user = self.request.user
        return super().form_valid(form)


class PersonalPasswordUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Passwords
    fields = ['app_name', 'password']
    template_name = 'password_creation/personal_password_creation.html'
    success_url = reverse_lazy('personal-passwords')

    def form_valid(self, form):
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


class DecrypterCreateView(LoginRequiredMixin, CreateView):
    model = Decrypter
    fields = ('decrypt_key',)
    template_name = 'password_creation/decrypter_create.html'
    success_url = reverse_lazy('personal-password-creation')

    def form_valid(self, form):
        decrypt_key = form.cleaned_data.get('decrypt_key')
        cipher = AES.new(SECRET_KEY, AES.MODE_ECB)
        encrypted_key = cipher.encrypt(decrypt_key)
        form.instance.decrypt_key = encrypted_key
        form.instance.user = self.request.user
        return super().form_valid(form)
