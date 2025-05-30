from django.urls import path

from .views import buy_toy, get_user_toys, update_exp

urlpatterns = [
    path('buy_toy/', buy_toy),
    path('get_user_toys/', get_user_toys),
    path('update_ext/', update_exp),
    path('on_start_command/', update_exp)
]
