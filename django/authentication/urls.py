from django.urls import path, include

from authentication.views import login_page, registration, logout, login_user


app_name = 'authentication'

urlpatterns = [
    path('login/', login_page, name="login"),
    path('signup/', registration, name="signup_page"),
    path('logout/', logout, name="logout")
]