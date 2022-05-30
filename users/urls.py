"""Визначити регулярні вирази URL"""

from django.urls import path, include

from . import views

app_name = 'users'
urlpatterns = [
    # додати уставні урл автентифікації
    path('', include('django.contrib.auth.urls')),
    # сторінка реєстрації
    path('register/', views.register, name='register'),
]
