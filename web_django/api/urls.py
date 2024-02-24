from django.urls import path, include

from .views import get_toys, buy_toy, get_user_toys


urlpatterns = [
    path('get_toys/', get_toys),
    path('buy_toy/', buy_toy),
    path('get_user_toys/', get_user_toys)
]
