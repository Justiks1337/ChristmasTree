from django.urls import path

from .views import buy_toy, get_user_toys, update_exp, on_start_command

urlpatterns = [
    path('buy_toy/', buy_toy),
    path('get_user_toys/', get_user_toys),
    path('update_exp/', update_exp),
    path('on_start_command/', on_start_command)
]
