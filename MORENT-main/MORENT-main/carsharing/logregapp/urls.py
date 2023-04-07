from django.urls import path
from . import views as logregapp_views
from main_menu import views as main_menu_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', logregapp_views.register, name='register'),
    path('login/', logregapp_views.login, name='login'),
    path('profile/', main_menu_views.profile, name='profile'),
]