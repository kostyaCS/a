"""
Module, that represent a user's registration and authorization.
"""
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpRequest
import re


# CURRENT_USER = User(username="Guest")

def is_valid_email(email):
    """
    Returns True if email is valid, otherwise False.
    """
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(regex, email))

def check_email(email):
    """
    Function checks if emai already exists.
    """
    try:
        _ = User.objects.get(email=email)
    except User.DoesNotExist:
        return True
    return False

def login(request: HttpRequest):
    """
    Function that helps user to login to his account.
    """
    print(request.user.username)
    if request.method == "POST":
        print(request.POST)
        print(request.user.username)
        if request.user.username != "":
            return redirect("main")
        username = request.POST['username']
        print(username)
        password = request.POST['password']
        print(password)

        # Creating dictionary for rendering html template
        data = {
            "warning": "",
        }

        user = authenticate(username=username, password=password)

        if user is not None:
            if 'payment' in request.POST:
                return render(request, 'logregapp/payment_history.html', {})
            auth_login(request, user)
            print(request.user.username)
            return redirect("main")
        else:
            data['warning'] = 'Wrong username or password'
            return render(request, 'logregapp/login.html', data)
    return render(request, 'logregapp/login.html', {})

def register(request: HttpRequest):
    """
    This function helps user to register.
    """
    if request.user.username != "":
        return render(request, 'main_menu/index.html', {})
    if request.method == "POST":
        print(request.POST)
        username = request.POST['username']
        email = request.POST['mail']
        password1 = request.POST['password']
        password2 = request.POST['confirm_password']
        data = {
            "username": "",
            "email": "",
            "password": "",
            "un_warning": "",
            "e_warning": "",
            "p_warning": ""
        }
        if (username == '' or User.objects.filter(username=username).exists() or
            email == '' or not is_valid_email(email) or not check_email(email) or
            len(password1) < 8 or password1 != password2):
            if username == "":
                data['un_warning'] = "The username field is empty"
            if User.objects.filter(username=username).exists():
                data['un_warning'] = "The username is already taken"
            if email == "":
                data['e_warning'] = "The email field is empty"
            if check_email(email) == False:
                data['e_warning'] = "The amail is alredy taken"
            if is_valid_email(email) == False:
                data['e_warning'] = "The input email doesn't exist"
            if password1 != password2:
                data['p_warning'] = "Passwords are not the same"
            if len(password1) < 8:
                data['p_warning'] = "Password is too short. Minimum length is 8"
            return render(request, 'logregapp/register.html', data)
        myUser = User.objects.create_user(username, email, password1)
        myUser.save()
        user = authenticate(username=username, password=password1)
        auth_login(request, user)
        try:
            send_mail('Account successfully created!', f"Hello, {username}!\
    Your account on Morent has been successfully created!", 'morentcorp@gmail.com', [user.email])
            return redirect("main")
        except Exception:
            return redirect("main")
    return render(request, 'logregapp/register.html', {})

def signout(request: HttpRequest):
    """
    This function signouts user from his account.
    """
    logout(request)
    return redirect(login)
