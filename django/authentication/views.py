from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q

# Create your views here.



def login_page(request):
    if request.user.is_authenticated:
        if request.user_type == 'ADMIN':
            return redirect('core:admin_home')
        else:
            return redirect('core:user_home')

    return render(request, "authentication/login.html")



def login_user(request):
    pass


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


    