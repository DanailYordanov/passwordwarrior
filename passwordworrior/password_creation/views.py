from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .forms import CharLongForm, PasswordCreationForm
from .models import Passwords
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
    personal_passwords_context_data = []
    user_personal_passwords = Passwords.objects.filter(user=request.user)
    for persoanl_password_object in user_personal_passwords:
        personal_password_data = {
            'password': persoanl_password_object.password,
            'app_name': persoanl_password_object.app_name,
        }
        personal_passwords_context_data.append(personal_password_data)
    context = {'personal_passwords': personal_passwords_context_data}
    return render(request, 'password_creation/personal_passwords.html', context)


def password_success(request):
    password = secrets.token_hex(int(request.POST['char_long']))
    context = {
        'password': password
    }
    return render(request, 'password_creation/password_success.html', context)


@login_required
def personal_password_creation(request):
    if request.method == 'POST':
        form = PasswordCreationForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('personal-passwords')
    else:
        form = PasswordCreationForm()
    context = {
        'form': form
    }
    return render(request, 'password_creation/personal_password_creation.html', context)


class PersonalPasswordDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Passwords
    success_url = reverse_lazy('personal-passwords')

    def test_func(self):
        personal_password = self.get_object()
        if self.request.user == personal_password.user:
            return True
        return False
