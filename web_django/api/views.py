from adrf import decorators
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.renderers import JSONRenderer
from django.shortcuts import render

from database.Connection import connect


@decorators.api_view(['GET'])
async def get_toys(request: Request):
    return Response(JSONRenderer().render({"items": await (await connect.request("SELECT * FROM toy_types")).fetchall()}))


@decorators.api_view(['POST'])
async def buy_toy(request: Request):
    user_id = request.query_params.get('user_id')
    slot = request.query_params.get('slot')
    toy_id = request.query_params.get('toy')

    toy_data = await (await connect.request("SELECT * FROM toy_types WHERE id = ?", (toy_id, ))).fetchone()
    user_data = await (await connect.request("SELECT * FROM users WHERE user_id = ?", (user_id, ))).fetchone()

    if user_data[2] - toy_data[2] < 0:
        return Response(JSONRenderer().render({"success": False, "message": "Недостаточно новогоднего настроения! Общайся в чате что бы получить больше!"}))

    await connect.request("UPDATE users SET exp = ? WHERE user_id = ?", (user_data[2] - toy_data[2], user_id))

    if await (await connect.request("SELECT id FROM toys WHERE owner = ? AND slot = ?", (user_id, slot))).fetchone():
        await connect.request("UPDATE toys SET toy = ? WHERE owner = ? AND slot = ?", (toy_id, user_id, slot))
        return Response(JSONRenderer().render({"success": True, 'message': "Игрушка успешно куплена!", "exp": user_data[2] - toy_data[2]}))

    await connect.request("INSERT INTO toys VALUES (?, ?, ?, ?)", (None, user_id, toy_id, slot))
    return Response(JSONRenderer().render({"success": True, 'message': "Игрушка успешно куплена!", "exp": user_data[2] - toy_data[2]}))


@decorators.api_view(['GET'])
async def get_user_toys(request: Request):

    user_id = request.query_params.get('user_id')
    data = await (await connect.request("SELECT * FROM toys WHERE owner = ?", (user_id, ))).fetchall()

    return Response(JSONRenderer().render({'items': data}))
