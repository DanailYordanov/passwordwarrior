from django.urls import path
from . import views as pass_views

urlpatterns = [
    path('', pass_views.password_generator, name='password-generator'),
    path('personal-passwords/', pass_views.personal_passwords,
         name='personal-passwords'),
    path('success/', pass_views.password_success, name='password-success'),
    path('personal-password/create/', pass_views.PersonalPasswordCreateView.as_view(),
         name='personal-password-creation'),
    path('personal-password/<int:pk>/update/',
         pass_views.PersonalPasswordUpdateView.as_view(), name='personal-password-update'),
    path('personal-password/<int:pk>/delete/',
         pass_views.PersonalPasswordDeleteView.as_view(), name='personal-password-delete'),
]
