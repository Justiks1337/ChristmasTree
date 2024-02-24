from django.shortcuts import render
from django.http.response import HttpResponse
from django.http.request import HttpRequest

from database.Connection import connect


async def index(request: HttpRequest):

    user_id = request.GET.get('user_id')
    uuid_ = request.GET.get('uuid')

    if not user_id or not uuid_:
        return HttpResponse('<h4>404! На ёлку можно входить только через бота!</h4>')

    exp = (await (await connect.request("SELECT exp FROM users WHERE user_id = ?", (user_id, ))).fetchone())[0]

    return render(request, 'spruce/index.html', {'exp': exp, 'user_id': user_id})


