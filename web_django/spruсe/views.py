from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render

from api.models import User


async def index(request: HttpRequest):

    user_id = request.GET.get('user_id')
    uuid_ = request.GET.get('uuid')

    if not user_id or not uuid_:
        return HttpResponse('<h4>404! На ёлку можно входить только через бота!</h4>')

    user = await User.objects.aget(user_id=user_id)

    return render(request, 'spruce/index.html', {'exp': user.exp, 'user_id': user_id})
