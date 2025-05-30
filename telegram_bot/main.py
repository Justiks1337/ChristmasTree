import asyncio

import aiogram
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardBuilder
from aiohttp import ClientSession

from config.Config import Config

bot = aiogram.Bot(Config.bot_token)
dispatcher = aiogram.Dispatcher()

HOST = "127.0.0.1"
PROTOCOL = "http://"


@dispatcher.message(Command("ёлка"))
async def christmas_tree_command_handler(message: aiogram.types.Message):
    user = message.from_user
    uuid_ = await database_manipulation(user)
    url = f"{PROTOCOL}{HOST}/?user_id={user.id}&uuid={uuid_}"
    # url = "https://google.com/"

    web_app = aiogram.types.WebAppInfo(url=url)
    keyboard_builder = InlineKeyboardBuilder()
    button = InlineKeyboardButton(text="Ссылка на елку", web_app=web_app)
    keyboard_builder.add(button)

    await bot.send_message(message.chat.id, "Успех ✅", reply_markup=keyboard_builder.as_markup())

    await message.delete()


async def database_manipulation(user: aiogram.types.User):
    """
    Args:
        user: aiogram user objects

    Returns: uuid of user
    """

    payload = {
        "user_id": user.id,
        "username": user.username,
    }

    async with ClientSession() as session:
        async with session.post(f"{PROTOCOL}{HOST}/api/v1/on_start_command/", json=payload) as response:
            result = await response.json()
            return result["uuid"]


@dispatcher.message()
async def main_handler(message: aiogram.types.Message):
    chat_id = message.chat.id
    if chat_id in [-1001720982250, -1001530910994]:
        points = round(len(message.text) / 10)

        payload = {
            "user_id": message.from_user.id,
            "exp": points,
        }

        async with ClientSession() as session:
            async with session.put(f"{PROTOCOL}{HOST}/api/v1/update_ext/", json=payload):
                pass


def get_name(user: aiogram.types.User):
    username = user.username

    if not username:
        username = user.first_name

    return username


if __name__ == '__main__':
    asyncio.run(dispatcher.start_polling(bot))
