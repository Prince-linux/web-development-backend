from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q

# Create your views here.



def login_page(request):
    return render(request, "authentication/login.html")

def login_user(request):
    pass

def registration(request):
    pass

def logout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success("You've been sucessfully logged out!")
    return redirect("authenticate:login")


    