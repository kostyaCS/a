from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='main'),
    path('observe/<int:pk>/', views.observe, name='observe'),
    path('auth_login/', views.auth_login, name='auth_login'),
    path('rent_car/<int:pk>/', views.rent_car, name='rent_car')
]
