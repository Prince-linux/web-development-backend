# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.shortcuts import render, redirect

from authentication.forms import SignupForm, LoginForm
from authentication.models import User
from authentication.utils import validate_data

# Create your views here.



def login_page(request):
    if request.user.is_authenticated:
        if request.user_type == 'ADMIN':
            return redirect('core:admin_home')
        else:
            return redirect('core:user_home')

    return render(request, "authentication/login.html")



def login_in(request):
    """Logs the user in
    Retrieves the username and password provided by the
    user after validating the form. The username and
    password is authenticated, and if successful, the
    user is logged into the current session.
    If the authentication fails, or the form data provided
    is invalid, or the data provided already exist, the
    user is presented with the form and the appropriate
    error message.
    :param request: The WSGIRequest object for the current session
    :return HttpResponse:
    """
    if request.user.is_authenticated:
        if request.user.user_type == 'ADMIN':
            return redirect('core:admin_home')
        else:
            return redirect('core:user_home')

    if request.method == "POST":

        # Get the login form with the data bound to it
        form = LoginForm(request.POST)

        # check to see if the data provided is valid.
        if form.is_valid():

            # If the data is valid, retrieve it.
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # check to ensure that the username is not None.
            # If it is, inform the user accordingly and presented
            # with the form to try again
            if username is not None and len(username) != 0:

                # authenticate the user. If the user object is not None,
                # it means the user exists in the system. Then if the password
                # check passes, the user is logged in and redirected to their
                # dashboard.
                user = authenticate(username=username, password=password)
                if user is not None:
                    if user.user_type == 'ADMIN':
                        user.check_password(password)
                        login(request, user)
                        messages.success(request, "You've been successfully logged in! ")
                        return redirect('core:admin_home')
                    else:
                        user.check_password(password)
                        login(request, user)
                        messages.success(request, "You've been successfully logged in! ")
                        return redirect('core:user_home')
                else:
                    messages.warning(request, "Username and/or password does not exist")
                    return render(request, "authentication/login.html", {
                        'form': form
                    })
    else:
        # For a GET request, create a login form ad pass it
        # to the login page for rendering.
        form = LoginForm()

    # render the login page along with the form
        return render(request, "authentication/login.html", {
            'form': form
        })



def registration(request):
    if request.user.is_authenticated:
        if request.user.user_type == 'ADMIN':
            return redirect('core:admin_home')
        else:
            return redirect('core:user_home')

    if request.method == 'POST':
        # import pdb;
        # pdb.set_trace()

        # Bind the form with the data submitted and check to
        # see if the data is valid.
        form = SignupForm(request.POST)
        # import pdb; pdb.set_trace()
        if form.is_valid():

            # retrieve the valid data
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            confirm_password = form.cleaned_data["confirm_password"]
            email = form.cleaned_data["email"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            user_type = form.cleaned_data["user_type"]

            # validate the information provided by the user. If there is
            # some invalid data, redirect to the registration page with
            # the error messages
            ok, msg = validate_data(username, password, confirm_password, email, first_name, last_name, user_type)
            if not ok:
                for m in msg:
                    messages.warning(request, m)

                return redirect('authentication:signup_page')
            else:
                # Ensure that the username provided is unique. If so, create and
                # save a new user instance
                if User.objects.filter(Q(username__exact=username) | Q(email__exact=email)).first() is None:
                    user = User(
                        username=username, password=password,
                        email=email, first_name=first_name,
                        last_name=last_name, user_type=user_type
                    )
                    user.set_password(password)
                    user.save()

                    # sign them in and redirect to dashboard after authentication
                    user = authenticate(username=username, password=password)
                    if user is not None:
                        # login(request, user)
                        messages.success(request, "Registration successful! Welcome %s !" %user.username)

                        return redirect('authentication:login')
                else:
                        # User already exists
                    messages.warning(request, "A user with that Email already exist")
                    return render(request, "authentication/signup.html", {
                        'registration_form': form
                    })
    else:
        # For a GET request, create a registration form ad pass it
        # to the login page for rendering.
        form = SignupForm()

    return render(request, "authentication/signup.html", {
        'form': form
    })


def logout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success("You've been sucessfully logged out!")
    return redirect("authenticate:login")


    