import asyncio
from uuid import uuid4

import aiogram
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardBuilder

from config.Config import Config
from database.Connection import connect

bot = aiogram.Bot(Config.bot_token)
dispatcher = aiogram.Dispatcher()


@dispatcher.message(Command("ёлка"))
async def christmas_tree_command_handler(message: aiogram.types.Message):

    user = message.from_user
    uuid_ = await database_manipulation(user)
    url = f"http://127.0.0.1:8000/?user_id={user.id}&uuid={uuid_}"
    #url = "https://google.com/"

    web_app = aiogram.types.WebAppInfo(url=url)
    keyboard_builder = InlineKeyboardBuilder()
    button = InlineKeyboardButton(text="Ссылка на елку", web_app=web_app)
    keyboard_builder.add(button)

    await bot.send_message(message.chat.id, "Успех ✅", reply_markup=keyboard_builder.as_markup())

    await message.delete()


async def database_manipulation(user: aiogram.types.User):
    user_info = await (await connect.request("SELECT * FROM users WHERE user_id = ?", (user.id,))).fetchone()

    if not user_info:
        id_ = user.id
        user_name = get_name(user)
        exp = 0
        uuid_ = str(uuid4())

        await connect.request("INSERT INTO users VALUES (?, ?, ?, ?)", (id_, user_name, exp, uuid_))

        return uuid_

    return str(user_info[3])


@dispatcher.message()
async def main_handler(message: aiogram.types.Message):
    chat_id = message.chat.id
    if chat_id in [-1001720982250, -1001530910994]:
        points = round(len(message.text) / 10)
        await connect.request("UPDATE users SET exp = exp + ? WHERE user_id = ?", (points, message.from_user.id))


def get_name(user: aiogram.types.User):
    username = user.username

    if not username:
        username = user.first_name

    return username

if __name__ == '__main__':
    asyncio.run(dispatcher.start_polling(bot))
