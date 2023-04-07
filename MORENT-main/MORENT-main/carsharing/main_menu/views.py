"""
Main module that represent functions, which help user to navigate through web application.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from django.core.mail import EmailMessage
from django.conf import settings
from logregapp.views import login, register, signout
import emoji
from .models import Car, TakenCar
from .find_distance import distance_betweeen_points, make_a_map_of_distances

USER_LOCATION = ''

def main_page(request: HttpRequest):
    """
    This function represent main logic of web application, with rendering
    to login, registration and observing car pages.
    """
    all_shown_popular = False
    all_shown_recomended = False
    cars_popular, cars_recomended = get_cars_from_database(request)
    data = dict()
    is_search1_started = False
    used_cars_popular = []
    used_cars_recomended = []
    for i in range(4):
        used_cars_popular.append(cars_popular[i])
    for i in range(8):
        used_cars_recomended.append(cars_recomended[i])
    data['cars_popular'] = used_cars_popular
    data['cars_recomended'] = used_cars_recomended
    if request.method == 'POST':
        if 'login' in request.POST:
            return redirect(login)
        elif 'register' in request.POST:
            return redirect(register)
        elif 'search' in request.POST:
            is_search1_started = True
            input_adress = request.POST.get('adress_pick_up1')
            global USER_LOCATION
            USER_LOCATION = input_adress
            data['current_street'] = input_adress
            input_adress += " Львів"
            cars = Car.objects.all()
            adrs_to_sort = []
            for car in cars:
                try:
                    photo_path = car.Photo.url
                    dist = distance_betweeen_points(car.Address.Address, input_adress)
                    if dist.split()[1] == "km":
                        dist = float(dist.split()[0])
                    else:
                        dist = float(dist.split()[0])/1000
                    if dist <= 1:
                        color = "green"
                    elif 1 < dist <= 2:
                        color = 'yellow'
                    else:
                        color = 'red'
                    adrs_to_sort.append((car, photo_path, dist, color))
                except Exception:
                    continue
            adrs_to_sort = sorted(adrs_to_sort, key=lambda x: x[2])
            data['car_tuples'] = adrs_to_sort[:8]
        elif 'view_more' in request.POST:
            data['cars_popular'] = cars_popular
            all_shown_popular = True
        elif 'view_less' in request.POST:
            new_used_cars_popular = []
            for i in range(4):
                new_used_cars_popular.append(cars_popular[i])
            data['cars_popular'] = new_used_cars_popular
            all_shown_popular = False
        elif 'view_more1' in request.POST:
            all_shown_recomended = True
            data['cars_recomended'] = cars_recomended
        elif 'view_less2' in request.POST:
            all_shown_recomended = False
            new_used_cars_recomended = []
            for i in range(8):
                new_used_cars_recomended.append(cars_recomended[i])
            data['cars_recomended'] = new_used_cars_recomended
        else:
            for car in Car.objects.all():
                if car.CarModel in request.POST:
                    return redirect("observe", pk=car.pk)
    is_authorized = True
    if request.user.username == "":
        is_authorized = False
    data['is_authorized'] = is_authorized
    data['all_shown_popular'] = all_shown_popular
    data['all_shown_recomended'] = all_shown_recomended
    data['is_search1_started'] = is_search1_started
    return render(request, 'main_menu/index.html', data)

def auth_login(request: HttpRequest):
    """
    This function manipulates with user, who are already authorized, rendering
    him to login page with info or payment history.
    """
    username = request.user.username
    useremail = request.user.get_email_field_name()
    if request.method == 'POST':
        if 'payment' in request.POST:
            cars = TakenCar.objects.filter(user=request.user)
            return render(request, 'logregapp/payment_history.html', {"cars": cars[::-1]})
        if 'logout' in request.POST:
            signout(request)
            return redirect(main_page)
    return render(request, 'main_menu/login.html', {"username": username, 'useremail': useremail})

def profile(request: HttpRequest):
    """
    This function checks if the user are already authorized
    and renders him to the main page.
    """
    if request.method == 'POST':
        signout(request)
        return redirect(main_page)
    return redirect(auth_login)

def get_cars_from_database(request: HttpRequest):
    """
    This function gets cars from database if user tups buttons
    'view more'.
    """
    cars = Car.objects.all()
    car_models_popular = cars[:20]
    car_models_recommend = cars[21:45]
    return car_models_popular, car_models_recommend

def observe(request: HttpRequest, pk: int):
    """
    This function is responsible for observing a car, that user wants to.
    """
    car = get_object_or_404(Car, pk=pk)
    if request.method == 'POST':
        if 'login' in request.POST:
            return redirect(login)
        elif 'register' in request.POST:
            return redirect(register)
        elif 'rent_now' in request.POST:
            return redirect(rent_car, pk=car.pk)
    return render(request, 'main_menu/observe.html', {'car': car})

def rent_car(request: HttpRequest, pk: int):
    """
    This function represent logic on the page, when the user wants to
    rent a car, also send gmail when rented.
    """
    global USER_LOCATION
    car = get_object_or_404(Car, pk=pk)
    if request.method == 'POST':
        if 'submit' in request.POST:
            try:
                TakenCar.objects.create(user=request.user, car=car)
                make_a_map_of_distances(USER_LOCATION + ' Львів', car.Address.Address + ' Львів')
                email = EmailMessage(
                'successful car rental', # subject of the email
                f'Dear {request.user.username}! You have succesfuly rented {car.CarModel}!\n'
                'In attached images, you have a map to see how you can get to it!\n'
                'Have a lucky ride!\n'
                f'{emoji.emojize("P.S. With love, MORENT :red_heart:")}\n', # body of the email
                settings.EMAIL_HOST_USER,
                [request.user.email],
            )
                with open('out.png', 'rb') as file_to_read:
                    image_data = file_to_read.read()
                    email.attach('image.jpg', image_data, 'image/jpeg')
                    email.send()
                    return render(request, 'main_menu/rented.html', {})
            except Exception:
                return render(request, 'main_menu/rented.html', {})
    return render(request, 'main_menu/rent.html', {"car": car})
