from django.shortcuts import render, HttpResponse, redirect
from .models import User
from django.contrib import messages
import bcrypt
import datetime
import re

# ----------------------------------------------------------------------------
# Routes to render templates
# ----------------------------------------------------------------------------

def index(request):
    if not request.session['isloggedin']:
        return redirect('/')
    else:
        return render(request, 'ayo_app/index.html')

def login(request):
    return render(request, 'ayo_app/login.html')

def credits(request):
    if not request.session['isloggedin']:
        return redirect('/')
    else:
        return render(request, 'ayo_app/credit.html')

def game(request):
    if not request.session['isloggedin']:
        return redirect('/')
    else:
        return render(request, 'ayo_app/game.html')

def tutorial(request):
    if not request.session['isloggedin']:
        return redirect('/')
    else:
        return render(request, 'ayo_app/tutorial.html')

def leaderboard(request):
    if not request.session['isloggedin']:
        return redirect('/')
    else:
        return render(request, 'ayo_app/leaderboard.html')

# ----------------------------------------------------------------------------
# Route to validate, register user and redirect to home page
# ----------------------------------------------------------------------------

def addUser(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        messages.error(request, request.POST["first_name"], "holdFName")
        messages.error(request, request.POST["last_name"], "holdLName")
        messages.error(request, request.POST["email"], "holdEmail")
        messages.error(request, request.POST["username"], "holdusername")
        return redirect('/')
    else:
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        username = request.POST["username"]
        pw_to_hash = request.POST["password"]
        password = bcrypt.hashpw(pw_to_hash.encode(), bcrypt.gensalt())
        password = password.decode()
        new_user = User.objects.create(
            first_name=first_name, last_name=last_name, email=email, username=username, password=password)
        request.session['userid'] = new_user.id
        request.session['first_name'] = new_user.first_name
        request.session['isloggedin'] = True
        request.session.modified = True
        return redirect("/home")

# ----------------------------------------------------------------------------
# Route to login and route to home page
# ----------------------------------------------------------------------------

def loginUser(request):
    if len(request.POST['emailLogin']) == 0:
    
        return redirect('/')
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        messages.error(request, request.POST["emailLogin"], "holdLoginEmail")
        return redirect('/')
    else:
        current_user = User.objects.get(email=request.POST['emailLogin'])
        request.session['userid'] = current_user.id
        request.session['isloggedin'] = True
        request.session['first_name'] = current_user.first_name
        return redirect("/home")

# ----------------------------------------------------------------------------
# Route to logout user
# ----------------------------------------------------------------------------

def logout(request):
    request.session.clear()
    request.session['isloggedin'] = False
    return redirect('/')








