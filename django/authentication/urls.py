from django.urls import path, include

from authentication.views import login_page

urlpatterns = [
    path('login/', login_page)
]