"""
Module for admin registration of models.
"""
from django.contrib import admin
from .models import Car, Address, TakenCar

admin.site.register(Car)
admin.site.register(Address)
admin.site.register(TakenCar)