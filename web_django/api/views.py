import uuid
from functools import wraps

from asgiref.sync import sync_to_async
from adrf import decorators
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from new_year.settings import SECRET_KEY

import api.models


def bot_auth_required(view_func):
    """Декоратор для проверки авторизации телеграм-бота"""
    @wraps(view_func)
    async def wrapper(request, *args, **kwargs):
        # Проверка токена из заголовка Authorization
        auth_header = request.META.get('HTTP_AUTHORIZATION')

        if not auth_header or not auth_header.startswith('Bot '):
            return Response(
                {"error": "Требуется авторизация бота"}, 
                status=status.HTTP_401_UNAUTHORIZED
            )

        token = auth_header.split(' ')[1]
        if token != SECRET_KEY:
            return Response(
                {"error": "Неверный токен авторизации"}, 
                status=status.HTTP_403_FORBIDDEN
            )

        return await view_func(request, *args, **kwargs)
    return wrapper


@decorators.api_view(['POST'])
async def buy_toy(request: Request):
    user_id = request.query_params.get('user_id')
    slot = request.query_params.get('slot')
    toy_id = request.query_params.get('toy')

    toy_data = await api.models.ToyTypes.objects.aget(id=toy_id)
    user_data = await api.models.User.objects.aget(user_id=user_id)

    if user_data.exp - toy_data.exp < 0:
        return Response(JSONRenderer().render({"success": False, "message": "Недостаточно новогоднего настроения! Общайся в чате что бы получить больше!"}))

    user_data.exp = user_data.exp - toy_data.exp
    await user_data.asave()
    toy = await api.models.Toys.objects.filter(owner=user_data, slot=slot).afirst()
    if toy is not None:
        toy.toy = toy_data
        await toy.asave()
        return Response(JSONRenderer().render({"success": True, 'message': "Игрушка успешно куплена!", "exp": user_data.exp - toy_data.exp}))

    await api.models.Toys.objects.acreate(owner=user_data, slot=slot, toy=toy_data)
    return Response(JSONRenderer().render({"success": True, 'message': "Игрушка успешно куплена!", "exp": user_data.exp - toy_data.exp}))


@sync_to_async
@decorators.api_view(['GET'])
def get_user_toys(request: Request):

    user_id = request.query_params.get('user_id')
    queryset = api.models.Toys.objects.filter(owner=user_id)
    return Response(JSONRenderer().render({'items': [[i.id, i.owner.user_id, i.toy.id, i.slot] for i in queryset]}))


@decorators.api_view(['PUT'])
@bot_auth_required
async def update_exp(request: Request):
    """
    Обновляет количество опыта (новогоднего настроения) для указанного пользователя.

    Этот эндпоинт используется телеграм-ботом для изменения значения опыта пользователя.

    Args:
        request (Request): HTTP запрос, который должен содержать:
            - exp (int): Новое значение опыта пользователя
            - user_id (int): Идентификатор пользователя

    Returns:
        Response: HTTP ответ со статусом 200 в случае успешного обновления

    Examples:
        PUT /api/update_exp/
        Request body:
        {
            "exp": 100,
            "user_id": 1
        }

        Headers:
        Authorization: Bot <ваш_секретный_токен>

    Note:
        - Для доступа требуется токен авторизации бота в заголовке
        - Метод является асинхронным

    Raises:
        User.DoesNotExist: Если пользователь с указанным user_id не найден
    """

    exp = request.data.get('exp')
    user_id = request.data.get('user_id')

    user_data = await api.models.User.objects.aget(user_id=user_id)
    user_data.exp = user_data.exp + exp
    await user_data.asave()

    return Response(200)


@decorators.api_view(['POST'])
@bot_auth_required
async def on_start_command(request: Request):
    user_id = request.data.get('user_id')
    username = request.data.get('username')

    user = await api.models.User.objects.filter(user_id=user_id).afirst()

    if user is None:
        user = await api.models.User.objects.acreate(user_id=user_id, username=username, exp=0, uuid=uuid.uuid4())

    return Response(JSONRenderer().render({"uuid": user.uuid}))