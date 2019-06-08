from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CharLongForm, PasswordCreationForm
from .models import Passwords
import secrets


def index(request):
    context = {}
    if request.method == 'POST' and 'charlongbutton' in request.POST:
        form = CharLongForm(request.POST)
        context['form'] = form

        if form.is_valid():
            char_long = form.cleaned_data.get('char_long')
            password = secrets.token_hex(int(char_long))
            context['password'] = password
            context['type'] = 'submit'

            if request.method == 'POST' and 'passwordsavebutton' in request.POST:
                print(request.POST)
                # populated_data = {
                #     'user': request.user,
                #     'app_name': request.POST.get('app_name'),
                #     'password': password
                # }
                personal_pass_form = PasswordCreationForm(
                    request.POST)
                context['personal_pass_form'] = personal_pass_form
                if personal_pass_form.is_valid():
                    personal_pass_form.instance.user = request.user
                    personal_pass_form.save()
                    return redirect('personal-passwords')

            else:
                personal_pass_form = PasswordCreationForm()
                context['personal_pass_form'] = personal_pass_form

    else:
        form = CharLongForm()
        context['form'] = form
        context['type'] = 'hidden'

    return render(request, 'password_creation/index.html', context)


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


# @login_required
# def password_creation(request):
#     if request.method == 'POST':
#         populated_data = {
#             'char_long': request.POST['char_long'],
#             'app_name': request.POST['app_name'],
#             'password':
#         }
#         form = PasswordCreationForm(request.POST)

# def index(request):
#     context = {}
#     if request.method == 'POST':
#         form = CharLongForm(request.POST)
#         context['form'] = form

#         if form.is_valid():
#             char_long = form.cleaned_data.get('char_long')
#             password = secrets.token_hex(int(char_long))
#             context['password'] = password
#             context['type'] = 'submit'

#             if request.method == 'POST':
#                 # populated_data = {
#                 #     'user': request.user,
#                 #     'app_name': request.POST.get('app_name'),
#                 #     'password': password
#                 # }

#                 personal_pass_form = PasswordCreationForm(
#                     request.POST)
#                 personal_pass_form.instance.user = request.user
#                 context['personal_pass_form'] = personal_pass_form

#                 if personal_pass_form.is_valid():
#                     personal_pass_form.save()
#                     return redirect('personal-passwords')

#             else:
#                 personal_pass_form = PasswordCreationForm()
#                 context['personal_pass_form'] = personal_pass_form

#     else:
#         form = CharLongForm()
#         context['form'] = form
#         context['type'] = 'hidden'

#     return render(request, 'password_creation/index.html', context)
