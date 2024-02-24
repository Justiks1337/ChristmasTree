from uuid import uuid4

import aiogram

from config.Config import Config
from database.Connection import connect


bot = aiogram.Bot(Config.bot_token)
dispatcher = aiogram.Dispatcher(bot)


@dispatcher.message_handler(aiogram.dispatcher.filters.Command("ёлка"))
async def christmas_tree_command_handler(message: aiogram.types.Message):

    user = message.from_user
    uuid_ = await database_manipulation(user)
    #url = f"https://new_year.galerka-kb.ru/?user_id={user.id}&uuid={uuid_}"
    url = "https://google.com/"

    web_app = aiogram.types.WebAppInfo(url=url)
    reply_markup = aiogram.types.ReplyKeyboardMarkup()
    button = aiogram.types.KeyboardButton("Ссылка на елку", web_app=web_app)
    reply_markup.add(button)

    await bot.send_message(message.chat.id, "Успех ✅", reply_markup=reply_markup)

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


@dispatcher.message_handler()
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


aiogram.executor.start_polling(dispatcher)
