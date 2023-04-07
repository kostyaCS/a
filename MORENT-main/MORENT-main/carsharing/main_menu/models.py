"""
This module includes some models for database.
"""
from django.db import models
from django.contrib.auth.models import User


class Car(models.Model):
    """
    Class, that represent car.
    """
    CarModel = models.CharField(("CarModel"), max_length=100)
    Engine = models.CharField(("Engine"), max_length=50)
    BodyType = models.CharField(("BodyType"), max_length=100)
    Capacity = models.IntegerField(("Capacity"), default=4)
    Fuel = models.CharField(("Fuel"), max_length=50)
    Transmission = models.CharField(("Transmission"), max_length=50)
    Address = models.ForeignKey("Address", on_delete=models.CASCADE, null=True)
    Photo = models.ImageField(null=True, blank=True, upload_to='media/car_photos')


class Address(models.Model):
    """
    Class, that represent address, where cars can be.
    """
    Address = models.CharField(("Address"), max_length=100)
    Latitude = models.FloatField(("Latitude"), default=0)
    Longitude = models.FloatField(("Longitude"), default=0)


class TakenCar(models.Model):
    """
    Class, that represent a user's taken cars.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, default=None)
    date_taken = models.DateField(auto_now_add=True)
