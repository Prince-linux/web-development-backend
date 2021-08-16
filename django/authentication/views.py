from django.shortcuts import render

# Create your views here.



def login_page(request):
    return render(request, "authentication/login.html")

def login_user(request):
    pass

def registration(request):
    pass

def logout(request):
    pass


    