from django.contrib import admin
from django.urls import path, include
from password_creation import views as pass_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('users.urls'), name='accounts'),
    path('', pass_views.index, name='index'),
    path('personal-passwords/', pass_views.personal_passwords,
         name='personal-passwords'),
]
