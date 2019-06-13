from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('users.urls'), name='accounts'),
    path('', include('password_creation.urls'))
]
