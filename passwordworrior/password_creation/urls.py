from django.urls import path
from . import views as pass_views

urlpatterns = [
    path('', pass_views.password_generator, name='password-generator'),
    path('personal-passwords/', pass_views.personal_passwords,
         name='personal-passwords'),
    path('success/', pass_views.password_success, name='password-success'),
    path('password-creation/', pass_views.personal_password_creation,
         name='personal-password-creation'),
    #     path('personal-password/<int:id>/delete',
    #          pass_views.personal_password_delete, name='personal-password-delete'),
    path('personal-password/<int:pk>/delete',
         pass_views.PersonalPasswordDeleteView.as_view(), name='personal-password-delete')
]
